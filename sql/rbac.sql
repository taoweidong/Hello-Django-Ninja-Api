/*
Navicat MySQL Data Transfer

Source Server         : 本地MySql
Source Server Version : 80032
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 80032
File Encoding         : 65001

Date: 2026-03-08 21:52:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for system_deptinfo
-- ----------------------------
DROP TABLE IF EXISTS `system_deptinfo`;
CREATE TABLE `system_deptinfo` (
  `mode_type` smallint NOT NULL,
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `name` varchar(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `rank` int NOT NULL,
  `auto_bind` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `parent_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `system_deptinfo_creator_id_6304526c_fk_system_userinfo_id` (`creator_id`),
  KEY `system_deptinfo_dept_belong_id_40eea2f6_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_deptinfo_modifier_id_eadcba8a_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_deptinfo_parent_id_86e73520_fk_system_deptinfo_id` (`parent_id`),
  CONSTRAINT `system_deptinfo_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_deptinfo_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_deptinfo_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_deptinfo_ibfk_4` FOREIGN KEY (`parent_id`) REFERENCES `system_deptinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `menu_type` smallint NOT NULL,
  `name` varchar(128) NOT NULL,
  `rank` int NOT NULL,
  `path` varchar(255) NOT NULL,
  `component` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `method` varchar(10) DEFAULT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `parent_id` char(32) DEFAULT NULL,
  `meta_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `meta_id` (`meta_id`),
  KEY `system_menu_creator_id_d58495af_fk_system_userinfo_id` (`creator_id`),
  KEY `system_menu_modifier_id_49b4db71_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_menu_parent_id_c715739f_fk_system_menu_id` (`parent_id`),
  CONSTRAINT `system_menu_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_menu_ibfk_3` FOREIGN KEY (`meta_id`) REFERENCES `system_menumeta` (`id`),
  CONSTRAINT `system_menu_ibfk_4` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_menu_ibfk_5` FOREIGN KEY (`parent_id`) REFERENCES `system_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_menumeta
-- ----------------------------
DROP TABLE IF EXISTS `system_menumeta`;
CREATE TABLE `system_menumeta` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `r_svg_name` varchar(255) DEFAULT NULL,
  `is_show_menu` tinyint(1) NOT NULL,
  `is_show_parent` tinyint(1) NOT NULL,
  `is_keepalive` tinyint(1) NOT NULL,
  `frame_url` varchar(255) DEFAULT NULL,
  `frame_loading` tinyint(1) NOT NULL,
  `transition_enter` varchar(255) DEFAULT NULL,
  `transition_leave` varchar(255) DEFAULT NULL,
  `is_hidden_tag` tinyint(1) NOT NULL,
  `fixed_tag` tinyint(1) NOT NULL,
  `dynamic_level` int NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_menumeta_creator_id_02956d64_fk_system_userinfo_id` (`creator_id`),
  KEY `system_menumeta_modifier_id_7bc4d182_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_menumeta_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_menumeta_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_operationlog
-- ----------------------------
DROP TABLE IF EXISTS `system_operationlog`;
CREATE TABLE `system_operationlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `module` varchar(64) DEFAULT NULL,
  `path` varchar(400) DEFAULT NULL,
  `body` longtext,
  `method` varchar(8) DEFAULT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `browser` varchar(64) DEFAULT NULL,
  `system` varchar(64) DEFAULT NULL,
  `response_code` int DEFAULT NULL,
  `response_result` longtext,
  `status_code` int DEFAULT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_operationlog_creator_id_75ee7a2c_fk_system_userinfo_id` (`creator_id`),
  KEY `system_operationlog_modifier_id_898ff5c3_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_operationlog_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_operationlog_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo`;
CREATE TABLE `system_userinfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `mode_type` smallint NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `nickname` varchar(150) NOT NULL,
  `gender` int NOT NULL,
  `phone` varchar(16) NOT NULL,
  `email` varchar(254) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `dept_id` char(32) DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `system_userinfo_dept_id_58621eca_fk_system_deptinfo_id` (`dept_id`),
  KEY `system_userinfo_dept_belong_id_3055ec74_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_userinfo_creator_id_300bf994_fk_system_userinfo_id` (`creator_id`),
  KEY `system_userinfo_modifier_id_439b401f_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_userinfo_phone_87b78cba` (`phone`),
  KEY `system_userinfo_email_bf1d19b4` (`email`),
  CONSTRAINT `system_userinfo_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_userinfo_ibfk_3` FOREIGN KEY (`dept_id`) REFERENCES `system_deptinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo_roles
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo_roles`;
CREATE TABLE `system_userinfo_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userinfo_id` bigint NOT NULL,
  `userrole_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userinfo_roles_userinfo_id_userrole_id_f613220a_uniq` (`userinfo_id`,`userrole_id`),
  KEY `system_userinfo_roles_userrole_id_19a0aa90_fk_system_userrole_id` (`userrole_id`),
  CONSTRAINT `system_userinfo_roles_ibfk_1` FOREIGN KEY (`userinfo_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userinfo_roles_ibfk_2` FOREIGN KEY (`userrole_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userrole
-- ----------------------------
DROP TABLE IF EXISTS `system_userrole`;
CREATE TABLE `system_userrole` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `name` varchar(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `system_userrole_creator_id_27e40be6_fk_system_userinfo_id` (`creator_id`),
  KEY `system_userrole_modifier_id_c682499b_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_userrole_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userrole_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userrole_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_userrole_menu`;
CREATE TABLE `system_userrole_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userrole_id` char(32) NOT NULL,
  `menu_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userrole_menu_userrole_id_menu_id_533db074_uniq` (`userrole_id`,`menu_id`),
  KEY `system_userrole_menu_menu_id_b6b2d65f_fk_system_menu_id` (`menu_id`),
  CONSTRAINT `system_userrole_menu_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`),
  CONSTRAINT `system_userrole_menu_ibfk_2` FOREIGN KEY (`userrole_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
