import asyncio
import asyncssh
from datetime import datetime

from logging import getLogger
_log = getLogger(__name__)


class Ssh:
    def __init__(self, app, db, options):
        self._server = None
        self._db = db
        self._options = options

        app.cleanup_ctx.append(self._sshd_engine)

    async def _sshd_engine(self, app):
        MySSHServer.set_db(self._db)
        self._server = await asyncssh.listen(
            self._options.ssh_server_bind_address,
            self._options.ssh_server_bind_port,
            reuse_port=self._options.ssh_server_reuse_port,
            server_host_keys=self._options.ssh_server_host_key,
            process_factory=self._handle_client,
            server_factory=MySSHServer)
        _log.debug("SSH engine started")
        yield
        MySSHServer.shutdown_all()
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
        _log.debug("SSH engine stopped")

    def _handle_client(self, process):
        process.stdout.write('Welcome to my SSH server, %s!\n' %
                             process.get_extra_info('username'))
        process.exit(0)

    def get_clients(self):
        return MySSHServer.get_clients()


class MySSHServer(asyncssh.SSHServer):
    _conn_list = []
    _db = None

    @classmethod
    def set_db(cls, db):
        cls._db = db

    @classmethod
    def shutdown_all(cls):
        for conn in cls._conn_list:
            conn.close()

    @classmethod
    def get_clients(cls):
        ret = []
        for conn in cls._conn_list:
            ret.append({
                'client_id': conn.get_extra_info('client_id'),
                'timestamp': conn.get_extra_info('timestamp'),
                'cloud_identifier': conn.get_extra_info('username'),
                'listen_port': conn.get_extra_info('listen_port'),
                'ip': conn.get_extra_info('peername')[0],
                'port': conn.get_extra_info('peername')[1]

            })
        return ret

    def __init__(self):
        self._conn = None

    async def server_requested(self, listen_host, listen_port):
        if (listen_host != 'localhost' or
                listen_port != self._conn.get_extra_info('listen_port')):
            _log.error('unallowed TCP forarding requested from: {}'.format(
                self._conn.get_extra_info('username')))
            await asyncio.sleep(3)
            return False
        _log.debug(f'Port forwarding established: {listen_host}:{listen_port}')
        # TODO Write log-information to database: timestamp,
        return True

    def connection_made(self, conn):
        self._conn = conn
        _log.debug('SSH connection received from {}'.format(
            conn.get_extra_info('peername')[0]))
        MySSHServer._conn_list.append(conn)

    def connection_lost(self, exc):
        if exc:
            _log.debug(f'SSH connection error: {exc}')
        else:
            _log.debug('SSH connection closed.')
        MySSHServer._conn_list.remove(self._conn)
        self._conn = None

    async def begin_auth(self, username):
        cursor = await MySSHServer._db.conn.cursor()
        await cursor.execute("""SELECT *
                          FROM clients
                          WHERE cloud_identifier = %s""", (username,))
        client = await cursor.fetchone()
        if client is None or client['is_disabled']:
            await asyncio.sleep(3)
            return True

        self._conn.set_extra_info(listen_port=client['ssh_server_listen_port'])
        self._conn.set_extra_info(client_id=client['id'])
        self._conn.set_extra_info(timestamp=datetime.now())

        key = asyncssh.import_authorized_keys(
            client['public_user_key'])
        self._conn.set_authorized_keys(key)
        return True

    def public_key_auth_supported(self):
        return True

    def validate_public_key(self, username, key):
        return True
