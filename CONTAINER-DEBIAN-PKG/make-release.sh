#!/bin/bash

set -e

function System()
{
    base=$FUNCNAME
    this=$1

    # Declare methods.
    for method in $(compgen -A function)
    do
        export ${method/#$base\_/$this\_}="${method} ${this}"
    done

    # Properties list.
    ACTION="$ACTION"
}

# ##################################################################################################################################################
# Public
# ##################################################################################################################################################

#
# Void System_run().
#
function System_run()
{
    if [ "$ACTION" == "deb" ]; then
        if System_checkEnvironment; then
            cd CONTAINER-DEBIAN-PKG

            System_definitions
            System_cleanup

            System_serviceDebCreate

            System_systemFilesSetup
            System_debianFilesSetup
            System_debCreate
            System_cleanup

            echo "Created /tmp/$projectName.deb"
        else
            echo "A Debian Buster operating system is required for the deb-ification. Aborting."
            exit 1
        fi
    else
        exit 1
    fi
}

# ##################################################################################################################################################
# Private static
# ##################################################################################################################################################

function System_checkEnvironment()
{
    if [ -f /etc/os-release ]; then
        if ! grep -q 'Debian GNU/Linux 10 (buster)' /etc/os-release; then
            return 1
        fi
    else
        return 1
    fi

    return 0
}


function System_definitions()
{
    declare -g debPackageRelease

    declare -g projectName
    declare -g workingFolder
    declare -g workingFolderPath

    workingFolder="/tmp"

    if [ -f DEBIAN-PKG/deb.release ]; then
        # Get program version from the release file.
        debPackageRelease=$(echo $(cat DEBIAN-PKG/deb.release))
    else
        echo "Error: deb.release missing."
        echo "Usage: bash CONTAINER-DEBIAN-PKG/make-release.sh --action deb"
        exit 1
    fi

    shortName="api-f5"
    debArch="amd64"

    serviceName="automation-interface-api"
    containerName="automation-interface-${shortName}-container"
    serviceProjectName="${serviceName}_${debPackageRelease}_${debArch}"
    serviceProjectPackage="${workingFolder}/${serviceProjectName}.deb" # inner .deb to be containerized.

    projectName="${containerName}_${debPackageRelease}_${debArch}"
    workingFolderPath="${workingFolder}/${projectName}"
}


function System_cleanup()
{
    # List of the directories to be deleted.
    rmDirs="$workingFolderPath ${workingFolder}/${containerName} ${workingFolder}/${serviceProjectName} ${workingFolder}/${projectName}"
    for dir in $rmDirs; do
        if [ -d "$dir" ]; then
            rm -fR "$dir"
        fi
    done
}


function System_serviceDebCreate()
{
    bash DEBIAN-PKG/make-release.sh --action deb
}


function System_systemFilesSetup()
{
    # Setting up system files.
    mkdir "$workingFolderPath"

    cp -R home $workingFolderPath
    cp -R usr $workingFolderPath
    cp -R etc $workingFolderPath
    cp -R var $workingFolderPath

    # Cleanup.
    rm -f $workingFolderPath/var/log/automation/${shortName}/placeholder

    mv $serviceProjectPackage $workingFolderPath/usr/lib/${shortName}
    sed -i "s/PACKAGE/${serviceProjectName}.deb/g" $workingFolderPath/usr/lib/${shortName}/Dockerfile

    find "$workingFolderPath" -type d -exec chmod 0755 {} \;
    find "$workingFolderPath" -type f -exec chmod 0644 {} \;

    chmod +x $workingFolderPath/usr/bin/bck-db_${shortName}.sh
    chmod +x $workingFolderPath/usr/bin/${shortName}-container.sh
    chmod +x $workingFolderPath/usr/lib/${shortName}/bootstrap.sh
}


function System_debianFilesSetup()
{
    # Setting up all the files needed to build the package (DEBIAN folder).
    cp -R DEBIAN $workingFolderPath

    sed -i "s/^Version:.*/Version:\ $debPackageRelease/g" $workingFolderPath/DEBIAN/control

    chmod +x $workingFolderPath/DEBIAN/preinst
    chmod +x $workingFolderPath/DEBIAN/postinst
    chmod +x $workingFolderPath/DEBIAN/prerm
    chmod +x $workingFolderPath/DEBIAN/postrm
}


function System_debCreate()
{
    cd $workingFolder
    dpkg-deb --build $projectName
}

# ##################################################################################################################################################
# Main
# ##################################################################################################################################################

ACTION=""

# Must be run as root.
ID=$(id -u)
if [ $ID -ne 0 ]; then
    echo "This script needs super cow powers."
    exit 1
fi

# Parse user input.
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --action)
            ACTION="$2"
            shift
            shift
            ;;

        *)
            shift
            ;;
    esac
done

if [ -z "$ACTION" ]; then
    echo "Missing parameters. Use --action deb."
else
    System "system"
    $system_run
fi

exit 0
