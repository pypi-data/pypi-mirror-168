#!/bin/sh


mysql -u root <<"EOT"
DROP DATABASE IF EXISTS riegocloud;
CREATE DATABASE riegocloud;
CREATE USER IF NOT EXISTS 'riegocloud'@'localhost' IDENTIFIED BY 'Eech5jaephaepaes';
GRANT ALL PRIVILEGES ON riegocloud.* TO 'riegocloud'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'riegocloud'@'localhost';
EOT



sudo bash -c "cat > /etc/systemd/system/riegocloud.service" <<'EOT'
[Unit]
Description=Riego Cloud Service
After=mariadb.service
StartLimitIntervalSec=0

[Service]
Environment="PYTHONUNBUFFERED=1"
Type=simple
User=riegocloud
WorkingDirectory=/srv/riegocloud
ExecStart=/srv/riegocloud/.venv/bin/riegocloud
Restart=always
RestartSec=60s

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable riegocloud
systemctl restart riegocloud
