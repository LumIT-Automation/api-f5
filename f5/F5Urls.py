from django.urls import path

from .controllers import Root
from .controllers.F5 import Partitions, Node, Nodes, Monitor, Monitors, Certificate, Certificates, Pools, Pool, SnatPool, SnatPools, PoolMembers, PoolMember, PoolMemberStats, Profile, Profiles, VirtualServer, VirtualServers
from .controllers.F5.Asset import Asset, Assets
from .controllers.F5.Workflow import VirtualServersController as WorkflowVirtualServers, VirtualServerController as WorkflowVirtualServer
from .controllers.Permission import Authorizations, IdentityGroups, IdentityGroup, Roles, Permission, Permissions
from .controllers import History


urlpatterns = [
    path('', Root.RootController.as_view()),

    path('identity-groups/', IdentityGroups.PermissionIdentityGroupsController.as_view(), name='permission-identity-groups'),
    path('identity-group/<str:identityGroupIdentifier>/', IdentityGroup.PermissionIdentityGroupController.as_view(), name='permission-identity-group'),
    path('roles/', Roles.PermissionRolesController.as_view(), name='permission-roles'),
    path('permissions/', Permissions.PermissionsController.as_view(), name='permissions'),
    path('permission/<int:permissionId>/', Permission.PermissionController.as_view(), name='permission'),

    path('authorizations/', Authorizations.AuthorizationsController.as_view(), name='authorizations'),

    # Asset.
    path('assets/', Assets.F5AssetsController.as_view(), name='f5-assets'),
    path('asset/<int:assetId>/', Asset.F5AssetController.as_view(), name='f5-asset'),

    # Partition.
    path('<int:assetId>/partitions/', Partitions.F5PartitionsController.as_view(), name='f5-partitions'),

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
    path('<int:assetId>/<str:partitionName>/profiles/<str:profileType>/<str:profileName>/', Profile.F5ProfileController.as_view(), name='f5-profile'),
    path('<int:assetId>/<str:partitionName>/profiles/<str:profileType>/', Profiles.F5ProfilesController.as_view(), name='f5-profiles'),
    path('<int:assetId>/<str:partitionName>/profiles/', Profiles.F5ProfilesController.as_view(), name='f5-profile-types'),

    # Virtual server.
    path('<int:assetId>/<str:partitionName>/virtualserver/<str:virtualServerName>/', VirtualServer.F5VirtualServerController.as_view(), name='f5-virtualserver'),
    path('<int:assetId>/<str:partitionName>/virtualservers/', VirtualServers.F5VirtualServersController.as_view(), name='f5-virtualservers'),

    # Certificate/key.
    path('<int:assetId>/<str:partitionName>/certificate/<str:resourceName>/', Certificate.F5CertificateController.as_view(), name='f5-certificate'),
    path('<int:assetId>/certificates/', Certificates.F5CertificatesController.as_view(), name='f5-certificates'), # not a broken-by-design feature: we need all partitions' certificates :)
    path('<int:assetId>/<str:partitionName>/key/<str:resourceName>/', Certificate.F5CertificateController.as_view(), name='f5-key'),
    path('<int:assetId>/keys/', Certificates.F5CertificatesController.as_view(), name='f5-keys'),

    # Workflows.
    # Virtual server.
    path('<int:assetId>/<str:partitionName>/workflow/virtualservers/<str:virtualServerName>/', WorkflowVirtualServer.F5WorkflowVirtualServerController.as_view(), name='f5-workflow-virtualserver'),
    path('<int:assetId>/<str:partitionName>/workflow/virtualservers/', WorkflowVirtualServers.F5WorkflowVirtualServersController.as_view(), name='f5-workflow-virtualservers'),

    # Log history.
    path('history/', History.HistoryLogsController.as_view(), name='f5-log-history'),
]
