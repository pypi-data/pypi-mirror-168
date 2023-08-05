import asyncio
import configargparse
import pkg_resources
import sys
from pathlib import Path

import logging
from logging.handlers import TimedRotatingFileHandler

from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp_debugtoolbar
from aiohttp_session import setup as session_setup
import base64
from cryptography import fernet
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from riegocloud import __version__

from riegocloud.ssh import Ssh
from riegocloud.db import Db
from riegocloud.web.security import Security

from riegocloud.web.views.home import Home
from riegocloud.web.views.system import System
from riegocloud.web.views.api import Api
from riegocloud.web.views.clients import Clients
from riegocloud.web.views.users import Users


app_name = 'riegocloud'


def main():
    options = _get_options()

    _setup_logging(options=options)

    if sys.version_info >= (3, 8) and options.WindowsSelectorEventLoopPolicy:
        asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy  # noqa: E501

    if sys.platform != "win32":
        import uvloop  # pylint: disable=import-error
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = web.Application()

    @web.middleware
    async def middleware1(request, handler):
        print(f'{request.remote} {request.rel_url} {request.headers}')
        return await handler(request)

    if options.enable_request_log:
        app.middlewares.append(middleware1)

    app['version'] = __version__
    app['options'] = options

    async def on_startup(app):
        if app['options'].enable_asyncio_debug:
            loop = asyncio.get_running_loop()
            loop.set_debug(True)
        logging.getLogger(__name__).debug("on_startup")
    app.on_startup.append(on_startup)

    async def on_shutdown(app):
        logging.getLogger(__name__).debug("on_shutdown")
    app.on_shutdown.append(on_shutdown)

    async def on_cleanup(app):
        logging.getLogger(__name__).debug("on_cleanup")
    app.on_cleanup.append(on_cleanup)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    session_setup(app, EncryptedCookieStorage(secret_key))

    if options.enable_aiohttp_debug_toolbar:
        aiohttp_debugtoolbar.setup(
            app, check_host=False, intercept_redirects=False)

    app.router.add_static('/static', options.http_server_static_dir,
                          name='static', show_index=True)

    db = Db(app=app, options=options)
    if not db.migrate():
        exit(1)

    ssh = Ssh(app, db, options)
    security = Security(app, db, options)

    Api(app, db, security, options)
    Home(app, db, security, ssh)
    Clients(app, db, security)
    System(app, db, security, options)
    Users(app, db, security)

    loader = jinja2.FileSystemLoader(options.http_server_template_dir)
    aiohttp_jinja2.setup(
        app,
        loader=loader,
        # enable_async=True,
        context_processors=[
            security.current_user_ctx_processor],
    )

    web.run_app(
        app,
        host=options.http_server_bind_address,
        port=options.http_server_bind_port,
        # Logging to stderr is always on
        # access_log=_setup_access_log(options=options),
        access_log_format='%{X-Real-IP}i %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'  # noqa: E501
    )
    exit(0)


def _setup_logging(options=None):
    formatter = logging.Formatter(
        "%(asctime)s;%(levelname)s;%(name)s;%(message)s ")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if options.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    Path(options.log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        options.log_file,
        when='midnight',
        backupCount=options.log_backup_count)
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[stream_handler, file_handler])

    if options.enable_aiohttp_access_debug:
        logging.getLogger("aiohttp.access").setLevel(logging.DEBUG)
    else:
        logging.getLogger("aiohttp.access").setLevel(logging.ERROR)

    if options.enable_ssh_debug:
        logging.getLogger("asyncssh").setLevel(logging.DEBUG)
    else:
        logging.getLogger("asyncssh").setLevel(logging.ERROR)


def _setup_access_log(options=None):
    if options.http_access_log_backup_count == -1:
        return None

    Path(options.http_access_log_file).parent.mkdir(
        parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        options.http_access_log_file,
        when='midnight',
        backupCount=options.http_access_log_backup_count)
    # file_handler.setFormatter(logging.Formatter("%(message)s"))
    file_handler.setLevel(logging.DEBUG)

    access_log = logging.getLogger("http_access_log")
    access_log.setLevel(logging.DEBUG)
    # TODO Why is it not possible to disable logging to stderr?
    access_log.addHandler(file_handler)
    return access_log


def _get_options():
    p = configargparse.ArgParser(
        default_config_files=[f'/etc/{app_name}.conf',
                              f'~/.{app_name}.conf',
                              f'{app_name}.conf'],
        args_for_writing_out_config_file=['-w',
                                          '--write-out-config-file'])
    p.add('-c', '--config', is_config_file=True, env_var=app_name.capitalize(),
          required=False, help='config file path')
# Database
    p.add('--db_migrations_dir',
          help='path to database migrations directory',
          default=pkg_resources.resource_filename(app_name, 'migrations'))
    p.add('--db_user', help='Database User', default=app_name)
    p.add('--db_password',
          help='Password for Database User',
          default='Eech5jaephaepaes')
    p.add('--db_name', help='Database name', default=app_name)

# Logging
    p.add('-l', '--log_file', help='Full path to logfile',
          default=f'log/{app_name}.log')
    p.add('--log_backup_count', help='How many files to rotate',
          default=20, type=int)
    p.add('--enable_request_log', help="Homebrew requestlog",
          action='store_true')
# Secrets & Scurity
    p.add('--max_age_remember_me', type=int, default=7776000)
    p.add('--cookie_name_remember_me', default="remember_me")
    p.add('--reset_admin', help='Reset admin-pw to given value an exit')
# Memcache
    p.add('--memcached_host', help='IP adress of memcached host',
          default='127.0.0.1')
    p.add('--memcached_port', help='Port of memcached service',
          default=11211, type=int)
# HTTP-Server / API
    p.add('--http_server_bind_address',
          help='http-server bind address', default='127.0.0.1')
    p.add('--http_server_bind_port', help='http-server bind port',
          default=8181, type=int)
    p.add('--http_server_endpoint', default='/api_20210221/')
    p.add('--ssh_server_hostname', help='Send this hostname to client',
          default="my.riego.cloud")
    p.add('--ssh_server_port', help='Send this port to client',
          default=8022, type=int)
    p.add('--cloud_server_url', help='Send this hostname to client',
          default='https://my.riego.cloud')
    p.add('--http_access_log_file', help='Full path to access logfile',
          default='log/access.log')
    p.add('--http_access_log_backup_count',
          help='How many files to rotate, -1 to disable',
          default=20, type=int)
# SSH-Server
    p.add('--ssh_server_bind_port', help='ssh-server bind port',
          default=8022, type=int)
    p.add('--ssh_server_bind_address', help='ssh-server bind address',
          default='0.0.0.0')
    p.add('--ssh_server_reuse_port', help='ssh-server socket option reuse_port',
          default=True, type=bool)
    p.add('--ssh_server_host_key',
          help='ssh Host key', default='ssh/ssh_host_key')
# Apache patching
    p.add('--apache_tpl_file', help='path to apache config template(s)',
          default=pkg_resources.resource_filename(
              app_name, 'apache/apache.conf.tpl'))
    p.add('--apache_conf_file', help='path to apache config file',
          default='apache/apache.conf')
    p.add('--enable_apache_patch', action='store_true')
# NGINX patching
    p.add('--nginx_tpl_file', help='path to nginx config template(s)',
          default=pkg_resources.resource_filename(
              app_name, 'nginx/nginx.conf.tpl'))
    p.add('--nginx_conf_file', help='path to nginx config file',
          default='nginx/nginx.conf')
    p.add('--enable_nginx_patch', action='store_true')
# Directories
    p.add('--base_dir', help='Change only if you know what you are doing',
          default=Path(__file__).parent)
    p.add('--http_server_static_dir',
          help='Serve static html files from this directory',
          default=pkg_resources.resource_filename(f'{app_name}.web', 'static'))
    p.add('--http_server_template_dir',
          help='Serve template files from this directory',
          default=pkg_resources.resource_filename(
              f'{app_name}.web', 'templates'))
# Debug
    p.add('--enable_aiohttp_debug_toolbar', action='store_true')
    p.add('--enable_aiohttp_access_debug', action='store_true')
    p.add('--enable_asyncio_debug', action='store_true')
    p.add('--enable_ssh_debug', action='store_true')
    p.add('--WindowsSelectorEventLoopPolicy', action='store_true')

# Version, Help, Verbosity
    p.add('-v', '--verbose', help='verbose', action='store_true')
    p.add('--version', help='Print version and exit', action='store_true')
    p.add('--defaults', help='Print options with default values and exit',
          action='store_true')

    options = p.parse_args()
    if options.verbose:
        print(p.format_values())

    try:
        with open(f'{app_name}.conf', 'xt') as f:
            for item in vars(options):
                f.write(f'# {item}={getattr(options, item)}\n')
    except IOError:
        pass

    if options.defaults:
        for item in vars(options):
            print(f'# {item}={getattr(options, item)}')
        exit(0)

    if options.version:
        print('Version: ', __version__)
        exit(0)

    if options.reset_admin:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_reset_admin(options=options, app=None))
        loop.close
        exit(0)

    return options


async def _reset_admin(options=None, app=None):
    import aiomysql
    import bcrypt

    password = options.reset_admin
    if len(password) == 0:
        return
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode('utf-8')

    conn = await aiomysql.connect(
        user=options.db_user,
        password=options.db_password,
        db=options.db_name,
        cursorclass=aiomysql.DictCursor)
    cursor = await conn.cursor()
    try:
        await cursor.execute('''UPDATE users
                            SET password = %s
                            WHERE id = %s ''', (password, 1))
        await conn.commit()
    except aiomysql.IntegrityError:
        await conn.rollback()
    if cursor.rowcount < 1:
        print('Error: Password not changed')
    else:
        print('Succesfully reset Admin PW: {}'.format(
            password.encode('utf-8')))
    await cursor.close()
    conn.close()
