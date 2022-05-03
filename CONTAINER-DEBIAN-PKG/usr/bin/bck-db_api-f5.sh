#!/bin/bash

# Backup script for databases in the api-vmware container.
# Run from the host via podman exec, so the backup is not deleted even if the container package is purged.

PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin

if [ -z "$1" ]; then
    echo "Usage: $0: db_name"
    exit 0
fi

if ! echo "$1" | grep -Eq 'api'; then
    echo "Databases on this api: api"
    exit 1
fi

now=`date +%Y%m%d-%H.%M`
db=$1
api="api-f5"
bckDir="/home/bck/${api}"
bckFile="${db}_${api}_${now}.dmp.xz"
containerDir="/var/www/api/api"
containerDirOnHost="/var/lib/containers/storage/volumes/${api}/_data"
bckCommand="mysqldump --single-transaction --routines --events --add-drop-database --add-drop-table --add-drop-trigger --databases $db"
containerCommand="$bckCommand | xz > ${containerDir}/${bckFile}"

cd $bckDir || exit 1

if podman exec -it $api bash -c "$containerCommand"; then
    mv ${containerDirOnHost}/${bckFile} $bckDir 
else
    echo "$api: backup of database $db failed."
    exit 1
fi

chmod 400 ${bckDir}/${bckFile}

# Delete backups older than 30 days.
find $bckDir -name "${db}_${api}_*" -mtime +30 -exec rm -f {} \;

