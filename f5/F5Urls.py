import os
import importlib
from django.urls import path

from .controllers import Root, RawTxtController
from .controllers.F5.ltm import PoolMemberStats, Datagroup, VirtualServers, Irules, Monitors, SnatPool, Pool, Irule, \
    PoolMember, Profile, Policy, Nodes, Datagroups, Monitor, PoolMembers, VirtualServer, Pools, SnatPools, Node, \
    Profiles, Policies
from .controllers.F5.auth import Partitions
from .controllers.F5.net import RouteDomains, Vlan, Vlans, Self, Selfs, Interface, Interfaces
from .controllers.F5.sys import Certificate, Certificates, Folder, Folders
from .controllers.F5.asm import Policies as ASMPolicies, Policy as ASMPolicy, PoliciesDifference as ASMPolicyDifference, PolicyMerge as ASMPolicyMerge, PolicyApply as ASMPolicyApply
from .controllers.Asset import Asset, Assets
from .controllers.Permission import Authorizations, IdentityGroups, IdentityGroup, Roles, Permission, Permissions, AuthorizationsWorkflow, Workflows, PermissionsWorkflow, PermissionWorkflow
from .controllers.Configuration import Configurations, Configuration
from .controllers.History import History, ActionHistory
from .controllers.Helpers import Locks
from .helpers.Log import Log


urlpatterns = [
    path('', Root.RootController.as_view()),

    path('identity-groups/', IdentityGroups.PermissionIdentityGroupsController.as_view(), name='permission-identity-groups'),
    path('identity-group/<str:identityGroupIdentifier>/', IdentityGroup.PermissionIdentityGroupController.as_view(), name='permission-identity-group'),
    path('roles/', Roles.PermissionRolesController.as_view(), name='permission-roles'),
    path('permissions/', Permissions.PermissionsController.as_view(), name='permissions'),
    path('permission/<int:permissionId>/', Permission.PermissionController.as_view(), name='permission'),

    path('workflows/', Workflows.WorkflowsController.as_view(), name='workflows'),
    path('permissions-workflow/', PermissionsWorkflow.PermissionsWorkflowController.as_view(), name='permissions-workflow'),
    path('permission-workflow/<int:permissionId>/', PermissionWorkflow.PermissionWorkflowController.as_view(), name='permission-workflow'),

    path('authorizations/', Authorizations.AuthorizationsController.as_view(), name='authorizations'),
    path('workflow-authorizations/', AuthorizationsWorkflow.AuthorizationsWorkflowController.as_view(), name='workflow-authorizations'),

    path('doc/<str:fileName>/', RawTxtController.F5RawTxtController.as_view(), name='txt'),

    path('configurations/', Configurations.ConfigurationsController.as_view(), name='configuration'),
    path('configuration/<int:configId>/', Configuration.ConfigurationController.as_view(), name='configuration'),

    # Asset.
    path('assets/', Assets.F5AssetsController.as_view(), name='f5-assets'),
    path('asset/<int:assetId>/', Asset.F5AssetController.as_view(), name='f5-asset'),

    # Partition.
    path('<int:assetId>/partitions/', Partitions.F5PartitionsController.as_view(), name='f5-partitions'),

    # Folder.
    path('<int:assetId>/<str:partitionName>/folders/', Folders.F5FoldersController.as_view(), name='f5-folders'),
    path('<int:assetId>/<str:partitionName>/folder/<str:folderName>/', Folder.F5FolderController.as_view(), name='f5-folder'),

    # Root domain.
    path('<int:assetId>/routedomains/', RouteDomains.F5RouteDomainsController.as_view(), name='f5-route-domains'),

    # Interface.
    path('<int:assetId>/interfaces/', Interfaces.F5InterfacesController.as_view(), name='f5-interfaces'),
    path('<int:assetId>/interface/<str:interfaceName>/', Interface.F5InterfaceController.as_view(), name='f5-interface'),

    # Vlan.
    path('<int:assetId>/vlans/', Vlans.F5VlansController.as_view(), name='f5-vlans'),
    path('<int:assetId>/vlan/<str:vlanName>/', Vlan.F5VlanController.as_view(), name='f5-vlan'),

    # Self IP.
    path('<int:assetId>/selfs/', Selfs.F5SelfsController.as_view(), name='f5-selfs'),
    path('<int:assetId>/self/<str:selfName>/', Self.F5SelfController.as_view(), name='f5-self'),

    # ASM endpoints.
    path('<int:assetId>/asm/policies/', ASMPolicies.F5ASMMPoliciesController.as_view(), name='f5-asm-policies'),
    path('<int:assetId>/asm/policy/<str:policyId>/', ASMPolicy.F5PolicyController.as_view(), name='f5-asm-policy'),
    path('<int:assetId>/asm/policy/<str:policyId>/apply/', ASMPolicyApply.F5PolicyApplyController.as_view(), name='f5-asm-policy-apply'),

    path('source-asset/<int:sourceAssetId>/destination-asset/<int:destinationAssetId>/asm/source-policy/<str:sourcePolicyId>/destination-policy/<str:destinationPolicyId>/differences/', ASMPolicyDifference.F5ASMPoliciesDifferenceController.as_view(), name='f5-asm-policy-differences'),
    path('<int:assetId>/asm/policy/<str:destinationPolicyId>/merge/', ASMPolicyMerge.F5ASMPoliciesMergeController.as_view(), name='f5-asm-policy-merge'),

    # Datagroup.
    path('<int:assetId>/<str:partitionName>/datagroup/<str:datagroupType>/<str:datagroupName>/', Datagroup.F5DatagroupController.as_view(), name='f5-datagroup'),
    path('<int:assetId>/<str:partitionName>/datagroups/<str:datagroupType>/', Datagroups.F5DatagroupsController.as_view(), name='f5-datagroups'),
    path('<int:assetId>/<str:partitionName>/datagroups/', Datagroups.F5DatagroupsController.as_view(), name='f5-datagroup-types'),

    # Node.
    path('<int:assetId>/<str:partitionName>/node/<str:nodeName>/', Node.F5NodeController.as_view(), name='f5-node'),
    path('<int:assetId>/<str:partitionName>/nodes/', Nodes.F5NodesController.as_view(), name='f5-nodes'),

    # Monitor.
    path('<int:assetId>/<str:partitionName>/monitor/<str:monitorType>/<str:monitorName>/', Monitor.F5MonitorController.as_view(), name='f5-monitor'),
    path('<int:assetId>/<str:partitionName>/monitors/<str:monitorType>/', Monitors.F5MonitorsController.as_view(), name='f5-monitors'),
    path('<int:assetId>/<str:partitionName>/monitors/', Monitors.F5MonitorsController.as_view(), name='f5-monitor-types'),

    # Pool.
    path('<int:assetId>/<str:partitionName>/pool/<str:poolName>/', Pool.F5PoolController.as_view(), name='f5-pool'),
    path('<int:assetId>/<str:partitionName>/pools/', Pools.F5PoolsController.as_view(), name='f5-pools'),

    # SNAT pool.
    path('<int:assetId>/<str:partitionName>/snatpool/<str:snatPoolName>/', SnatPool.F5SnatPoolController.as_view(), name='f5-snatpool'),
    path('<int:assetId>/<str:partitionName>/snatpools/', SnatPools.F5SnatPoolsController.as_view(), name='f5-snatpools'),

    # Pool member.
    path('<int:assetId>/<str:partitionName>/pool/<str:poolName>/member/<str:poolMemberName>/', PoolMember.F5PoolMemberController.as_view(), name='f5-pool-member'),
    path('<int:assetId>/<str:partitionName>/pool/<str:poolName>/member/<str:poolMemberName>/stats/', PoolMemberStats.F5PoolMemberStatsController.as_view(), name='f5-pool-member-stats'),
    path('<int:assetId>/<str:partitionName>/pool/<str:poolName>/members/', PoolMembers.F5PoolMembersController.as_view(), name='f5-pool-members'),

    # Profile.
    path('<int:assetId>/<str:partitionName>/profiles/<str:profileType>/', Profiles.F5ProfilesController.as_view(), name='f5-profiles'),
    path('<int:assetId>/<str:partitionName>/profiles/', Profiles.F5ProfilesController.as_view(), name='f5-profile-types'),
    path('<int:assetId>/<str:partitionName>/profile/<str:profileType>/<str:profileName>/', Profile.F5ProfileController.as_view(), name='f5-profile'),

    # Policy.
    path('<int:assetId>/<str:partitionName>/policies/', Policies.F5PoliciesController.as_view(), name='f5-policies'),
    path('<int:assetId>/<str:partitionName>/policy/<str:policyName>/', Policy.F5PolicyController.as_view(), name='f5-policy'),

    # iRule.
    path('<int:assetId>/<str:partitionName>/irule/<str:iruleName>/', Irule.F5IruleController.as_view(), name='f5-irule'),
    path('<int:assetId>/<str:partitionName>/irules/', Irules.F5IrulesController.as_view(), name='f5-irules'),

    # Virtual server.
    path('<int:assetId>/<str:partitionName>/virtualserver/<str:virtualServerName>/', VirtualServer.F5VirtualServerController.as_view(), name='f5-virtualserver'),
    path('<int:assetId>/<str:partitionName>/virtualservers/', VirtualServers.F5VirtualServersController.as_view(), name='f5-virtualservers'),

    # Certificate/key.
    path('<int:assetId>/<str:partitionName>/certificate/<str:resourceName>/', Certificate.F5CertificateController.as_view(), name='f5-certificate'),
    path('<int:assetId>/<str:partitionName>/certificates/', Certificates.F5CertificatesController.as_view(), name='f5-certificates'),
    path('<int:assetId>/<str:partitionName>/key/<str:resourceName>/', Certificate.F5CertificateController.as_view(), name='f5-key'),
    path('<int:assetId>/<str:partitionName>/keys/', Certificates.F5CertificatesController.as_view(), name='f5-keys'),

    # Locks
    path('locks/', Locks.F5WorkflowLocksController.as_view(), name='f5-workflow-locks'),

    # History.
    path('history/', History.HistoryLogsController.as_view(), name='f5-log-history'),
    path('action-history/', ActionHistory.ActionHistoryLogsController.as_view(), name='f5-log-action-history'),
]

# Add usecases urls.
try:
    modules = os.listdir(os.path.dirname("/var/www/api/f5/urlsUsecases/"))
except Exception:
    modules = []

for fileModule in modules:
    try:
        if fileModule == '__init__.py' or fileModule[-3:] != '.py':
            continue

        try:
            module = importlib.import_module("f5.urlsUsecases." + fileModule[:-3], package=None)
        except Exception as e:
            Log.log("Error when importing module from file " + fileModule + str(e))
            raise e

        # Replace.
        try:
            replaceUrlpatterns = getattr(module, 'replaceUrlpatterns')
            if replaceUrlpatterns:
                for path in reversed(urlpatterns):
                    for replacePath in replaceUrlpatterns:
                        if path.pattern._route == replacePath.pattern._route: # call another controller.
                            urlpatterns.remove(path)
                            urlpatterns.append(replacePath)

        except Exception:
            pass

        # Add.
        usecaseUrlpatterns = getattr(module, 'urlpatterns')
        urlpatterns.extend(usecaseUrlpatterns)

    except Exception:
        pass
