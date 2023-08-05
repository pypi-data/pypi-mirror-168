import aiomysql


from yoyo import read_migrations
from yoyo import get_backend

from logging import getLogger
_log = getLogger(__name__)


class Db:
    def __init__(self, app=None, options=None):
        self.conn = None
        self.pool = None
        self._app = app
        self._options = options

        app.cleanup_ctx.append(self._db_engine)

    async def _db_engine(self, app):
        try:
            self.conn = await aiomysql.connect(
                user=self._options.db_user,
                password=self._options.db_password,
                db=self._options.db_name,
                cursorclass=aiomysql.DictCursor)
        except aiomysql.Error as e:
            _log.error(f'Unable to connect to database: {e}')

        try:
            self.pool = await aiomysql.create_pool(
                user=self._options.db_user,
                password=self._options.db_password,
                db=self._options.db_name,
                cursorclass=aiomysql.DictCursor)
        except aiomysql.Error as e:
            _log.error(f'Unable to connect to database: {e}')

# TODO Fix clean error handling
            exit(1)
        _log.debug("DB engine started")
        yield
        # close = getattr(self.conn, "close", None)
        if callable(self.conn.close):
            self.conn.close()

        self.pool.close()
        await self.pool.wait_closed()

        _log.debug("DB engine stopped")

    def migrate(self):
        try:
            backend = get_backend(
                'mysql://{}:{}@localhost/{}'.format(self._options.db_user,
                                                    self._options.db_password,
                                                    self._options.db_name)
            )
        except Exception as e:
            _log.error(f'Unable to open database: {e}')
            return False

        migrations = read_migrations(self._options.db_migrations_dir)

        try:
            with backend.lock():
                backend.apply_migrations(backend.to_apply(migrations))
        except Exception as e:
            _log.error(f'Database Migration went wrong: {e}')
            return False
        return True
