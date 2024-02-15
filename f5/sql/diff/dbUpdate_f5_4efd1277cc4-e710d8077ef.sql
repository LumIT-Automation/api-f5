
/*
OLD COMMIT: 4efd1277cc4ccc75566f0361b74bcdac6c8afe00
NEW COMMIT: e710d8077ef5697e89beaa007c2add4a50a220db
*/


/*
SQL SCHEMA SECTION
*/

## mysqldiff 0.60
## 
## Run on Thu Feb 15 11:39:51 2024
## Options: host=10.0.111.22, user=api, password=password, debug=0
##
## --- file: /tmp/f5_old.sql
## +++ file: /tmp/f5_new.sql



ALTER TABLE asset CHANGE COLUMN baseurl baseurl varchar(255) NOT NULL DEFAULT ''; # was varchar(255) NOT NULL
ALTER TABLE asset CHANGE COLUMN fqdn fqdn varchar(255) NOT NULL; # was varchar(255) DEFAULT NULL
ALTER TABLE asset DROP INDEX address;
ALTER TABLE asset DROP COLUMN address; # was varchar(64) NOT NULL
ALTER TABLE asset ADD COLUMN protocol varchar(16) NOT NULL DEFAULT 'https' AFTER fqdn;
ALTER TABLE asset ADD COLUMN port int(11) NOT NULL DEFAULT 443 AFTER protocol;
ALTER TABLE asset ADD COLUMN path varchar(255) NOT NULL DEFAULT '/' AFTER port;
ALTER TABLE asset MODIFY `tlsverify` tinyint(4) NOT NULL DEFAULT 1 AFTER path;
ALTER TABLE asset MODIFY `datacenter` varchar(255) NOT NULL DEFAULT '';
ALTER TABLE asset MODIFY `environment` varchar(255) NOT NULL DEFAULT '';
ALTER TABLE asset MODIFY `position` varchar(255) NOT NULL DEFAULT '';

ALTER TABLE asset ADD UNIQUE fqdn (fqdn,protocol,port);
ALTER TABLE log ADD COLUMN dr_replica_flow varchar(255) DEFAULT '';

CREATE TABLE asset_assetdr (
  pr_asset_id int(11) NOT NULL,
  dr_asset_id int(11) NOT NULL,
  enabled tinyint(1) NOT NULL,
  PRIMARY KEY (pr_asset_id,dr_asset_id),
  KEY k_dr_asset_id (dr_asset_id),
  CONSTRAINT k_dr_asset_id FOREIGN KEY (dr_asset_id) REFERENCES asset (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT k_pr_asset_id FOREIGN KEY (pr_asset_id) REFERENCES asset (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE log_request (
  id int(11) NOT NULL AUTO_INCREMENT,
  asset_id int(11) DEFAULT NULL,
  action varchar(255) NOT NULL,
  response_status int(11) NOT NULL,
  date datetime NOT NULL DEFAULT current_timestamp(),
  username varchar(255) NOT NULL,
  PRIMARY KEY (id),
  KEY log_request_asset_id (asset_id),
  CONSTRAINT log_request_asset_id FOREIGN KEY (asset_id) REFERENCES asset (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



/*
DATA SECTION
*/

set foreign_key_checks = 0;


# Set the protocol from the original baseurl.
update asset A1 INNER JOIN asset A2 ON A1.id = A2.id set A1.protocol = SUBSTRING_INDEX(A2.baseurl,':',1);

# Set the path from the original baseurl.
update asset A1 INNER JOIN asset A2 ON A1.id = A2.id set A1.path = (select if(p0 REGEXP '.*/$', p0, concat(p0, '/') ) from (select REGEXP_REPLACE(A3.baseurl, '[a-zA-Z]+://[0-9a-zA-Z.-]+(:[0-9]+)?(/.*)', '\\2') as p0 from asset A3) as p1);

# Put an "/" at the end of the baseurl if missing.
update asset A1 INNER JOIN asset A2 ON A1.id = A2.id set A1.baseurl = ( select if(b0 REGEXP '.*/$', b0, concat(b0, '/') ) as b from (select A3.baseurl as b0 from asset A3) as a );



truncate table privilege;
truncate table role_privilege;
truncate table role;


INSERT INTO `privilege` (`id`, `privilege`, `privilege_type`, `description`) VALUES
(1, 'asset_patch', 'asset', NULL),
(2, 'asset_delete', 'asset', NULL),
(3, 'assets_get', 'asset', NULL),
(4, 'assets_post', 'asset', NULL),
(5, 'certificates_post', 'object', NULL),
(6, 'poolMember_get', 'object', NULL),
(7, 'poolMember_patch', 'object', NULL),
(8, 'poolMembers_get', 'object', NULL),
(9, 'poolMemberStats_get', 'object', NULL),
(10, 'pools_get', 'object', NULL),
(11, 'permission_identityGroups_get', 'global', NULL),
(12, 'permission_identityGroups_post', 'global', NULL),
(13, 'permission_roles_get', 'global', NULL),
(14, 'permission_identityGroup_patch', 'global', NULL),
(15, 'permission_identityGroup_delete', 'global', NULL),
(16, 'partitions_get', 'object', NULL),
(18, 'nodes_get', 'object', NULL),
(19, 'nodes_post', 'object', NULL),
(20, 'node_patch', 'object', NULL),
(21, 'node_delete', 'object', NULL),
(22, 'monitors_get', 'object', NULL),
(23, 'monitors_post', 'object', NULL),
(24, 'monitor_patch', 'object', NULL),
(25, 'monitor_delete', 'object', NULL),
(26, 'pools_post', 'object', NULL),
(27, 'pool_delete', 'object', NULL),
(28, 'pool_patch', 'object', NULL),
(29, 'poolMembers_post', 'object', NULL),
(30, 'poolMember_delete', 'object', NULL),
(31, 'virtualServers_get', 'object', NULL),
(32, 'virtualServers_post', 'object', NULL),
(33, 'virtualServer_patch', 'object', NULL),
(34, 'virtualServer_delete', 'object', NULL),
(35, 'virtualServer_get', 'object', NULL),
(36, 'profiles_get', 'object', NULL),
(37, 'workflow_virtualServers_post', 'object', NULL),
(38, 'profiles_post', 'object', NULL),
(39, 'profile_delete', 'object', NULL),
(40, 'profile_patch', 'object', NULL),
(41, 'snatPools_get', 'object', NULL),
(42, 'snatPools_post', 'object', NULL),
(43, 'snatPool_delete', 'object', NULL),
(44, 'snatPool_patch', 'object', NULL),
(45, 'historyComplete_get', 'global', NULL),
(46, 'workflow_virtualServers_delete', 'object', NULL),
(47, 'certificates_get', 'object', NULL),
(48, 'certificate_delete', 'object', NULL),
(49, 'policies_get', 'object', NULL),
(50, 'policies_post', 'object', NULL),
(51, 'policy_patch', 'object', NULL),
(52, 'policy_delete', 'object', NULL),
(53, 'irules_get', 'object', NULL),
(54, 'irules_post', 'object', NULL),
(55, 'irule_patch', 'object', NULL),
(56, 'irule_delete', 'object', NULL),
(57, 'routedomains_get', 'asset', NULL),
(58, 'configuration_put', 'global', NULL),
(59, 'datagroups_get', 'object', NULL),
(60, 'datagroups_post', 'object', NULL),
(61, 'datagroup_delete', 'object', NULL),
(62, 'datagroup_patch', 'object', NULL),
(63, 'datagroup_get', 'object', NULL),
(64, 'full_visibility', 'global', NULL),
(65, 'asm_policies_get', 'asset', NULL),
(66, 'asm_policy_get', 'asset', NULL),
(67, 'asm_policy_delete', 'asset', NULL),
(68, 'asm_policy_differences_get', 'global', NULL),
(69, 'asm_policy_merge_post', 'asset', NULL),
(70, 'asm_policy_apply_post', 'asset', NULL),
(71, 'workflow_node_delete', 'object', NULL),
(72, 'asset_get', 'asset', NULL);

INSERT INTO `role_privilege` (`id_role`, `id_privilege`) VALUES
(1, 3),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 25),
(1, 26),
(1, 27),
(1, 28),
(1, 29),
(1, 30),
(1, 31),
(1, 32),
(1, 33),
(1, 34),
(1, 35),
(1, 36),
(1, 37),
(1, 38),
(1, 39),
(1, 40),
(1, 41),
(1, 42),
(1, 43),
(1, 44),
(1, 45),
(1, 46),
(1, 47),
(1, 48),
(1, 49),
(1, 50),
(1, 51),
(1, 52),
(1, 53),
(1, 54),
(1, 55),
(1, 56),
(1, 57),
(1, 58),
(1, 59),
(1, 60),
(1, 61),
(1, 62),
(1, 63),
(1, 64),
(1, 65),
(1, 66),
(1, 67),
(1, 68),
(1, 69),
(1, 70),
(1, 71),
(1, 72),
(2, 3),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(2, 16),
(2, 30),
(2, 31),
(2, 37),
(2, 46),
(2, 57),
(2, 59),
(2, 71),
(2, 72),
(3, 3),
(3, 6),
(3, 8),
(3, 9),
(3, 10),
(3, 16),
(3, 18),
(3, 22),
(3, 31),
(3, 35),
(3, 36),
(3, 41),
(3, 47),
(3, 49),
(3, 53),
(3, 57),
(3, 59),
(3, 63),
(3, 72),
(4, 3),
(4, 72);

INSERT INTO `role` (`id`, `role`, `description`) VALUES
(1, 'admin', 'admin'),
(2, 'staff', 'read / write, excluding assets'),
(3, 'readonly', 'readonly'),
(4, 'workflow', 'workflow system user');


set foreign_key_checks = 1;
