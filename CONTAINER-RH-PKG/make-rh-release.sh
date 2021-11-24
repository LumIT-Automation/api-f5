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
    if [ "$ACTION" == "rpm" ]; then
        if System_checkEnvironment; then
            cd CONTAINER-RH-PKG
            if ! which rpm > /dev/null; then
                echo "rpm not found, try: apt install rpm"
                exit 1
            fi

            System_definitions
            System_cleanup

            System_serviceDebCreate
            System_systemFilesSetup

            System_redhatFilesSetup
            System_rpmCreate
            System_cleanup

            echo "Created /tmp/$rpmPackage"
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

    if [ -f ../CONTAINER-DEBIAN-PKG/DEBIAN-PKG/deb.release ]; then
        # Get program version from the release file.
        debPackageRelease=$(echo $(cat ../CONTAINER-DEBIAN-PKG/DEBIAN-PKG/deb.release))
        rpmPackageVer=$(awk -F'-' '{print $1}' ../CONTAINER-DEBIAN-PKG/DEBIAN-PKG/deb.release)
        rpmPackageRel=$(awk -F'-' '{print $2}' ../CONTAINER-DEBIAN-PKG/DEBIAN-PKG/deb.release)
    else
        echo "Error: deb.release missing."
        echo "Usage: bash CONTAINER-RH-PKG/make-release.sh --action rpm"
        exit 1
    fi
   
    shortName="api-f5"
    debArch="amd64"
    rpmArch="x86_64"

    serviceName="automation-interface-api"
    containerName="automation-interface-${shortName}-container"
    serviceProjectName="${serviceName}_${debPackageRelease}_${debArch}"
    serviceProjectPackage="${workingFolder}/${serviceProjectName}.deb" # inner .deb to be containerized.

    projectName="${containerName}_${debPackageRelease}_${rpmArch}"
    workingFolderPath="${workingFolder}/${containerName}-${rpmPackageVer}"

    rpmPackage=${containerName}-${rpmPackageVer}-${rpmPackageRel}.${rpmArch}.rpm
    mainSpec=${containerName}.spec
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
    cd  ../CONTAINER-DEBIAN-PKG
    bash DEBIAN-PKG/make-release.sh --action deb
    cd -
}


function System_systemFilesSetup()
{
    # Setting up system files.
    mkdir "$workingFolderPath"

    cp -R ../CONTAINER-DEBIAN-PKG/usr $workingFolderPath
    cp -R ../CONTAINER-DEBIAN-PKG/etc $workingFolderPath
    cp -R ../CONTAINER-DEBIAN-PKG/var $workingFolderPath

    # Cleanup.
    rm -f $workingFolderPath/var/log/automation/${shortName}/placeholder

    mv $serviceProjectPackage $workingFolderPath/usr/lib/${shortName}
    sed -i "s/PACKAGE/${serviceProjectName}.deb/g" $workingFolderPath/usr/lib/${shortName}/Dockerfile

    find "$workingFolderPath" -type d -exec chmod 0755 {} \;
    find "$workingFolderPath" -type f -exec chmod 0644 {} \;

    chmod +x ${workingFolderPath}/usr/bin/${shortName}-container.sh
    chmod +x ${workingFolderPath}/usr/lib/${shortName}/bootstrap.sh
}


function System_debCreate()
{
    cd $workingFolder
    dpkg-deb --build $projectName
}


function System_redhatFilesSetup()
{
    # Create the rpmbuild tree in $workingFolder.
    # The path must be passed to rpmbuild with the --define "_topdir <path>" option
    rpmDirs="RPMS BUILD SOURCES SPECS SRPMS BUILDROOT/${containerName}-${rpmPackageVer}-${rpmPackageRel}.x86_64"
    for dir in $rpmDirs; do
        mkdir -p "${workingFolder}/rpmbuild/$dir"
    done

    # Copy spec files to build the rpm package.
    cp REDHAT/*.spec ${workingFolder}/rpmbuild/SPECS

    # Set version, release, source tar in the main spec file. 
    sed -i "s/RH_VERSION/$rpmPackageVer/g" ${workingFolder}/rpmbuild/SPECS/${mainSpec}
    sed -i "s/RH_RELEASE/$rpmPackageRel/g" ${workingFolder}/rpmbuild/SPECS/${mainSpec}
    sed -i "s/RPM_SOURCE/${containerName}.tar/g" ${workingFolder}/rpmbuild/SPECS/${mainSpec}

    # Create the source tar file for the rpm.
    cd $workingFolder
    tar pcf ${containerName}.tar ${containerName}-${rpmPackageVer}
    mv ${containerName}.tar ${workingFolder}/rpmbuild/SOURCES
    cd -

    # Build the file specs section. List files only, not directories.
    echo "%files" > ${workingFolder}/rpmbuild/SPECS/files.spec
    tar tf ${workingFolder}/rpmbuild/SOURCES/${containerName}.tar | grep -Ev '/$' | sed "s#${containerName}-${rpmPackageVer}##g" >> ${workingFolder}/rpmbuild/SPECS/files.spec
}


function System_rpmCreate()
{
    rpmbuild --define "_topdir ${workingFolder}/rpmbuild" -ba ${workingFolder}/rpmbuild/SPECS/${mainSpec}
    mv ${workingFolder}/rpmbuild/RPMS/${rpmArch}/${rpmPackage} /tmp
    rm -fr ${workingFolder}/rpmbuild
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
    echo "Missing parameters. Use --action rpm."
else
    System "system"
    $system_run
fi

exit 0
