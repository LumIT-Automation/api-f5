#!/bin/bash
set -e

HELP="usage: $0 -o [The commit of the old schema version] (mandatory)\\n
-n [Commit or branch at which make the update] (mandatory)\\n
-d [dev-setup directory] (mandatory)\\n
-r [git repository directory]\\n
-v [prepare VM for db comparison]\\n
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

if [ -z "$oldCommit" ] || [ -z "$newCommit" ] || [ -z "$devSetupDir" ]; then
    echo "Argument missing."
    echo
    echo -e ${HELP}
    exit 1
fi

if [ -z "$workDir" ]; then
    workDir=/tmp
fi

if [ -z "$repoDir" ]; then
    repoDir=$(cd `dirname $0`/../.. && pwd)
    if [ ! -f ${repoDir}/.git/config ]; then
        echo "\$repoDir: $repoDir is not a git repo, please use the -r option."
        exit 1
    fi
fi

api=f5
# db schema file in the git repo.
sqlSchemaFile=${api}/sql/${api}.schema.sql
# db data file in the git repo.
sqlDataFile=${api}/sql/${api}.data.sql
# Tables that need data update.
updateTables='privilege role_privilege role'

sqlFileOld=${workDir}/${api}_old.sql
sqlFileNew=${workDir}/${api}_new.sql

dbUser=api
dbPassword=password
hostIp=$(grep -oP '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' $devSetupDir/vagrantfile-api-${api})

yellow='\033[0;33m'
nc='\033[0m' # no color.

dbVM_prepare() {
    devSetup="$1"

    cd $devSetup
    vagrant up api${api}

}

###############################################
if ! which mysql-schema-diff > /dev/null; then
    apt install libmysql-diff-perl
fi

if [ "$vmDbSetup" == "y" ]; then
    dbVM_prepare $devSetupDir
fi

cd $repoDir
git checkout $oldCommit
oldCommit=$(git log -1 --pretty=%H) # Get the full hash.
oldCommitShort=$(git rev-parse --short=11 $oldCommit)
cp $sqlSchemaFile $sqlFileOld

git checkout $newCommit
newCommit=$(git log -1 --pretty=%H) # Get the full hash.
newCommitShort=$(git rev-parse --short=11 $newCommit)
cp $sqlSchemaFile $sqlFileNew

outputSqlScript=${workDir}/dbUpdate_${api}_${oldCommitShort}-${newCommitShort}.sql

echo -e "\n/*\nOLD COMMIT: $oldCommit\nNEW COMMIT: $newCommit\n*/\n\n" > $outputSqlScript
echo -e "/*\nSQL SCHEMA SECTION\n*/\n" >> $outputSqlScript

mysql-schema-diff --user=$dbUser --password=$dbPassword --host=$hostIp $sqlFileOld $sqlFileNew >> $outputSqlScript

if grep -Ei 'DROP\s+TABLE' $outputSqlScript || grep -Ei 'DROP\s+COLUMN' $outputSqlScript; then
    echo -e "\n${yellow}WARNING: DROP TABLE or DROP COLUMN command found in script $outputSqlScript"
    echo -e "Possible data drop, check if a RENAME TABLE + ALTER TABLE is a better choice.${nc}"
fi


echo -e "\n\n/*\nDATA SECTION\n*/\n" >> $outputSqlScript
echo "set foreign_key_checks = 0;" >> $outputSqlScript
echo -e '\n' >> $outputSqlScript
for table in $updateTables; do
    echo "truncate table $table;" >> $outputSqlScript
done

echo -e '\n' >> $outputSqlScript

for table in $updateTables; do
    sed -r -n "/INSERT INTO \`${table}\`/,/.*\);/p" $sqlDataFile >> $outputSqlScript
    echo >> $outputSqlScript
done

echo  >> $outputSqlScript

echo "set foreign_key_checks = 1;" >> $outputSqlScript

echo -e "\nOuput script: $outputSqlScript"

