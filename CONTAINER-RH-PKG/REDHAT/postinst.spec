%post
#!/bin/bash

printf "\n* Container postinst...\n" | tee -a /dev/tty

printf "\n* Building podman image...\n" | tee -a /dev/tty
cd /usr/lib/api-f5

# Build container image.
buildah bud -t api-f5 . | tee -a /dev/tty

printf "\n* The container will start in few seconds.\n\n"

function containerSetup()
{
    wallBanner="RPM automation-interface-api-f5-container post-install configuration message:\n"
    cd /usr/lib/api-f5

    # Grab the host timezone.
    timeZone=$(timedatectl show| awk -F'=' '/Timezone/ {print $2}')

    # First container run: associate name, bind ports, bind fs volume, define init process, ...
    # api-f5 folder will be bound to /var/lib/containers/storage/volumes/.
    podman run --name api-f5 -v api-f5:/var/www/api/api -v api-f5-db:/var/lib/mysql -v api-f5-cacerts:/usr/local/share/ca-certificates -dt localhost/api-f5 /sbin/init
    podman exec api-f5 chown www-data:www-data /var/www/api/api # within container.

    podman exec api-f5 chown mysql:mysql /var/lib/mysql # within container.
    podman exec api-f5 systemctl restart mysql

    printf "$wallBanner Starting Container Service on HOST..." | wall -n
    systemctl daemon-reload

    systemctl start automation-interface-api-f5-container # (upon installation, container is already run).
    systemctl enable automation-interface-api-f5-container

    printf "$wallBanner Configuring container..." | wall -n
    # Setup a Django secret key: using host-bound folders.
    djangoSecretKey=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
    sed -i "s|^SECRET_KEY =.*|SECRET_KEY = \"$djangoSecretKey\"|g" /var/lib/containers/storage/volumes/api-f5/_data/settings.py

    # Setup the JWT token public key (taken from SSO): using host-bound folders.
    cp -f /var/lib/containers/storage/volumes/sso/_data/settings_jwt.py /var/lib/containers/storage/volumes/api-f5/_data/settings_jwt.py
    sed -i -e ':a;N;$!ba;s|\s*"privateKey.*}|\n}|g' /var/lib/containers/storage/volumes/api-f5/_data/settings_jwt.py

    printf "$wallBanner Set the timezone of the container to be the same as the host timezone..." | wall -n
    podman exec api-f5 bash -c "timedatectl set-timezone $timeZone"

    printf "$wallBanner Internal database configuration..." | wall -n
    if podman exec api-f5 mysql -e "exit"; then
        # User api.
        # Upon podman image creation, a password is generated for the user api.
        databaseUserPassword=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

        if [ "$(podman exec api-f5 mysql --vertical -e "SELECT User FROM mysql.user WHERE User = 'api';" | tail -1 | awk '{print $2}')" == "" ]; then
            # User api not present: create.
            echo "Creating api user..."
            podman exec api-f5 mysql -e "CREATE USER 'api'@'localhost' IDENTIFIED BY '$databaseUserPassword';"
            podman exec api-f5 mysql -e "GRANT USAGE ON *.* TO 'api'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;"
            podman exec api-f5 mysql -e 'GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW, SHOW VIEW, EXECUTE ON `api`.* TO `api`@`localhost`;'
        else
            # Update user's password.
            echo "Updating api user's password..."
            podman exec api-f5 mysql -e "SET PASSWORD FOR 'api'@'localhost' = PASSWORD('$databaseUserPassword');"
        fi

        # Change database password into Django config file, too.
        echo "Configuring Django..."
        sed -i "s/^.*DATABASE_USER$/        'USER': 'api', #DATABASE_USER/g" /var/lib/containers/storage/volumes/api-f5/_data/settings.py
        sed -i "s/^.*DATABASE_PASSWORD$/        'PASSWORD': '$databaseUserPassword', #DATABASE_PASSWORD/g" /var/lib/containers/storage/volumes/api-f5/_data/settings.py

        # Database api.
        echo "Creating database api and restoring SQL dump..."
        if [ "$(podman exec api-f5 mysql --vertical -e "SHOW DATABASES LIKE 'api';" | tail -1 | awk -F': ' '{print $2}')" == "" ]; then
            podman exec api-f5 mysql -e 'CREATE DATABASE api DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;' # create database.
            podman exec api-f5 mysql api -e "source /var/www/api/f5/sql/f5.schema.sql" # restore database schema.
            podman exec api-f5 mysql api -e "source /var/www/api/f5/sql/f5.data.sql" # restore database data.
        fi

        # Database update via diff.sql (migrations).
        echo "Applying migrations..."
        podman exec api-f5 bash /var/www/api/f5/sql/migrate.sh

        # Activate mysql audit plugin.
        podman exec api-f5 bash -c "cp -p /usr/share/automation-interface-api/51-mariadb.cnf /etc/mysql/mariadb.conf.d"
    else
        echo "Failed to access MariaDB RDBMS, auth_socket plugin must be enabled for the database root user. Quitting."
        exit 1
    fi

    printf "$wallBanner Restarting container's services..." | wall -n
    podman exec api-f5 systemctl restart apache2
    podman exec api-f5 systemctl restart mariadb

    diffOutput=$(podman exec api-f5 diff /var/www/api_default_settings.py /var/www/api/api/settings.py | grep '^[<>].*' | grep -v SECRET | grep -v PASSWORD | grep -v VENV || true)
    if [ -n "$diffOutput" ]; then
        printf "$wallBanner Differences from package's stock config file and the installed one (please import NEW directives in your installed config file, if any):\n* $diffOutput" | wall -n
    fi

    # syslog-ng seems going into a catatonic state while updating a package: restarting the whole thing.
    if rpm -qa | grep -q automation-interface-log; then
        if systemctl list-unit-files | grep -q syslog-ng.service; then
            systemctl restart syslog-ng || true # on host.
            podman exec api-f5 systemctl restart syslog-ng # on this container.
        fi
    fi

    rm -f /home/bck/api-f5/placeholder
    # Schedule the databases backup.
    (crontab -l ; echo "03 3 * * * /usr/bin/bck-db_api-f5.sh api >/dev/null 2>&1") | crontab -

    printf "$wallBanner Installation completed." | wall -n
}

systemctl start atd

{ declare -f; cat << EOM; } | at now
containerSetup
EOM

exit 0

