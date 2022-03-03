-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Mag 06, 2021 alle 16:58
-- Versione del server: 10.3.27-MariaDB-0+deb10u1-log
-- Versione PHP: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `api`
--

--
-- Dump dei dati per la tabella `configuration`
--

INSERT INTO `configuration` (`id`, `config_type`, `configuration`) VALUES
(1, 'global', '{\"config\": {}}');


--
-- Dump dei dati per la tabella `privilege`
--

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
(63, 'datagroup_get', 'object', NULL);

--
-- Dump dei dati per la tabella `role`
--

INSERT INTO `role` (`id`, `role`, `description`) VALUES
(1, 'admin', 'admin'),
(2, 'staff', 'read / write, excluding assets'),
(3, 'readonly', 'readonly');

--
-- Dump dei dati per la tabella `role_privilege`
--

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
(2, 3),
(2, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(2, 16),
(2, 18),
(2, 19),
(2, 20),
(2, 21),
(2, 22),
(2, 23),
(2, 24),
(2, 25),
(2, 26),
(2, 27),
(2, 28),
(2, 29),
(2, 30),
(2, 31),
(2, 32),
(2, 33),
(2, 34),
(2, 35),
(2, 36),
(2, 37),
(2, 38),
(2, 39),
(2, 40),
(2, 41),
(2, 42),
(2, 43),
(2, 44),
(2, 46),
(2, 47),
(2, 48),
(2, 49),
(2, 50),
(2, 51),
(2, 52),
(2, 53),
(2, 54),
(2, 55),
(2, 56),
(2, 57),
(2, 59),
(2, 60),
(2, 61),
(2, 62),
(2, 63),
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
(3, 63);


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;