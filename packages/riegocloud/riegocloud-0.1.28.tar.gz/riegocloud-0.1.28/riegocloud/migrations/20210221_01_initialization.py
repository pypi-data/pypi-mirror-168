"""

"""

from yoyo import step

__depends__ = {'__init__'}

steps = [
    step(
    '''CREATE TABLE users (
	id	        INT AUTO_INCREMENT,
	identity	    VARCHAR(255),
	password	    VARCHAR(1000),
    full_name     VARCHAR(255),
    email         VARCHAR(255),
    permission_id	TINYINT,
	is_superuser	TINYINT DEFAULT 0,
	is_disabled	TINYINT DEFAULT 0,
	remember_me	VARCHAR(255),
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT identity_uc UNIQUE(identity),
	PRIMARY KEY(id))''',
    '''DROP TABLE users'''
    ),
    step(
    '''INSERT INTO users
    (identity,password,is_superuser)
    VALUES ("admin","$2b$12$P4VfSJN/iJ2o9CSLGjS87.IcmOaZTc1T0rxfAJQ0/Z7i3RW2G47iu",1)''',
    """DELETE FROM users WHERE identity = "admin" """
    ),
    step(
    ''' CREATE TABLE users_permissions (
	id	        INT AUTO_INCREMENT,
	name	        VARCHAR(255),
	user_id	    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(id))''',
    ''' DROP TABLE users_permissions '''
    ),
    step(
    ''' CREATE TABLE users_tokens (
	id	        INT AUTO_INCREMENT,
	sequence	    VARCHAR(255) NOT NULL,
    hash	        VARCHAR(255),
    category	    VARCHAR(255),
	user_id	    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT sequence_uc UNIQUE(sequence),
	PRIMARY KEY(id))''',
    ''' DROP TABLE users_tokens '''
    ),
    step(
    '''CREATE TABLE clients (
	id	                    INT AUTO_INCREMENT,
	cloud_identifier	        VARCHAR(255),
    is_disabled               INTEGER DEFAULT 0,
	public_user_key    	    VARCHAR(255),
    ssh_server_listen_port    INTEGER,
  	ssh_server_hostname       VARCHAR(255),
    ssh_server_port           INTEGER,
	created_at	            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cloud_identifier_uc UNIQUE(cloud_identifier),
    CONSTRAINT ssh_server_listen_port_uc UNIQUE(ssh_server_listen_port),
	PRIMARY KEY(id))''',
    '''DROP TABLE clients'''
    )
]