#!/bin/bash
set -e

HELP="usage: $0 -o [The commit of the old schema version] (mandatory)\\n
-n [Commit or branch at which make the update] (mandatory)\\n
-d [dev-setup directory] (mandatory)\\n
-r [git repository directory] (mandatory)\\n
-w [workdir] (default: /tmp)\\n
[-h] this help
\\n"

while getopts "o:n:d:r:w:vh" opt
     do
        case $opt in
                o  ) oldCommit=$OPTARG ;;
                n  ) newCommit=$OPTARG ;;
                d  ) devSetupDir=$OPTARG ;;
                r  ) repoDir=$OPTARG ;;
                w  ) workDir=$OPTARG ;;
                v  ) vmDbSetup="y" ;;
                h  ) echo -e ${HELP}; exit 0 ;;
                *  ) echo -e ${HELP}; exit 0
              exit 0
        esac
done
shift $(($OPTIND - 1))

if [ -z "$oldCommit" ] || [ -z "$newCommit" ] || [ -z "$devSetupDir" ] || [ -z "$repoDir" ]; then
    echo "Argument missing."
    echo
    echo -e ${HELP}
    exit 1
fi

if [ -z "$workDir" ]; then
    workDir=/tmp
fi

# db schema file in the git repo.
sqlSchemaFile=f5/sql/f5.schema.sql
# db data file in the git repo.
sqlDataFile=f5/sql/f5.data.sql
# Tables that need data update.
updateTables='privilege role_privilege role'

sqlFileOld=${workDir}/f5_old.sql
sqlFileNew=${workDir}/f5_new.sql

dbUser=migrator
dbPassword=`uuidgen -r | tr -d '-' | head -c 12`
hostIp=10.0.111.204

# Outputfile for schema update
sqlSchemaScript=${workDir}/dbSchema_update.sql
# Outputfile for data update
sqlDataScript=${workDir}/dbData_update.sql

dbVM_prepare() {
    devSetup="$1"
    dbUser=$2
    dbPwd=$3

    cd $devSetup
    vagrant up deb12

    vagrant ssh deb12 -c "sudo apt install mariadb"
    vagrant ssh deb12 -c "sudo sed -i -r 's/bind-address([ \t]+)=/# bind-address\1=/g' mariadb.conf.d/50-server.cnf"
    vagrant ssh deb12 -c "sudo systemctl restart mariadb"

    vagrant ssh deb12 -c "sudo mysql -e \"grant all privileges on *.* to '$dbUser'@'%' identified by '$dbPwd';\""
    cd -
}

dbVM_passwd() {
    devSetup="$1"
    dbUser=$2
    dbPwd=$3

    cd $devSetup
    vagrant ssh deb12 -c "sudo mysql -e \"grant all privileges on *.* to '$dbUser'@'%' identified by '$dbPwd';\""
    cd -
}

###############################################
if ! which mysql-schema-diff > /dev/null; then
    apt install libmysql-diff-perl
fi

if [ "$vmDbSetup" == "y" ]; then
    dbVM_prepare $devSetupDir $dbUser $dbPassword
else
    dbVM_passwd $devSetupDir $dbUser $dbPassword
fi

cd $repoDir
git checkout $oldCommit
cp $sqlSchemaFile $sqlFileOld

git checkout $newCommit
cp $sqlSchemaFile $sqlFileNew

mysql-schema-diff --user=$dbUser --password=$dbPassword --host=$hostIp $sqlFileOld $sqlFileNew > $sqlSchemaScript


echo "set foreign_key_checks = 0;" > $sqlDataScript
echo -e '\n' >> $sqlDataScript
for table in $updateTables; do
    echo "truncate table $table;" >> $sqlDataScript
done

echo -e '\n' >> $sqlDataScript

for table in $updateTables; do
    sed -r -n "/INSERT INTO \`${table}\`/,/.*\);/p" $sqlDataFile >> $sqlDataScript
    echo >> $sqlDataScript
done

echo  >> $sqlDataScript

echo "set foreign_key_checks = 1;" >> $sqlDataScript


