from aiohttp import web
from aiohttp_session import get_session, new_session
import aiohttp_jinja2
import bcrypt
import secrets
import asyncio

from logging import getLogger
_log = getLogger(__name__)


class Security():

    def __init__(self, app, db, options):
        self._db = db
        self._options = options
        app.router.add_get('/login', self._login, name='login')
        app.router.add_post('/login', self._login_apply)
        app.router.add_get('/logout', self._logout, name='logout')
        app.router.add_get('/profile', self._profile, name='profile')
        app.router.add_post('/profile', self._profile_apply)

    async def get_user(self, request):
        session = await get_session(request)
        user_id = session.get('user_id')
        if user_id is not None:
            async with self._db.pool.acquire() as pconn:
                async with pconn.cursor() as cur:
                    await cur.execute(
                        """SELECT *, 'session' AS provider
                        FROM users
                        WHERE id = %s""", (user_id,))
                    user = await cur.fetchone()

            # Disabled User must be logged out
            if user is None or user['is_disabled']:
                session.pop('user_id', None)
                return None
            return user
        remember_me = request.cookies.get('remember_me')
        if remember_me is not None:
            async with self._db.pool.acquire() as pconn:
                async with pconn.cursor() as cur:
                    await cur.execute(
                        """SELECT *, 'remember_me' AS provider
                        FROM users
                        WHERE remember_me = %s""", (remember_me,))
                    user = await cur.fetchone()

            # Disabled User must be logged out
            if user is not None and user['is_disabled']:
                async with self._db.pool.acquire() as pconn:
                    async with pconn.cursor() as cur:
                        await cur.execute(
                            """UPDATE users
                            SET remember_me = ''
                            WHERE id = %s""", (user['id'],))
                return None
            return user
        return None

    async def current_user_ctx_processor(self, request):
        user = await self.get_user(request)
        return {'user': user}

    async def check_perm(self, request, perm=None):
        user = await self.get_user(request)
        if user is None:
            return None
        if user['is_superuser']:
            return user
        if perm is None:
            return user

        cursor = await self._db.conn.cursor()
        await cursor.execute('''SELECT * FROM users_permissions
                        WHERE user_id = %s''', (user['id'],))
        rows = await cursor.fetchall()
        await cursor.close()
        for row in rows:
            if row['name'] == perm:
                return user
        return None

    async def raise_perm(self, request: web.BaseRequest, perm: str = None):
        """Generate redirection to login form if permission is not
        sufficent. Append query string with information for redirecting
        after login to the original url.

        :param request: [description]
        :type request: web.Baserequest
        :param perm: If no permission is given, check auth only
        :type perm: str, optional
        :raises web.HTTPSeeOther: [description]
        """
        if await self.check_perm(request, perm=perm) is None:
            raise web.HTTPSeeOther(
                request.app.router['login'].url_for(
                ).with_query(
                    {"redirect": str(request.rel_url)}
                )
            )

#    @aiohttp_jinja2.template("security/login.html")
    async def _login(self, request: web.Request):
        redirect = request.rel_url.query.get("redirect", "")
        csrf_token = secrets.token_urlsafe()
#        session = await get_session(request)
        session = await new_session(request)
        session['csrf_token'] = csrf_token
        session.changed()
        context = {'csrf_token': csrf_token, 'redirect': redirect}

        response = aiohttp_jinja2.render_template('security/login.html',
                                                  request,
                                                  context)
        return response

    async def _login_apply(self, request: web.Request):
        form = await request.post()
        session = await get_session(request)
#        if session.get('csrf_token') != form['csrf_token']:
#            _log.error('Possible CSRF attack')
#            # Normally not possible
#            await asyncio.sleep(2)
#            return web.HTTPUnauthorized()

        if form.get('identity') is None:
            await asyncio.sleep(2)
            return web.HTTPSeeOther(request.app.router['login'].url_for())

        cursor = await self._db.conn.cursor()
        await cursor.execute("""SELECT *, 'login' AS provider
                        FROM users
                        WHERE identity = %s""", (form['identity'],))
        user = await cursor.fetchone()
        await cursor.close()

        if (
            user is None or
            user['is_disabled'] or
            user['password'] is None or
            not len(user['password'])
        ):
            await asyncio.sleep(2)
            return web.HTTPSeeOther(request.app.router['login'].url_for())
        if not bcrypt.checkpw(form['password'].encode('utf-8'),
                              user['password'].encode('utf-8')):
            await asyncio.sleep(2)
            return web.HTTPSeeOther(request.app.router['login'].url_for())

        session['user_id'] = user['id']
        session.changed()

        location = form.get('redirect')
        if location is None or location == '':
            location = request.app.router['home'].url_for()
        response = web.HTTPSeeOther(location=location)
        if form.get('remember_me') is not None:
            remember_me = secrets.token_urlsafe()
            cursor = await self._db.conn.cursor()
            try:
                await cursor.execute('''UPDATE users
                                SET remember_me = %s
                                WHERE id = %s ''', (remember_me, user['id']))
                await self._db.conn.commit()
            except Exception as e:
                await self._db.conn.rollback()
                _log.error(f'Rememeber_me: unable to update: {e}')
            if cursor.rowcount < 1:
                _log.error('Rememeber_me: unable to update:')
            await cursor.close()
            response.set_cookie("remember_me", remember_me,
                                max_age=self._options.max_age_remember_me,  # noqa: E501
                                httponly=True,
                                samesite='strict')
        return response

    async def _logout(self, request: web.Request):
        user = await self.get_user(request)
        cursor = await self._db.conn.cursor()
        if user is not None:
            try:
                await cursor.execute("""UPDATE users
                                SET remember_me = ''
                                WHERE id = %s""", (user['id'],))
                await self._db.conn.commit()
            except Exception as e:
                _log.error(f'logout: Unable to Update: {e}')
                await self._db.conn.rollback()
            if cursor.rowcount < 1:
                _log.error('logout: Unable to Update')
            await cursor.close()
        session = await get_session(request)
        if session is not None:
            session.pop('user_id', None)
        session.invalidate()
        response = web.HTTPSeeOther(request.app.router['login'].url_for())
    #    response.set_cookie('remember_me', None,
    #                        expires='Thu, 01 Jan 1970 00:00:00 GMT')
        response.del_cookie('remember_me')
        return response

    @ aiohttp_jinja2.template("security/profile.html")
    async def _profile(self, request: web.Request):
        return {}

    async def _profile_apply(self, request: web.Request):
        form = await request.post()
        user = await self.get_user(request)

    # TODO check old_password and equality of pw1 an pw2
        password = form['new_password_1'].encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        password = password.decode('utf-8')
        cursor = await self._db.conn.cursor()
        try:
            await cursor.execute('''UPDATE users
                            SET password = %s
                            WHERE id = %s ''', (password, user['id']))
            await self._db.conn.commit()
        except Exception as e:
            _log.error(f'Unable to update: {e}')
            await self._db.conn.rollback()
        if cursor.rowcount < 1:
            await cursor.close()
            return web.HTTPSeeOther(request.app.router['profile'].url_for())
        else:
            await cursor.close()
            return web.HTTPSeeOther(request.app.router['home'].url_for())
