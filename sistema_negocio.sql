-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.4.3 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para sistema_negocio
CREATE DATABASE IF NOT EXISTS `sistema_negocio` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sistema_negocio`;

-- Volcando estructura para tabla sistema_negocio.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_group: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_permission: ~64 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add Cliente', 7, 'add_cliente'),
	(26, 'Can change Cliente', 7, 'change_cliente'),
	(27, 'Can delete Cliente', 7, 'delete_cliente'),
	(28, 'Can view Cliente', 7, 'view_cliente'),
	(29, 'Can add Conversación', 8, 'add_conversacion'),
	(30, 'Can change Conversación', 8, 'change_conversacion'),
	(31, 'Can delete Conversación', 8, 'delete_conversacion'),
	(32, 'Can view Conversación', 8, 'view_conversacion'),
	(33, 'Can add Mensaje', 9, 'add_mensaje'),
	(34, 'Can change Mensaje', 9, 'change_mensaje'),
	(35, 'Can delete Mensaje', 9, 'delete_mensaje'),
	(36, 'Can view Mensaje', 9, 'view_mensaje'),
	(37, 'Can add Categoría', 10, 'add_categoria'),
	(38, 'Can change Categoría', 10, 'change_categoria'),
	(39, 'Can delete Categoría', 10, 'delete_categoria'),
	(40, 'Can view Categoría', 10, 'view_categoria'),
	(41, 'Can add Producto', 11, 'add_producto'),
	(42, 'Can change Producto', 11, 'change_producto'),
	(43, 'Can delete Producto', 11, 'delete_producto'),
	(44, 'Can view Producto', 11, 'view_producto'),
	(45, 'Can add Proveedor', 12, 'add_proveedor'),
	(46, 'Can change Proveedor', 12, 'change_proveedor'),
	(47, 'Can delete Proveedor', 12, 'delete_proveedor'),
	(48, 'Can view Proveedor', 12, 'view_proveedor'),
	(49, 'Can add Variante de Producto', 13, 'add_productovariante'),
	(50, 'Can change Variante de Producto', 13, 'change_productovariante'),
	(51, 'Can delete Variante de Producto', 13, 'delete_productovariante'),
	(52, 'Can view Variante de Producto', 13, 'view_productovariante'),
	(53, 'Can add Detalle de iPhone', 14, 'add_detalleiphone'),
	(54, 'Can change Detalle de iPhone', 14, 'change_detalleiphone'),
	(55, 'Can delete Detalle de iPhone', 14, 'delete_detalleiphone'),
	(56, 'Can view Detalle de iPhone', 14, 'view_detalleiphone'),
	(57, 'Can add Precio', 15, 'add_precio'),
	(58, 'Can change Precio', 15, 'change_precio'),
	(59, 'Can delete Precio', 15, 'delete_precio'),
	(60, 'Can view Precio', 15, 'view_precio'),
	(61, 'Can add Registro de Historial', 16, 'add_registrohistorial'),
	(62, 'Can change Registro de Historial', 16, 'change_registrohistorial'),
	(63, 'Can delete Registro de Historial', 16, 'delete_registrohistorial'),
	(64, 'Can view Registro de Historial', 16, 'view_registrohistorial');

-- Volcando estructura para tabla sistema_negocio.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_user: ~1 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$600000$Aug4S1VCCpAva4vjvJtxir$B+dNpahdN40gH9WmT7VbSO3KytHeJvuRVW9P1vsmB+A=', '2025-11-03 01:06:37.277911', 1, 'esrsosa', '', '', 'emanuelsosa4436@gmail.com', 1, 1, '2025-11-03 01:05:46.221246');

-- Volcando estructura para tabla sistema_negocio.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.crm_cliente
CREATE TABLE IF NOT EXISTS `crm_cliente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_cliente` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `instagram_handle` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telefono` (`telefono`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.crm_cliente: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.crm_conversacion
CREATE TABLE IF NOT EXISTS `crm_conversacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fuente` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `resumen` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL,
  `asesor_asignado_id` int DEFAULT NULL,
  `cliente_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_conversacion_asesor_asignado_id_b38461f1_fk_auth_user_id` (`asesor_asignado_id`),
  KEY `crm_conversacion_cliente_id_6d9bafb1_fk_crm_cliente_id` (`cliente_id`),
  CONSTRAINT `crm_conversacion_asesor_asignado_id_b38461f1_fk_auth_user_id` FOREIGN KEY (`asesor_asignado_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `crm_conversacion_cliente_id_6d9bafb1_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.crm_conversacion: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.crm_mensaje
CREATE TABLE IF NOT EXISTS `crm_mensaje` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `emisor` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `contenido` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_envio` datetime(6) NOT NULL,
  `enviado_por_ia` tinyint(1) NOT NULL,
  `conversacion_id` bigint NOT NULL,
  `archivo` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_mensaje` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_mensaje_conversacion_id_4226bb24_fk_crm_conversacion_id` (`conversacion_id`),
  CONSTRAINT `crm_mensaje_conversacion_id_4226bb24_fk_crm_conversacion_id` FOREIGN KEY (`conversacion_id`) REFERENCES `crm_conversacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.crm_mensaje: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_admin_log: ~2 rows (aproximadamente)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2025-11-03 01:20:14.137223', '1', 'CARGADORES', 1, '[{"added": {}}]', 10, 1),
	(2, '2025-11-03 01:21:35.112729', '1', 'VARIOS', 1, '[{"added": {}}]', 12, 1);

-- Volcando estructura para tabla sistema_negocio.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_content_type: ~16 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(7, 'crm', 'cliente'),
	(8, 'crm', 'conversacion'),
	(9, 'crm', 'mensaje'),
	(16, 'historial', 'registrohistorial'),
	(10, 'inventario', 'categoria'),
	(14, 'inventario', 'detalleiphone'),
	(15, 'inventario', 'precio'),
	(11, 'inventario', 'producto'),
	(13, 'inventario', 'productovariante'),
	(12, 'inventario', 'proveedor'),
	(6, 'sessions', 'session');

-- Volcando estructura para tabla sistema_negocio.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_migrations: ~27 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-11-03 00:56:19.084429'),
	(2, 'auth', '0001_initial', '2025-11-03 00:56:19.801554'),
	(3, 'admin', '0001_initial', '2025-11-03 00:56:19.910881'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-03 00:56:19.922251'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-03 00:56:19.933946'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-03 00:56:19.999487'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-03 00:56:20.047793'),
	(8, 'auth', '0003_alter_user_email_max_length', '2025-11-03 00:56:20.061729'),
	(9, 'auth', '0004_alter_user_username_opts', '2025-11-03 00:56:20.070397'),
	(10, 'auth', '0005_alter_user_last_login_null', '2025-11-03 00:56:20.122030'),
	(11, 'auth', '0006_require_contenttypes_0002', '2025-11-03 00:56:20.125292'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-03 00:56:20.138697'),
	(13, 'auth', '0008_alter_user_username_max_length', '2025-11-03 00:56:20.164944'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-03 00:56:20.178717'),
	(15, 'auth', '0010_alter_group_name_max_length', '2025-11-03 00:56:20.195549'),
	(16, 'auth', '0011_update_proxy_permissions', '2025-11-03 00:56:20.205569'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-03 00:56:20.219872'),
	(18, 'crm', '0001_initial', '2025-11-03 00:56:20.559669'),
	(19, 'crm', '0002_alter_mensaje_emisor', '2025-11-03 00:56:20.568544'),
	(20, 'crm', '0003_mensaje_archivo_mensaje_tipo_mensaje', '2025-11-03 00:56:20.597203'),
	(21, 'historial', '0001_initial', '2025-11-03 00:56:20.668071'),
	(22, 'inventario', '0001_initial', '2025-11-03 00:56:21.179171'),
	(23, 'inventario', '0002_producto_imagen', '2025-11-03 00:56:21.191854'),
	(27, 'sessions', '0001_initial', '2025-11-03 00:56:21.382981'),
	(28, 'inventario', '0006_remove_producto_activo_remove_producto_codigo_barras_and_more', '2025-11-06 22:42:14.514069'),
	(29, 'inventario', '0003_producto_activo', '2025-11-07 00:55:16.871087'),
	(30, 'inventario', '0004_precio_moneda', '2025-11-07 01:02:00.695145'),
	(31, 'inventario', '0005_remove_detalleiphone_fecha_compra_and_more', '2025-11-07 01:04:32.262483');

-- Volcando estructura para tabla sistema_negocio.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_session: ~1 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('msa2ueqt76z5z271ggymv3ql7b8s0q51', '.eJxVjEEOwiAQRe_C2pDCgIBL9z0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kbgIJU6_W8L84LYDumO7zTLPbV2mJHdFHrTLcSZ-Xg_376Bir9_a55wVKxcCWHUenCFtTOFExnhndQAoAwAob5HAabaOCoA1CJY9BC3eH7yaNpA:1vFj1p:4rA4LdnEsEzjiX3swuXSXLPV6J6aGdCpLvGVo6o29Yo', '2025-11-17 01:06:37.279905');

-- Volcando estructura para tabla sistema_negocio.historial_registrohistorial
CREATE TABLE IF NOT EXISTS `historial_registrohistorial` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_accion` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `historial_registrohistorial_usuario_id_ccace41c_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `historial_registrohistorial_usuario_id_ccace41c_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.historial_registrohistorial: ~0 rows (aproximadamente)
INSERT INTO `historial_registrohistorial` (`id`, `tipo_accion`, `descripcion`, `fecha`, `usuario_id`) VALUES
	(1, 'CREACION', 'Se agregó el nuevo iPhone: iPhone 13 mini - 1TB / Azul.', '2025-11-06 22:14:53.368133', 1);

-- Volcando estructura para tabla sistema_negocio.inventario_categoria
CREATE TABLE IF NOT EXISTS `inventario_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_categoria: ~1 rows (aproximadamente)
INSERT INTO `inventario_categoria` (`id`, `nombre`, `descripcion`) VALUES
	(1, 'CARGADORES', ''),
	(2, 'Celulares', '');

-- Volcando estructura para tabla sistema_negocio.inventario_detalleiphone
CREATE TABLE IF NOT EXISTS `inventario_detalleiphone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `imei` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `salud_bateria` int unsigned DEFAULT NULL,
  `fallas_detectadas` longtext COLLATE utf8mb4_general_ci,
  `es_plan_canje` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `imei` (`imei`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_detalleiphone: ~0 rows (aproximadamente)
INSERT INTO `inventario_detalleiphone` (`id`, `imei`, `salud_bateria`, `fallas_detectadas`, `es_plan_canje`) VALUES
	(1, '123456789012345', 12, '', 1);

-- Volcando estructura para tabla sistema_negocio.inventario_precio
CREATE TABLE IF NOT EXISTS `inventario_precio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_precio` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `precio_venta_normal` decimal(10,2) NOT NULL,
  `precio_venta_minimo` decimal(10,2) NOT NULL,
  `precio_venta_descuento` decimal(10,2) DEFAULT NULL,
  `variante_id` bigint NOT NULL,
  `moneda` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `precio` decimal(12,2) NOT NULL,
  `tipo` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_precio_variante_id_tipo_precio_moneda_0026b93e_uniq` (`variante_id`,`tipo_precio`,`moneda`),
  KEY `inventario_precio_variante_id_28e3c002` (`variante_id`),
  CONSTRAINT `inventario_precio_variante_id_28e3c002_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_precio: ~0 rows (aproximadamente)
INSERT INTO `inventario_precio` (`id`, `tipo_precio`, `costo`, `precio_venta_normal`, `precio_venta_minimo`, `precio_venta_descuento`, `variante_id`, `moneda`, `activo`, `actualizado`, `creado`, `precio`, `tipo`) VALUES
	(1, 'Minorista', 1233.00, 123333.00, 1233.00, NULL, 1, 'ARS', 1, '2025-11-07 16:08:45.635499', '2025-11-07 16:08:45.661848', 0.00, 'MINORISTA'),
	(2, 'Minorista', 123.00, 3400.00, 123.00, NULL, 2, 'USD', 1, '2025-11-07 16:08:45.635499', '2025-11-07 16:08:45.661848', 0.00, 'MINORISTA');

-- Volcando estructura para tabla sistema_negocio.inventario_producto
CREATE TABLE IF NOT EXISTS `inventario_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci,
  `actualizado` datetime(6) NOT NULL,
  `categoria_id` bigint DEFAULT NULL,
  `proveedor_id` bigint DEFAULT NULL,
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `seo_descripcion` varchar(160) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `seo_titulo` varchar(70) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `codigo_barras` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `imagen_codigo_barras` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_producto_proveedor_id_2feee190_fk_inventari` (`proveedor_id`),
  KEY `inventario_producto_categoria_id_7033fb47_fk_inventari` (`categoria_id`),
  KEY `idx_producto_codigo_barras` (`codigo_barras`),
  CONSTRAINT `inventario_producto_categoria_id_7033fb47_fk_inventari` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`),
  CONSTRAINT `inventario_producto_proveedor_id_2feee190_fk_inventari` FOREIGN KEY (`proveedor_id`) REFERENCES `inventario_proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_producto: ~3 rows (aproximadamente)
INSERT INTO `inventario_producto` (`id`, `nombre`, `descripcion`, `actualizado`, `categoria_id`, `proveedor_id`, `estado`, `seo_descripcion`, `seo_titulo`, `activo`, `codigo_barras`, `imagen_codigo_barras`, `creado`) VALUES
	(1, 'Cargador 20w', '', '2025-11-03 01:22:21.202598', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023'),
	(2, 'CArgador', '', '2025-11-06 21:55:26.445794', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023'),
	(3, 'iPhone 13 mini', NULL, '2025-11-06 22:14:53.350289', 2, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023');

-- Volcando estructura para tabla sistema_negocio.inventario_productovariante
CREATE TABLE IF NOT EXISTS `inventario_productovariante` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_variante` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `stock` int unsigned NOT NULL,
  `producto_id` bigint NOT NULL,
  `codigo_barras` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `peso` decimal(10,2) NOT NULL,
  `sku` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `atributo_1` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
  `atributo_2` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
  `creado` datetime(6) NOT NULL,
  `stock_actual` int NOT NULL DEFAULT '0',
  `stock_minimo` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_productovaria_producto_id_nombre_varia_9e2b3846_uniq` (`producto_id`,`nombre_variante`),
  UNIQUE KEY `codigo_barras` (`codigo_barras`),
  UNIQUE KEY `sku` (`sku`),
  CONSTRAINT `inventario_productov_producto_id_23032fd0_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`),
  CONSTRAINT `inventario_productovariante_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_productovariante: ~0 rows (aproximadamente)
INSERT INTO `inventario_productovariante` (`id`, `nombre_variante`, `stock`, `producto_id`, `codigo_barras`, `peso`, `sku`, `activo`, `actualizado`, `atributo_1`, `atributo_2`, `creado`, `stock_actual`, `stock_minimo`) VALUES
	(1, 'Único', 10, 2, NULL, 0.00, NULL, 1, '2025-11-07 16:08:45.808734', '', '', '2025-11-07 16:08:45.931486', 0, 0),
	(2, '1TB / Azul', 1, 3, NULL, 0.00, NULL, 1, '2025-11-07 16:08:45.808734', '', '', '2025-11-07 16:08:45.931486', 0, 0);

-- Volcando estructura para tabla sistema_negocio.inventario_proveedor
CREATE TABLE IF NOT EXISTS `inventario_proveedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_proveedor: ~1 rows (aproximadamente)
INSERT INTO `inventario_proveedor` (`id`, `nombre`, `telefono`, `email`, `activo`) VALUES
	(1, 'VARIOS', '266503', 'emanuelsosa4436@gmail.com', 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
