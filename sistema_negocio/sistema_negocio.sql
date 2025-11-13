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

-- Volcando estructura para tabla sistema_negocio.asistente_ia_assistantknowledgearticle
CREATE TABLE IF NOT EXISTS `asistente_ia_assistantknowledgearticle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(140) NOT NULL,
  `resumen` longtext NOT NULL,
  `contenido` longtext NOT NULL,
  `tags` varchar(200) NOT NULL,
  `destacado` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.asistente_ia_assistantknowledgearticle: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.asistente_ia_assistantplaybook
CREATE TABLE IF NOT EXISTS `asistente_ia_assistantplaybook` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(120) NOT NULL,
  `descripcion` longtext NOT NULL,
  `pasos` json NOT NULL,
  `es_template` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.asistente_ia_assistantplaybook: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.asistente_ia_assistantquickreply
CREATE TABLE IF NOT EXISTS `asistente_ia_assistantquickreply` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(80) NOT NULL,
  `prompt` longtext NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `orden` int unsigned NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `asistente_ia_assistantquickreply_chk_1` CHECK ((`orden` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.asistente_ia_assistantquickreply: ~0 rows (aproximadamente)

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
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_permission: ~128 rows (aproximadamente)
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
	(64, 'Can view Registro de Historial', 16, 'view_registrohistorial'),
	(65, 'Can add Etiqueta', 17, 'add_etiqueta'),
	(66, 'Can change Etiqueta', 17, 'change_etiqueta'),
	(67, 'Can delete Etiqueta', 17, 'delete_etiqueta'),
	(68, 'Can view Etiqueta', 17, 'view_etiqueta'),
	(69, 'Can add venta', 18, 'add_venta'),
	(70, 'Can change venta', 18, 'change_venta'),
	(71, 'Can delete venta', 18, 'delete_venta'),
	(72, 'Can view venta', 18, 'view_venta'),
	(73, 'Can add Línea de venta', 19, 'add_lineaventa'),
	(74, 'Can change Línea de venta', 19, 'change_lineaventa'),
	(75, 'Can delete Línea de venta', 19, 'delete_lineaventa'),
	(76, 'Can view Línea de venta', 19, 'view_lineaventa'),
	(77, 'Can add Artículo de conocimiento', 20, 'add_assistantknowledgearticle'),
	(78, 'Can change Artículo de conocimiento', 20, 'change_assistantknowledgearticle'),
	(79, 'Can delete Artículo de conocimiento', 20, 'delete_assistantknowledgearticle'),
	(80, 'Can view Artículo de conocimiento', 20, 'view_assistantknowledgearticle'),
	(81, 'Can add Playbook del asistente', 21, 'add_assistantplaybook'),
	(82, 'Can change Playbook del asistente', 21, 'change_assistantplaybook'),
	(83, 'Can delete Playbook del asistente', 21, 'delete_assistantplaybook'),
	(84, 'Can view Playbook del asistente', 21, 'view_assistantplaybook'),
	(85, 'Can add Respuesta rápida', 22, 'add_assistantquickreply'),
	(86, 'Can change Respuesta rápida', 22, 'change_assistantquickreply'),
	(87, 'Can delete Respuesta rápida', 22, 'delete_assistantquickreply'),
	(88, 'Can view Respuesta rápida', 22, 'view_assistantquickreply'),
	(89, 'Can add Configuración del sistema', 23, 'add_configuracionsistema'),
	(90, 'Can change Configuración del sistema', 23, 'change_configuracionsistema'),
	(91, 'Can delete Configuración del sistema', 23, 'delete_configuracionsistema'),
	(92, 'Can view Configuración del sistema', 23, 'view_configuracionsistema'),
	(93, 'Can add preferencia usuario', 24, 'add_preferenciausuario'),
	(94, 'Can change preferencia usuario', 24, 'change_preferenciausuario'),
	(95, 'Can delete preferencia usuario', 24, 'delete_preferenciausuario'),
	(96, 'Can view preferencia usuario', 24, 'view_preferenciausuario'),
	(97, 'Can add Configuración de tienda', 25, 'add_configuraciontienda'),
	(98, 'Can change Configuración de tienda', 25, 'change_configuraciontienda'),
	(99, 'Can delete Configuración de tienda', 25, 'delete_configuraciontienda'),
	(100, 'Can view Configuración de tienda', 25, 'view_configuraciontienda'),
	(101, 'Can add Detalle de venta', 26, 'add_detalleventa'),
	(102, 'Can change Detalle de venta', 26, 'change_detalleventa'),
	(103, 'Can delete Detalle de venta', 26, 'delete_detalleventa'),
	(104, 'Can view Detalle de venta', 26, 'view_detalleventa'),
	(105, 'Can add local', 27, 'add_local'),
	(106, 'Can change local', 27, 'change_local'),
	(107, 'Can delete local', 27, 'delete_local'),
	(108, 'Can view local', 27, 'view_local'),
	(109, 'Can add Caja Diaria', 28, 'add_cajadiaria'),
	(110, 'Can change Caja Diaria', 28, 'change_cajadiaria'),
	(111, 'Can delete Caja Diaria', 28, 'delete_cajadiaria'),
	(112, 'Can view Caja Diaria', 28, 'view_cajadiaria'),
	(113, 'Can add Movimiento de Caja', 29, 'add_movimientocaja'),
	(114, 'Can change Movimiento de Caja', 29, 'change_movimientocaja'),
	(115, 'Can delete Movimiento de Caja', 29, 'delete_movimientocaja'),
	(116, 'Can view Movimiento de Caja', 29, 'view_movimientocaja'),
	(117, 'Can add Solicitud de Impresión', 30, 'add_solicitudimpresion'),
	(118, 'Can change Solicitud de Impresión', 30, 'change_solicitudimpresion'),
	(119, 'Can delete Solicitud de Impresión', 30, 'delete_solicitudimpresion'),
	(120, 'Can view Solicitud de Impresión', 30, 'view_solicitudimpresion'),
	(121, 'Can add Carrito Remoto', 31, 'add_carritoremoto'),
	(122, 'Can change Carrito Remoto', 31, 'change_carritoremoto'),
	(123, 'Can delete Carrito Remoto', 31, 'delete_carritoremoto'),
	(124, 'Can view Carrito Remoto', 31, 'view_carritoremoto'),
	(125, 'Can add Imagen de producto', 32, 'add_productoimagen'),
	(126, 'Can change Imagen de producto', 32, 'change_productoimagen'),
	(127, 'Can delete Imagen de producto', 32, 'delete_productoimagen'),
	(128, 'Can view Imagen de producto', 32, 'view_productoimagen');

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.auth_user: ~2 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$600000$Aug4S1VCCpAva4vjvJtxir$B+dNpahdN40gH9WmT7VbSO3KytHeJvuRVW9P1vsmB+A=', '2025-11-03 01:06:37.277911', 1, 'esrsosa', '', '', 'emanuelsosa4436@gmail.com', 1, 1, '2025-11-03 01:05:46.221246'),
	(2, 'pbkdf2_sha256$1000000$LnCcyS3JAbLnu8OcMupBTT$bc0lw8TgvI3UJyviyceBwtOBaI/EQFIacG2yRqLE9es=', '2025-11-13 16:09:52.581416', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2025-11-11 20:06:13.956375');

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

-- Volcando estructura para tabla sistema_negocio.caja_cajadiaria
CREATE TABLE IF NOT EXISTS `caja_cajadiaria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_apertura` datetime(6) NOT NULL,
  `monto_inicial_ars` decimal(12,2) NOT NULL,
  `fecha_cierre` datetime(6) DEFAULT NULL,
  `monto_cierre_real_ars` decimal(12,2) DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  `local_id` bigint NOT NULL,
  `usuario_apertura_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_caja_local_estado` (`local_id`,`estado`),
  KEY `idx_caja_fecha` (`fecha_apertura`),
  KEY `caja_cajadiaria_usuario_apertura_id_3670adb1_fk_auth_user_id` (`usuario_apertura_id`),
  CONSTRAINT `caja_cajadiaria_local_id_425ca589_fk_locales_local_id` FOREIGN KEY (`local_id`) REFERENCES `locales_local` (`id`),
  CONSTRAINT `caja_cajadiaria_usuario_apertura_id_3670adb1_fk_auth_user_id` FOREIGN KEY (`usuario_apertura_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.caja_cajadiaria: ~2 rows (aproximadamente)
INSERT INTO `caja_cajadiaria` (`id`, `fecha_apertura`, `monto_inicial_ars`, `fecha_cierre`, `monto_cierre_real_ars`, `estado`, `local_id`, `usuario_apertura_id`) VALUES
	(1, '2025-11-12 18:19:31.447156', 122.00, '2025-11-12 19:26:03.948536', 1.00, 'CERRADA', 1, 2),
	(2, '2025-11-13 16:35:00.127376', 0.00, '2025-11-13 16:35:09.385217', 1500.00, 'CERRADA', 1, 2);

-- Volcando estructura para tabla sistema_negocio.caja_movimientocaja
CREATE TABLE IF NOT EXISTS `caja_movimientocaja` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `monto_ars` decimal(12,2) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `caja_diaria_id` bigint NOT NULL,
  `usuario_id` int NOT NULL,
  `venta_asociada_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_mov_caja_tipo` (`caja_diaria_id`,`tipo`),
  KEY `idx_mov_venta` (`venta_asociada_id`),
  KEY `caja_movimientocaja_usuario_id_788e149a_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `caja_movimientocaja_caja_diaria_id_0363354b_fk_caja_caja` FOREIGN KEY (`caja_diaria_id`) REFERENCES `caja_cajadiaria` (`id`),
  CONSTRAINT `caja_movimientocaja_usuario_id_788e149a_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `caja_movimientocaja_venta_asociada_id_6098e59a_fk_ventas_ve` FOREIGN KEY (`venta_asociada_id`) REFERENCES `ventas_venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.caja_movimientocaja: ~4 rows (aproximadamente)
INSERT INTO `caja_movimientocaja` (`id`, `tipo`, `metodo_pago`, `monto_ars`, `descripcion`, `fecha`, `caja_diaria_id`, `usuario_id`, `venta_asociada_id`) VALUES
	(1, 'APERTURA', 'EFECTIVO_ARS', 122.00, 'Apertura de caja - Monto inicial', '2025-11-12 18:19:31.448157', 1, 2, NULL),
	(2, 'VENTA', 'EFECTIVO_ARS', 12085.48, 'Venta POS-4B6258AE', '2025-11-12 18:41:40.164738', 1, 2, 'POS-4B6258AE'),
	(3, 'VENTA', 'EFECTIVO_ARS', 7333333.26, 'Venta POS-3BABAE79', '2025-11-12 19:21:00.164626', 1, 2, 'POS-3BABAE79'),
	(4, 'APERTURA', 'EFECTIVO_ARS', 0.00, 'Apertura de caja - Monto inicial', '2025-11-13 16:35:00.131623', 2, 2, NULL);

-- Volcando estructura para tabla sistema_negocio.configuracion_configuracionsistema
CREATE TABLE IF NOT EXISTS `configuracion_configuracionsistema` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_comercial` varchar(120) NOT NULL,
  `lema` varchar(180) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `color_principal` varchar(7) NOT NULL,
  `modo_oscuro_predeterminado` tinyint(1) NOT NULL,
  `mostrar_alertas` tinyint(1) NOT NULL,
  `whatsapp_numero` varchar(30) NOT NULL,
  `acceso_admin_habilitado` tinyint(1) NOT NULL,
  `contacto_email` varchar(254) NOT NULL,
  `domicilio_comercial` varchar(200) NOT NULL,
  `notas_sistema` longtext NOT NULL,
  `dolar_blue_manual` decimal(10,2) DEFAULT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.configuracion_configuracionsistema: ~1 rows (aproximadamente)
INSERT INTO `configuracion_configuracionsistema` (`id`, `nombre_comercial`, `lema`, `logo`, `color_principal`, `modo_oscuro_predeterminado`, `mostrar_alertas`, `whatsapp_numero`, `acceso_admin_habilitado`, `contacto_email`, `domicilio_comercial`, `notas_sistema`, `dolar_blue_manual`, `ultima_actualizacion`) VALUES
	(1, 'ImportSt', 'Distribuidora de tecnología', 'branding/Belgrano_47_San_Luis..png', '#ffffff', 0, 1, '2665032890', 1, 'importstore.sanluis@gmail.com', 'Belgrano 47 local 1', '', NULL, '2025-11-12 23:14:31.174793');

-- Volcando estructura para tabla sistema_negocio.configuracion_configuraciontienda
CREATE TABLE IF NOT EXISTS `configuracion_configuraciontienda` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_tienda` varchar(150) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `cuit` varchar(20) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `email_contacto` varchar(254) NOT NULL,
  `telefono_contacto` varchar(40) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `garantia_dias_general` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `configuracion_configuraciontienda_chk_1` CHECK ((`garantia_dias_general` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.configuracion_configuraciontienda: ~1 rows (aproximadamente)
INSERT INTO `configuracion_configuraciontienda` (`id`, `nombre_tienda`, `logo`, `cuit`, `direccion`, `email_contacto`, `telefono_contacto`, `actualizado`, `garantia_dias_general`) VALUES
	(1, 'ImportStore', '', '20443604031', 'Belgrano 47, San Luis capital', 'importstore.sanluis@gmail.com', '+542665031180', '2025-11-12 22:04:19.861668', 50);

-- Volcando estructura para tabla sistema_negocio.configuracion_preferenciausuario
CREATE TABLE IF NOT EXISTS `configuracion_preferenciausuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usa_modo_oscuro` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `configuracion_prefer_usuario_id_333b55ea_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.configuracion_preferenciausuario: ~1 rows (aproximadamente)
INSERT INTO `configuracion_preferenciausuario` (`id`, `usa_modo_oscuro`, `actualizado`, `usuario_id`) VALUES
	(1, 0, '2025-11-12 23:14:31.179109', 2);

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.crm_cliente: ~2 rows (aproximadamente)
INSERT INTO `crm_cliente` (`id`, `nombre`, `telefono`, `email`, `tipo_cliente`, `instagram_handle`, `fecha_creacion`, `ultima_actualizacion`) VALUES
	(1, 'Sosa Raul emanuel', '2665032890', NULL, 'Potencial', NULL, '2025-11-12 17:18:10.837266', '2025-11-12 17:18:10.837266'),
	(2, 's', 's', NULL, 'Minorista', NULL, '2025-11-13 04:02:07.468363', '2025-11-13 04:02:07.468363');

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
  `prioridad` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `sla_vencimiento` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_conversacion_asesor_asignado_id_b38461f1_fk_auth_user_id` (`asesor_asignado_id`),
  KEY `crm_conversacion_cliente_id_6d9bafb1_fk_crm_cliente_id` (`cliente_id`),
  CONSTRAINT `crm_conversacion_asesor_asignado_id_b38461f1_fk_auth_user_id` FOREIGN KEY (`asesor_asignado_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `crm_conversacion_cliente_id_6d9bafb1_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.crm_conversacion: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.crm_conversacion_etiquetas
CREATE TABLE IF NOT EXISTS `crm_conversacion_etiquetas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `conversacion_id` bigint NOT NULL,
  `etiqueta_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_conversacion_etiquet_conversacion_id_etiqueta_e3e8c740_uniq` (`conversacion_id`,`etiqueta_id`),
  KEY `crm_conversacion_eti_etiqueta_id_9048b1b9_fk_crm_etiqu` (`etiqueta_id`),
  CONSTRAINT `crm_conversacion_eti_conversacion_id_9d07f708_fk_crm_conve` FOREIGN KEY (`conversacion_id`) REFERENCES `crm_conversacion` (`id`),
  CONSTRAINT `crm_conversacion_eti_etiqueta_id_9048b1b9_fk_crm_etiqu` FOREIGN KEY (`etiqueta_id`) REFERENCES `crm_etiqueta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.crm_conversacion_etiquetas: ~0 rows (aproximadamente)

-- Volcando estructura para tabla sistema_negocio.crm_etiqueta
CREATE TABLE IF NOT EXISTS `crm_etiqueta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `color` varchar(7) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.crm_etiqueta: ~0 rows (aproximadamente)

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
  `metadata` json DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_admin_log: ~15 rows (aproximadamente)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2025-11-03 01:20:14.137223', '1', 'CARGADORES', 1, '[{"added": {}}]', 10, 1),
	(2, '2025-11-03 01:21:35.112729', '1', 'VARIOS', 1, '[{"added": {}}]', 12, 1),
	(3, '2025-11-11 20:09:10.904678', '1', 'None — MINORISTA 10000 ARS', 2, '[{"changed": {"fields": ["Precio"]}}]', 15, 2),
	(4, '2025-11-11 20:11:44.398695', '2', 'iPhone 13 mini [None]', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2),
	(5, '2025-11-11 20:12:01.335820', '2', 'None — MINORISTA 12121212 USD', 2, '[{"changed": {"fields": ["Precio"]}}]', 15, 2),
	(6, '2025-11-12 16:58:15.306384', '2', 'CArgador', 2, '[{"changed": {"name": "Variante de Producto", "object": "CArgador [SKU-000001]", "fields": ["Stock actual"]}}]', 11, 2),
	(7, '2025-11-12 18:31:08.111219', '1', 'CArgador [SKU-000001]', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2),
	(8, '2025-11-12 18:31:08.115219', '2', 'iPhone 13 mini [SKU-000002]', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2),
	(9, '2025-11-12 20:21:30.965771', '1', 'CArgador [SKU-000001]', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2),
	(10, '2025-11-12 20:21:49.821696', '2', 'SKU-000002 — MINORISTA 350 USD', 2, '[{"changed": {"fields": ["Precio"]}}]', 15, 2),
	(11, '2025-11-12 21:38:33.388452', '1', 'CArgador [SKU-000001]', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2),
	(12, '2025-11-12 21:38:33.392453', '2', 'iPhone 13 mini [IPHONE-13-MINI-64GB-TITANIO-NATURAL] — 64GB / Titanio Natural', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2),
	(13, '2025-11-12 21:57:02.086596', '3', 'iPhone 13 mini', 2, '[{"changed": {"name": "Variante de Producto", "object": "iPhone 13 mini [IPHONE-13-MINI-64GB-TITANIO-NATURAL] \\u2014 64GB / Titanio Natural", "fields": ["Stock actual"]}}]', 11, 2),
	(14, '2025-11-12 21:57:09.264094', '1', 'Cargador 20w', 2, '[]', 11, 2),
	(15, '2025-11-12 22:13:21.552177', '2', 'iPhone 13 mini [IPHONE-13-MINI-64GB-TITANIO-NATURAL] — 64GB / Titanio Natural', 2, '[{"changed": {"fields": ["Stock actual"]}}]', 13, 2);

-- Volcando estructura para tabla sistema_negocio.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_content_type: ~32 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(20, 'asistente_ia', 'assistantknowledgearticle'),
	(21, 'asistente_ia', 'assistantplaybook'),
	(22, 'asistente_ia', 'assistantquickreply'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(28, 'caja', 'cajadiaria'),
	(29, 'caja', 'movimientocaja'),
	(23, 'configuracion', 'configuracionsistema'),
	(25, 'configuracion', 'configuraciontienda'),
	(24, 'configuracion', 'preferenciausuario'),
	(5, 'contenttypes', 'contenttype'),
	(7, 'crm', 'cliente'),
	(8, 'crm', 'conversacion'),
	(17, 'crm', 'etiqueta'),
	(9, 'crm', 'mensaje'),
	(16, 'historial', 'registrohistorial'),
	(10, 'inventario', 'categoria'),
	(14, 'inventario', 'detalleiphone'),
	(15, 'inventario', 'precio'),
	(11, 'inventario', 'producto'),
	(32, 'inventario', 'productoimagen'),
	(13, 'inventario', 'productovariante'),
	(12, 'inventario', 'proveedor'),
	(27, 'locales', 'local'),
	(6, 'sessions', 'session'),
	(31, 'ventas', 'carritoremoto'),
	(26, 'ventas', 'detalleventa'),
	(19, 'ventas', 'lineaventa'),
	(30, 'ventas', 'solicitudimpresion'),
	(18, 'ventas', 'venta');

-- Volcando estructura para tabla sistema_negocio.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_migrations: ~56 rows (aproximadamente)
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
	(31, 'inventario', '0005_remove_detalleiphone_fecha_compra_and_more', '2025-11-07 01:04:32.262483'),
	(32, 'inventario', '0007_reconcile_state_only', '2025-11-07 21:53:11.002944'),
	(33, 'asistente_ia', '0001_initial', '2025-11-08 16:45:58.104175'),
	(34, 'crm', '0004_conversacion_enhancements', '2025-11-08 16:45:58.407536'),
	(35, 'configuracion', '0001_initial', '2025-11-11 19:58:03.876085'),
	(36, 'inventario', '0006_remove_detalleiphone_variante_and_more', '2025-11-11 19:58:04.163139'),
	(37, 'inventario', '0008_detalleiphone_rebuild', '2025-11-11 19:58:04.310929'),
	(38, 'inventario', '0009_detalleiphone_variante_bridge', '2025-11-11 19:58:04.540853'),
	(39, 'inventario', '0010_sync_schema_new', '2025-11-11 19:58:04.886335'),
	(40, 'ventas', '0001_initial', '2025-11-11 19:58:05.108096'),
	(41, 'ventas', '0002_venta_extensiones', '2025-11-11 19:58:05.373184'),
	(42, 'inventario', '0007_squash_fix_state_only', '2025-11-11 19:58:05.373184'),
	(43, 'configuracion', '0002_configuraciontienda', '2025-11-12 15:48:31.722855'),
	(44, 'ventas', '0003_remove_venta_descuento_general_and_more', '2025-11-12 15:48:40.219144'),
	(45, 'locales', '0001_initial', '2025-11-12 16:18:49.343203'),
	(47, 'inventario', '0011_rename_ultima_actualizacion_and_fix_sku', '2025-11-12 16:34:56.674638'),
	(48, 'caja', '0001_initial', '2025-11-12 17:11:36.815757'),
	(49, 'ventas', '0004_detalleventa_precio_unitario_usd_original_and_more', '2025-11-12 18:25:13.132866'),
	(50, 'inventario', '0012_productovariante_codigo_barras_and_more', '2025-11-12 18:34:19.336053'),
	(51, 'inventario', '0013_add_estado_field_to_producto', '2025-11-12 20:29:48.946276'),
	(52, 'inventario', '0014_add_nombre_variante_field', '2025-11-12 20:40:04.035902'),
	(53, 'ventas', '0005_make_variante_nullable', '2025-11-12 20:50:36.603011'),
	(54, 'configuracion', '0003_configuraciontienda_garantia_dias_general', '2025-11-12 21:25:37.079696'),
	(55, 'inventario', '0015_categoria_garantia_dias', '2025-11-12 21:25:43.163793'),
	(56, 'ventas', '0006_venta_es_pago_mixto_venta_metodo_pago_2_and_more', '2025-11-12 23:39:54.501857'),
	(57, 'ventas', '0007_alter_detalleventa_variante_carritoremoto', '2025-11-13 07:09:45.647591'),
	(58, 'ventas', '0008_solicitudimpresion', '2025-11-13 07:09:45.869855'),
	(59, 'ventas', '0009_venta_descuento_metodo_pago_ars', '2025-11-13 14:04:20.681549'),
	(60, 'inventario', '0016_productoimagen', '2025-11-13 15:08:25.952422');

-- Volcando estructura para tabla sistema_negocio.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.django_session: ~23 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('0g723v6avmnn7mo60kmrc6shqrpydpt9', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJRk0:-McLfyZm59oB5E_S5oUMaehU9WefhNlxQi7WrAuVk9Q', '2025-11-27 07:27:36.135705'),
	('0t94cgbavdbqnagpsxowbt760gca9qs3', '.eJxVjDsOwjAQBe_iGllZxz9S0nMChKyN10vCJ5Ycp0LcnURKAe2befMWAZc6hGVOJYwkOqHE4XfrMT7StAG643TLMuaplrGXmyJ3OstzpvQ87e5fYMB5WN_GW-6t8wxGgSVQpiWwhhsC3yjQrHmNJU2uQWKkyC17YKWNs2iObo1GLGWsOZT0yjWL7nL9fAF5WT8g:1vJPhH:aUGHs25Odlj4G_7ytfm0prW2ChCd1EP9UW872fFiqNE', '2025-11-27 05:16:39.447376'),
	('14p8zklmi8hcptj00vzo5jflyfpwdexa', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJRk8:-YKZvkrHxq8xvOMOUzbsFd2s09sLbv9pz8FuDeeUQwY', '2025-11-27 07:27:44.387442'),
	('8wqugj5agb9y5sy0gj7jk0s2io8is6pt', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZLk:fM3ivcDgx48Bc0WJTKAvHM6QgxtpTWC41O33ia_dTe8', '2025-11-27 15:35:04.744420'),
	('aucedjbk59jktb21ux43qxlirnxej9fo', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJS0x:Xlyy9PYIro4uqMLfZPS1vCnh0vRvK7xPtjbjq9tVtgc', '2025-11-27 07:45:07.432670'),
	('axfmt132087b8z8oh3gf943czt1n88c5', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJY3u:HG_xF0yH5NXICfa0BGk8GiDF4sTP0Vu3JWe8XClV-tQ', '2025-11-27 14:12:34.475382'),
	('cdkrgx38xp1w3fq8npqcijcm1fht51ig', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vIurZ:S0Cc11OUsFmWeFc9tPJhZxf4PUGVy7e-0CKcLD0ClY0', '2025-11-25 20:21:13.921514'),
	('dm7dx4zdh2kcj0eeydrxjanw5sj8jgnz', '.eJxVjrtuwzAMRX8l0GwYluNXs7WdO3UsCoHWI2Zii4Ykdwny72UcI0053se5vAgFSxrUEm1QaMRBlCJ71nrQZ-tvhjmBP1KuyaeAfX6L5Jsb8w8ydnzbsv8AA8SB23XXuL5pOyfrUjZGlvXeyKZ2hZFdUcrKVY5htjJtAcaB0W7vOunKqm4bqF9ahmoIAROpYCdKJA5fF_EDAcEnu74uMxHPC29x8AiGAnc8TX2wrL2_PjRjow44ayT_ZOw-0e9snK1Gh0xYB31CA4wuMzEHdkgtHhOPkoIQebLgy4s_NxpFAY_oYRQHv4xjJmxUOA_k-QsHY7SropeYaHoo9zoDL2JCz4SY4L4gtolCXK_f1180TZE-:1vJQR7:vxO6nisHIWCFvWmSuefHWUOCtzOWRtMflus6h7cR510', '2025-11-27 06:04:01.812474'),
	('e5rob8jh27puw0nf1ccbyztu6ys1ysvz', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZtQ:jHfYrBva2nzUcnY-N7pnlNmpi4jKlr9n3XdUGF1QW00', '2025-11-27 16:09:52.581416'),
	('eb9hqtxujmieyopwj0e4x4hl36qrms0c', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZ99:36fEGzIg3a1V0j7woQ8fiwZeW3zmlFeCAlEXc55KHQU', '2025-11-27 15:22:03.818907'),
	('fuicmdeqn043tfov8p3av3364asr9ydy', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJPQc:cJm9I2DSTYbi2HZAUxskdQFr5CqYzzvmpnK7e-Sr740', '2025-11-27 04:59:26.469841'),
	('iyjfnmaj00qao2zk2j9y41j4mi2phcwy', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJY3t:Uk-irswfBzQbJr03629X7nM8-om6y1dt3PFJj4VmJs8', '2025-11-27 14:12:33.208342'),
	('lfioiqrtkocaz735iuajv2k3j1ai80wo', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZ0q:eWXTGSRc010jXkoV5E4L0aauF6NGGoK3g4YhinG-R1o', '2025-11-27 15:13:28.836164'),
	('mhirscrf8ylm4v8o1qabjy5yykp8uvog', '.eJxVjrtuwzAMRX8l0GwYluNXs7WdO3UsCoHWI2Zii4Ykdwny72UcI0053se5vAgFSxrUEm1QaMRBlCJ71nrQZ-tvhjmBP1KuyaeAfX6L5Jsb8w8ydnzbsv8AA8SB23XXuL5pOyfrUjZGlvXeyKZ2hZFdUcrKVY5htjJtAcaB0W7vOunKqm4bqF9ahmoIAROpYCdKJA5fF_EDAcEnu74uMxHPC29x8AiGAnc8TX2wrL2_PjRjow44ayT_ZOw-0e9snK1Gh0xYB31CA4yu2kzMgS1Si8fEq6QgRN4s-PLiz41GUcAjehjFwS_jmAkbFc4DeX7DwRjtquglJpoeyr3OwIuY0DMhJrgviG2iENfr9_UXtQWRdw:1vJPWH:T76niIhumzDp7hi6NHzCXkT37N7TVL_yf00_5AuTAI0', '2025-11-27 05:05:17.460091'),
	('msa2ueqt76z5z271ggymv3ql7b8s0q51', '.eJxVjEEOwiAQRe_C2pDCgIBL9z0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kbgIJU6_W8L84LYDumO7zTLPbV2mJHdFHrTLcSZ-Xg_376Bir9_a55wVKxcCWHUenCFtTOFExnhndQAoAwAob5HAabaOCoA1CJY9BC3eH7yaNpA:1vFj1p:4rA4LdnEsEzjiX3swuXSXLPV6J6aGdCpLvGVo6o29Yo', '2025-11-17 01:06:37.279905'),
	('mtrc6d2a4zzmk3fuq4bzsqq7trgb75kb', '.eJxVjLkOwjAQBf_FNbJi4wu60FFESEBDZW28XhKOGOWoEP-OI6WA9s28eTMP09j4aYi9b5FtmWSr362GcI_dDPAG3TXxkLqxb2s-K3yhA68Sxsducf8CDQxNfmtnqDbWkdBSGBRSr1EYTQUKV0ihSFGORYW2ACTAQGtygqTS1oDe2Bx9Jkz-1cfQphysysvhuD-dS_b5Au-lQAw:1vJaHJ:Sac3_8ss_Z2DYFw157SV0B4ci-86AIPUoW_dWV36g1o', '2025-11-27 16:34:33.999577'),
	('nb01o5oilyl8vw8stncrmzbuy1arcupw', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJYzV:ft5AtRNVxfLCyolYQ-GxgL_TG_X4f-HSFaa4SYaK0gs', '2025-11-27 15:12:05.379683'),
	('px26c45tdy9au338butruirhjn9yvivw', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJS0p:jr6Ly2d694GmAWSaMCxx5bPpbK7fwj7Dyn8ILJcNGtM', '2025-11-27 07:44:59.039390'),
	('q3ixqctaadr3vjylutzsyt54s1537h7v', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vIudI:_OLMxaz1wtiFqVFgGG-CaUWRwK0W1gKAU2My_S_49ME', '2025-11-25 20:06:28.196085'),
	('tw9flkkzxiu40od5nlfm4mbu7gmp4d87', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJPdD:z5qqP36MWRxD9J2I2IXYvUZ-pzC3L02HQ-tqtaG3bzU', '2025-11-27 05:12:27.840176'),
	('tyiuvm69kmy4bczlzs2ld23urzmhszvw', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJXt7:Y2nj3nw-9mmkP3mS3xQsoPVDqX1KAXzI1xwGkQlUOfI', '2025-11-27 14:01:25.750910'),
	('ub0c0jtm0cj5zfv1whlsw1eo5lydx17c', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJRj3:mdnzDz67e-oFfJT4p0AT6NoQ5Mtas9j5LiksMVzjAVE', '2025-11-27 07:26:37.048013'),
	('y4da69m4vkpya3xe0w4a54waivpuzc7o', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZrQ:nqBjrxM4fi9vu6PbsUV-kH3dY8mbFevqJju5VuHuqq8', '2025-11-27 16:07:48.265267');

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
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.historial_registrohistorial: ~64 rows (aproximadamente)
INSERT INTO `historial_registrohistorial` (`id`, `tipo_accion`, `descripcion`, `fecha`, `usuario_id`) VALUES
	(1, 'CREACION', 'Se agregó el nuevo iPhone: iPhone 13 mini - 1TB / Azul.', '2025-11-06 22:14:53.368133', 1),
	(2, 'VENTA', 'Venta POS-0686AF2B por 9000.00 (efectivo).', '2025-11-11 20:09:48.099498', NULL),
	(3, 'VENTA', 'Venta POS-7C627328 por 12906666.54 (efectivo).', '2025-11-11 20:13:01.224965', 2),
	(4, 'VENTA', 'Venta POS-6A89ADAE por 10000.00 (efectivo).', '2025-11-11 20:22:27.192347', 2),
	(5, 'VENTA', 'Venta POS-88CA0C8B por 12121212.00 (efectivo).', '2025-11-11 20:44:58.359410', 2),
	(6, 'VENTA', 'Venta POS-CF4E18B1 por 10000.00 (efectivo).', '2025-11-12 15:22:13.782224', 2),
	(7, 'VENTA', 'Venta POS-BE12561B por $10000.00 (EFECTIVO_ARS).', '2025-11-12 16:58:29.682890', 2),
	(9, 'ESTADO', 'Estado inactivo → iPhone 13 mini', '2025-11-12 17:16:12.065615', 2),
	(10, 'ESTADO', 'Estado activo → iPhone 13 mini', '2025-11-12 17:16:17.210622', 2),
	(11, 'VENTA', 'Venta POS-6251D818 por $12085.48 (EFECTIVO_ARS).', '2025-11-12 17:58:54.803385', 2),
	(12, 'VENTA', 'Venta POS-CB216F2A por $10648.00 (EFECTIVO_ARS).', '2025-11-12 18:04:34.609291', 2),
	(13, 'VENTA', 'Venta POS-119A299D por $12085.48 (EFECTIVO_USD).', '2025-11-12 18:07:21.151394', 2),
	(15, 'VENTA', 'Venta POS-B627CAD1 por $12121212.00 (EFECTIVO_ARS).', '2025-11-12 18:14:47.970821', 2),
	(16, 'VENTA', 'Venta POS-4B6258AE por $12085.48 (EFECTIVO_ARS).', '2025-11-12 18:41:40.047282', 2),
	(17, 'VENTA', 'Venta POS-3BABAE79 por $7333333.26 (EFECTIVO_ARS).', '2025-11-12 19:21:00.029567', 2),
	(18, 'VENTA', 'Venta POS-B0240418 por $10648.00 (EFECTIVO_ARS).', '2025-11-12 20:00:17.935555', 2),
	(19, 'VENTA', 'Venta POS-F5DB5517 por $616048.60 (EFECTIVO_ARS).', '2025-11-12 20:10:17.632548', 2),
	(20, 'VENTA', 'Venta POS-5D3E5CE4 por $381.15 (TARJETA).', '2025-11-12 20:25:57.543526', 2),
	(21, 'ESTADO', 'Estado inactivo → iPhone 13 mini', '2025-11-12 20:32:45.683187', 2),
	(22, 'ESTADO', 'Estado activo → iPhone 13 mini', '2025-11-12 20:32:48.144542', 2),
	(23, 'VENTA', 'Venta POS-553AE394 por $10648.00 (EFECTIVO_ARS).', '2025-11-12 20:34:26.182190', 2),
	(24, 'VENTA', 'Venta POS-298C6FD3 por $10621.38 (TRANSFERENCIA).', '2025-11-12 20:41:38.961576', 2),
	(25, 'VENTA', 'Venta POS-5BEC9024 por $1488.00 (EFECTIVO_ARS).', '2025-11-12 20:52:37.059502', 2),
	(26, 'VENTA', 'Venta POS-796712CB por $1999.00 (EFECTIVO_ARS).', '2025-11-12 20:53:08.470798', 2),
	(28, 'MODIFICACION', 'Actualización iPhone iPhone 13 mini (64GB / Titanio Natural)', '2025-11-12 21:28:43.520548', 2),
	(29, 'VENTA', 'Venta POS-90825F5D por $10000.00 (EFECTIVO_ARS).', '2025-11-12 21:36:40.290284', 2),
	(30, 'VENTA', 'Venta POS-65B108DF por $11949.19 (EFECTIVO_ARS).', '2025-11-12 21:38:39.256947', 2),
	(31, 'VENTA', 'Venta POS-DF47FA7E por $1729130.00 (EFECTIVO_ARS).', '2025-11-12 21:53:35.433867', 2),
	(32, 'VENTA', 'Venta POS-C21BAE7C por $2092247.30 (EFECTIVO_ARS).', '2025-11-12 21:58:46.699782', 2),
	(33, 'VENTA', 'Venta POS-A4518974 por $20000.00 (EFECTIVO_ARS).', '2025-11-12 22:01:07.478957', 2),
	(34, 'VENTA', 'Venta POS-39941E37 por $1729130.00 (TRANSFERENCIA).', '2025-11-12 22:07:47.683654', 2),
	(35, 'VENTA', 'Venta POS-9EB7FA22 por $1729130.00 (EFECTIVO_ARS).', '2025-11-12 22:13:24.942162', 2),
	(36, 'VENTA', 'Venta POS-00EA9703 por $50000.00 (EFECTIVO_ARS).', '2025-11-12 22:17:54.190908', 2),
	(37, 'VENTA', 'Venta POS-B80FE78F por $14666666.52 (EFECTIVO_ARS).', '2025-11-12 22:21:27.664003', 2),
	(38, 'VENTA', 'Venta POS-FE370894 por $1288.00 (EFECTIVO_ARS).', '2025-11-12 23:06:06.558582', 2),
	(39, 'VENTA', 'Venta POS-92C3F826 por $21212.00 (EFECTIVO_ARS).', '2025-11-12 23:09:49.890483', 2),
	(40, 'VENTA', 'Venta POS-ECB1CCF8 por $13552.00 (EFECTIVO_ARS).', '2025-11-12 23:15:39.300115', 2),
	(41, 'VENTA', 'Venta POS-130AD6CE por $121.00 (EFECTIVO_ARS).', '2025-11-12 23:23:04.337819', 2),
	(42, 'VENTA', 'Venta POS-D990084C por $10000.00 (TRANSFERENCIA).', '2025-11-12 23:41:57.760327', 2),
	(43, 'VENTA', 'Venta POS-ABFC278E por $1729130.00 (EFECTIVO_ARS).', '2025-11-12 23:43:15.684592', 2),
	(44, 'VENTA', 'Venta POS-F74FFB14 por $1212.00 (EFECTIVO_ARS).', '2025-11-12 23:44:59.189877', 2),
	(45, 'VENTA', 'Venta POS-248DDA43 por $10000.00 (EFECTIVO_ARS).', '2025-11-12 23:47:12.400974', 2),
	(46, 'VENTA', 'Venta POS-3650B009 por $10000.00 (EFECTIVO_ARS).', '2025-11-12 23:54:24.252033', 2),
	(47, 'VENTA', 'Venta POS-0E5CFD36 por $12222.00 (EFECTIVO_ARS).', '2025-11-13 00:00:21.109901', 2),
	(48, 'CREACION', 'Alta iPhone iPhone 16 (128GB / Titanio Negro)', '2025-11-13 03:44:06.003076', 2),
	(49, 'VENTA', 'Venta POS-1E7960FF por $2092247.30 (EFECTIVO_ARS).', '2025-11-13 03:44:33.898798', 2),
	(50, 'MODIFICACION', 'Actualización iPhone iPhone 16 (128GB / Titanio Negro)', '2025-11-13 03:45:37.842376', 2),
	(51, 'ELIMINACION', 'Baja iPhone iPhone 13 mini (64GB / Titanio Natural)', '2025-11-13 03:47:46.646351', 2),
	(52, 'VENTA', 'Venta POS-040397B8 por $10513.33 (EFECTIVO_ARS).', '2025-11-13 04:02:07.501802', 2),
	(53, 'VENTA', 'Venta POS-8D0BAA4A por $11.00 (EFECTIVO_ARS).', '2025-11-13 04:02:47.967546', 2),
	(54, 'ESTADO', 'Estado de venta POS-D990084C cambiado de Completado a Pendiente de pago', '2025-11-13 04:38:54.319609', 2),
	(55, 'VENTA', 'Venta POS-41E8B8C7 por $6685.25 (EFECTIVO_ARS).', '2025-11-13 05:27:20.995995', 2),
	(56, 'ELIMINACION', 'Venta POS-41E8B8C7 anulada. Stock devuelto. ', '2025-11-13 05:28:25.231134', 2),
	(57, 'VENTA', 'Venta POS-A074FD78 por $60197.50 (EFECTIVO_ARS).', '2025-11-13 05:33:48.488027', 2),
	(58, 'VENTA', 'Venta POS-A518A580 por $9990.00 (EFECTIVO_ARS).', '2025-11-13 06:18:20.890565', 2),
	(59, 'VENTA', 'Venta POS-5773F459 por $8075.00 (EFECTIVO_ARS).', '2025-11-13 06:50:19.676838', 2),
	(60, 'ELIMINACION', 'Venta POS-5773F459 anulada. Stock devuelto. ', '2025-11-13 07:01:33.558014', 2),
	(61, 'VENTA', 'Venta POS-049D4502 por $1477835.50 (EFECTIVO_ARS).', '2025-11-13 07:17:04.326943', 2),
	(62, 'VENTA', 'Venta POS-20F0E7F3 por $9500.00 (EFECTIVO_ARS).', '2025-11-13 07:23:37.283467', 2),
	(63, 'VENTA', 'Venta POS-D4BF06D2 por $5759.60 (EFECTIVO_ARS).', '2025-11-13 07:42:42.522376', 2),
	(64, 'VENTA', 'Venta POS-CDE476D4 por $9770.75 (EFECTIVO_ARS).', '2025-11-13 14:15:02.732651', 2),
	(65, 'CREACION', 'Alta iPhone iPhone 15 Pro (64GB / Titanio Natural)', '2025-11-13 15:28:11.070914', 2),
	(66, 'ESTADO', 'Estado inactivo → iPhone 13 mini', '2025-11-13 15:30:11.219692', 2),
	(67, 'MODIFICACION', 'Actualización iPhone iPhone 16 (128GB / Titanio Negro)', '2025-11-13 16:21:56.588624', 2);

-- Volcando estructura para tabla sistema_negocio.inventario_categoria
CREATE TABLE IF NOT EXISTS `inventario_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `garantia_dias` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `idx_categoria_nombre` (`nombre`),
  CONSTRAINT `inventario_categoria_chk_1` CHECK ((`garantia_dias` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_categoria: ~3 rows (aproximadamente)
INSERT INTO `inventario_categoria` (`id`, `nombre`, `descripcion`, `garantia_dias`) VALUES
	(1, 'CARGADORES', '', 30),
	(2, 'Celulares', '', 60),
	(3, 'Fundas', '', NULL);

-- Volcando estructura para tabla sistema_negocio.inventario_detalleiphone
CREATE TABLE IF NOT EXISTS `inventario_detalleiphone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `imei` varchar(15) DEFAULT NULL,
  `salud_bateria` int unsigned DEFAULT NULL,
  `fallas_detectadas` longtext NOT NULL,
  `es_plan_canje` tinyint(1) NOT NULL,
  `costo_usd` decimal(10,2) DEFAULT NULL,
  `precio_venta_usd` decimal(10,2) NOT NULL,
  `precio_oferta_usd` decimal(10,2) DEFAULT NULL,
  `notas` longtext NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `variante_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `variante_id` (`variante_id`),
  UNIQUE KEY `imei` (`imei`),
  CONSTRAINT `inventario_detalleip_variante_id_aea6e6f8_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`),
  CONSTRAINT `inventario_detalleiphone_chk_1` CHECK ((`salud_bateria` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_detalleiphone: ~2 rows (aproximadamente)
INSERT INTO `inventario_detalleiphone` (`id`, `imei`, `salud_bateria`, `fallas_detectadas`, `es_plan_canje`, `costo_usd`, `precio_venta_usd`, `precio_oferta_usd`, `notas`, `foto`, `creado`, `actualizado`, `variante_id`) VALUES
	(2, '123456789012340', 12, '', 1, 1222.00, 1222.00, NULL, '', '', '2025-11-13 03:44:06.001074', '2025-11-13 16:21:56.588624', 4),
	(3, '', NULL, '', 1, 1000.00, 1500.00, NULL, '', '', '2025-11-13 15:28:11.070914', '2025-11-13 15:28:11.070914', 9);

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
  KEY `idx_precio_activo` (`activo`),
  KEY `idx_precio_var_tipo_mon` (`variante_id`,`tipo`,`moneda`),
  CONSTRAINT `inventario_precio_variante_id_28e3c002_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_precio: ~7 rows (aproximadamente)
INSERT INTO `inventario_precio` (`id`, `tipo_precio`, `costo`, `precio_venta_normal`, `precio_venta_minimo`, `precio_venta_descuento`, `variante_id`, `moneda`, `activo`, `actualizado`, `creado`, `precio`, `tipo`) VALUES
	(1, 'Minorista', 1233.00, 123333.00, 1233.00, NULL, 1, 'ARS', 1, '2025-11-13 06:55:58.431991', '2025-11-07 16:08:45.661848', 9500.00, 'MINORISTA'),
	(2, 'Minorista', 123.00, 3400.00, 123.00, NULL, 2, 'USD', 1, '2025-11-12 21:28:43.486897', '2025-11-07 16:08:45.661848', 1222.00, 'MINORISTA'),
	(3, 'MAYORISTA', 0.00, 1222.00, 1222.00, NULL, 2, 'USD', 1, '2025-11-12 18:28:43.000000', '2025-11-12 18:28:43.000000', 1222.00, 'MAYORISTA'),
	(4, 'MINORISTA', 0.00, 1222.00, 1222.00, NULL, 4, 'USD', 1, '2025-11-13 16:21:56.582362', '2025-11-13 00:44:05.000000', 1222.00, 'MINORISTA'),
	(5, 'MAYORISTA', 0.00, 1222.00, 1222.00, NULL, 4, 'USD', 1, '2025-11-13 16:21:56.588624', '2025-11-13 00:44:05.000000', 1222.00, 'MAYORISTA'),
	(6, 'MINORISTA', 0.00, 1500.00, 1500.00, NULL, 9, 'USD', 1, '2025-11-13 12:28:11.000000', '2025-11-13 12:28:11.000000', 1500.00, 'MINORISTA'),
	(7, 'MAYORISTA', 0.00, 1500.00, 1500.00, NULL, 9, 'USD', 1, '2025-11-13 12:28:11.000000', '2025-11-13 12:28:11.000000', 1500.00, 'MAYORISTA');

-- Volcando estructura para tabla sistema_negocio.inventario_producto
CREATE TABLE IF NOT EXISTS `inventario_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci,
  `actualizado` datetime(6) DEFAULT NULL,
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
  KEY `idx_producto_activo` (`activo`),
  KEY `idx_producto_nombre` (`nombre`),
  KEY `idx_producto_cod_barras` (`codigo_barras`),
  CONSTRAINT `inventario_producto_categoria_id_7033fb47_fk_inventari` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`),
  CONSTRAINT `inventario_producto_proveedor_id_2feee190_fk_inventari` FOREIGN KEY (`proveedor_id`) REFERENCES `inventario_proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_producto: ~5 rows (aproximadamente)
INSERT INTO `inventario_producto` (`id`, `nombre`, `descripcion`, `actualizado`, `categoria_id`, `proveedor_id`, `estado`, `seo_descripcion`, `seo_titulo`, `activo`, `codigo_barras`, `imagen_codigo_barras`, `creado`) VALUES
	(1, 'Cargador 20w', '', '2025-11-12 21:57:09.263095', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023'),
	(2, 'Cargador 20w', 'Caragdor 292', '2025-11-13 06:55:58.419261', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023'),
	(3, 'iPhone 13 mini', '', '2025-11-13 15:30:11.213695', 2, NULL, 'ACTIVO', NULL, NULL, 0, NULL, NULL, '2025-11-07 16:08:45.733023'),
	(11, 'iPhone 16', '', '2025-11-13 16:21:56.571924', 2, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 03:44:05.946364'),
	(21, 'iPhone 15 Pro', '', '2025-11-13 15:28:11.009025', 2, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 15:28:11.007026');

-- Volcando estructura para tabla sistema_negocio.inventario_productovariante
CREATE TABLE IF NOT EXISTS `inventario_productovariante` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_variante` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `stock` int unsigned NOT NULL,
  `producto_id` bigint NOT NULL,
  `codigo_barras` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `peso` decimal(10,2) NOT NULL,
  `sku` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `atributo_1` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
  `atributo_2` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
  `creado` datetime(6) NOT NULL,
  `stock_actual` int NOT NULL DEFAULT '0',
  `stock_minimo` int NOT NULL DEFAULT '0',
  `qr_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_productovaria_producto_id_nombre_varia_9e2b3846_uniq` (`producto_id`,`nombre_variante`),
  UNIQUE KEY `sku` (`sku`),
  UNIQUE KEY `codigo_barras` (`codigo_barras`),
  KEY `idx_var_sku` (`sku`),
  KEY `idx_var_activo` (`activo`),
  KEY `idx_var_stock` (`stock_actual`),
  CONSTRAINT `inventario_productov_producto_id_23032fd0_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`),
  CONSTRAINT `inventario_productovariante_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_productovariante: ~4 rows (aproximadamente)
INSERT INTO `inventario_productovariante` (`id`, `nombre_variante`, `stock`, `producto_id`, `codigo_barras`, `peso`, `sku`, `activo`, `actualizado`, `atributo_1`, `atributo_2`, `creado`, `stock_actual`, `stock_minimo`, `qr_code`) VALUES
	(1, 'Único', 12, 2, NULL, 0.00, 'cargador-20w-pata-recta', 1, '2025-11-13 06:55:58.427992', 'pata recta', '', '2025-11-07 16:08:45.931486', 10, 0, NULL),
	(2, '1TB / Azul', 1, 3, NULL, 0.00, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 1, '2025-11-12 22:13:21.547175', '64GB', 'Titanio Natural', '2025-11-07 16:08:45.931486', 0, 0, NULL),
	(4, 'iPhone 16 128GB Titanio Negro', 1, 11, '443395475901', 0.00, 'IPHONE-16-128GB-TITANIO-NEGRO', 1, '2025-11-13 16:21:56.571924', '128GB', 'Titanio Negro', '2025-11-13 03:44:05.956153', 1, 0, 'https://importstore.com/producto/IPHONE-16-128GB-TITANIO-NEGRO'),
	(9, 'iPhone 15 Pro 64GB Titanio Natural', 1, 21, '805687808856', 0.00, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 1, '2025-11-13 15:28:11.020720', '64GB', 'Titanio Natural', '2025-11-13 15:28:11.020720', 1, 0, 'https://importstore.com/producto/IPHONE-15-PRO-64GB-TITANIO-NATURAL');

-- Volcando estructura para tabla sistema_negocio.inventario_proveedor
CREATE TABLE IF NOT EXISTS `inventario_proveedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `idx_proveedor_activo` (`activo`),
  KEY `idx_proveedor_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla sistema_negocio.inventario_proveedor: ~1 rows (aproximadamente)
INSERT INTO `inventario_proveedor` (`id`, `nombre`, `telefono`, `email`, `activo`) VALUES
	(1, 'VARIOS', '266503', 'emanuelsosa4436@gmail.com', 1);

-- Volcando estructura para tabla sistema_negocio.locales_local
CREATE TABLE IF NOT EXISTS `locales_local` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.locales_local: ~1 rows (aproximadamente)
INSERT INTO `locales_local` (`id`, `nombre`, `direccion`, `creado`, `actualizado`) VALUES
	(1, 'ImportST', 'Belgrano 47, San Luis', '2025-11-12 16:57:31.035108', '2025-11-12 16:57:31.035108');

-- Volcando estructura para tabla sistema_negocio.ventas_carritoremoto
CREATE TABLE IF NOT EXISTS `ventas_carritoremoto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `items` json NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `ventas_carritoremoto_usuario_id_ab0111ac_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.ventas_carritoremoto: ~1 rows (aproximadamente)
INSERT INTO `ventas_carritoremoto` (`id`, `items`, `actualizado`, `usuario_id`) VALUES
	(1, '[]', '2025-11-13 14:15:03.412094', 2);

-- Volcando estructura para tabla sistema_negocio.ventas_detalleventa
CREATE TABLE IF NOT EXISTS `ventas_detalleventa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sku` varchar(60) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `precio_unitario_ars_congelado` decimal(12,2) NOT NULL,
  `subtotal_ars` decimal(12,2) NOT NULL,
  `variante_id` bigint DEFAULT NULL,
  `venta_id` varchar(20) NOT NULL,
  `precio_unitario_usd_original` decimal(12,2) DEFAULT NULL,
  `tipo_cambio_usado` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_detalleventa_venta_id_c370bcd7_fk_ventas_venta_id` (`venta_id`),
  KEY `ventas_detalleventa_variante_id_67772d78_fk_inventari` (`variante_id`),
  CONSTRAINT `ventas_detalleventa_variante_id_67772d78_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`),
  CONSTRAINT `ventas_detalleventa_venta_id_c370bcd7_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`),
  CONSTRAINT `ventas_detalleventa_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.ventas_detalleventa: ~50 rows (aproximadamente)
INSERT INTO `ventas_detalleventa` (`id`, `sku`, `descripcion`, `cantidad`, `precio_unitario_ars_congelado`, `subtotal_ars`, `variante_id`, `venta_id`, `precio_unitario_usd_original`, `tipo_cambio_usado`) VALUES
	(1, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-BE12561B', NULL, NULL),
	(3, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-6251D818', NULL, NULL),
	(4, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-CB216F2A', NULL, NULL),
	(5, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-119A299D', NULL, NULL),
	(7, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 12121212.00, 12121212.00, 2, 'POS-B627CAD1', NULL, NULL),
	(8, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-4B6258AE', NULL, NULL),
	(9, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 12121212.00, 12121212.00, 2, 'POS-3BABAE79', 12121212.00, 1420.00),
	(10, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 8800.00, 1, 'POS-B0240418', NULL, NULL),
	(11, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 9988.00, 1, 'POS-F5DB5517', NULL, NULL),
	(12, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 12121212.00, 606060.60, 2, 'POS-F5DB5517', 12121212.00, 1420.00),
	(13, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 350.00, 350.00, 2, 'POS-5D3E5CE4', 350.00, 1420.00),
	(14, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 8800.00, 1, 'POS-553AE394', NULL, NULL),
	(15, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 8778.00, 1, 'POS-298C6FD3', NULL, NULL),
	(16, 'VAR-1762980757.047442', 'Producto varios', 1, 1500.00, 1488.00, NULL, 'POS-5BEC9024', NULL, NULL),
	(17, 'VAR-1762980788.462759', 'Producto varios', 1, 1999.00, 1999.00, NULL, 'POS-796712CB', NULL, NULL),
	(19, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-90825F5D', NULL, NULL),
	(20, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1222.00, 1222.00, 2, 'POS-65B108DF', 1222.00, 1415.00),
	(21, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-65B108DF', NULL, NULL),
	(22, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, 2, 'POS-DF47FA7E', 1222.00, 1415.00),
	(23, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, 2, 'POS-C21BAE7C', 1222.00, 1415.00),
	(24, 'SKU-000001', 'CArgador Sin especificar', 2, 10000.00, 20000.00, 1, 'POS-A4518974', NULL, NULL),
	(25, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, 2, 'POS-39941E37', 1222.00, 1415.00),
	(26, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, 2, 'POS-9EB7FA22', 1222.00, 1415.00),
	(27, 'VAR-1762985874.181103', 'Producto varios', 1, 50000.00, 50000.00, NULL, 'POS-00EA9703', NULL, NULL),
	(28, 'VAR-1762986087.653159', 'Producto varios', 1, 12121212.00, 12121212.00, NULL, 'POS-B80FE78F', NULL, NULL),
	(29, 'VAR-1762988766.550541', 'Producto varios', 1, 1300.00, 1288.00, NULL, 'POS-FE370894', NULL, NULL),
	(30, 'VAR-1762988989.885236', 'Producto varios', 1, 21212.00, 21212.00, NULL, 'POS-92C3F826', NULL, NULL),
	(31, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-ECB1CCF8', NULL, NULL),
	(32, 'VAR-1762989339.28968', 'Producto varios', 1, 1212.00, 1212.00, NULL, 'POS-ECB1CCF8', NULL, NULL),
	(33, 'VAR-1762989784.326604', 'Producto varios', 1, 121.00, 121.00, NULL, 'POS-130AD6CE', NULL, NULL),
	(34, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-D990084C', NULL, NULL),
	(35, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, 2, 'POS-ABFC278E', 1222.00, 1415.00),
	(36, 'VAR-1762991096597', 'cacsscacs', 1, 1212.00, 1212.00, NULL, 'POS-F74FFB14', NULL, NULL),
	(37, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-248DDA43', NULL, NULL),
	(38, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-3650B009', NULL, NULL),
	(39, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-0E5CFD36', NULL, NULL),
	(40, 'VAR-1762992012680', 'CARGADOR 20W', 1, 2222.00, 2222.00, NULL, 'POS-0E5CFD36', NULL, NULL),
	(41, 'IPHONE-16-128GB-TITANIO-NEGRO', 'iPhone 16 128GB / Titanio Negro', 1, 1729130.00, 1729130.00, 4, 'POS-1E7960FF', 1222.00, 1415.00),
	(42, 'cargador', 'CArgador Sin especificar', 1, 10000.00, 9000.00, 1, 'POS-040397B8', NULL, NULL),
	(43, 'VAR-1763006399390', 'tv', 1, 1222.00, 1222.00, NULL, 'POS-040397B8', NULL, NULL),
	(44, 'VAR-1763006565804', 'aaaa', 1, 11.00, 11.00, NULL, 'POS-8D0BAA4A', NULL, NULL),
	(45, 'VAR-1763011627490', 'Parlante', 1, 6500.00, 6500.00, NULL, 'POS-41E8B8C7', NULL, NULL),
	(46, 'VAR-1763011991916', 'TV box', 1, 50500.00, 50500.00, NULL, 'POS-A074FD78', NULL, NULL),
	(47, 'VAR-1763014697928', 'Fundas 2x1', 1, 9990.00, 9990.00, NULL, 'POS-A518A580', NULL, NULL),
	(48, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-5773F459', NULL, NULL),
	(49, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-049D4502', NULL, NULL),
	(50, 'IPHONE-16-128GB-TITANIO-NEGRO', 'iPhone 16 128GB / Titanio Negro', 1, 1729130.00, 1729130.00, 4, 'POS-049D4502', 1222.00, 1415.00),
	(51, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-20F0E7F3', NULL, NULL),
	(52, 'VAR-1763019751174', 'Cargador', 1, 5600.00, 5600.00, NULL, 'POS-D4BF06D2', NULL, NULL),
	(53, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-CDE476D4', NULL, NULL);

-- Volcando estructura para tabla sistema_negocio.ventas_solicitudimpresion
CREATE TABLE IF NOT EXISTS `ventas_solicitudimpresion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `estado` varchar(20) NOT NULL,
  `error` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `procesado` datetime(6) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  `venta_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_solicitudimpresion_usuario_id_eb5afc53_fk_auth_user_id` (`usuario_id`),
  KEY `ventas_solicitudimpresion_venta_id_0965f3de_fk_ventas_venta_id` (`venta_id`),
  CONSTRAINT `ventas_solicitudimpresion_usuario_id_eb5afc53_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `ventas_solicitudimpresion_venta_id_0965f3de_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.ventas_solicitudimpresion: ~11 rows (aproximadamente)
INSERT INTO `ventas_solicitudimpresion` (`id`, `estado`, `error`, `creado`, `procesado`, `usuario_id`, `venta_id`) VALUES
	(1, 'COMPLETADA', '', '2025-11-13 07:12:34.063212', '2025-11-13 07:12:38.890269', 2, 'POS-A518A580'),
	(2, 'COMPLETADA', '', '2025-11-13 07:12:54.397019', '2025-11-13 07:12:58.402907', 2, 'POS-A074FD78'),
	(3, 'COMPLETADA', '', '2025-11-13 07:13:22.956973', '2025-11-13 07:13:28.999677', 2, 'POS-5773F459'),
	(4, 'COMPLETADA', '', '2025-11-13 07:14:15.090431', '2025-11-13 07:15:08.346292', 2, 'POS-5773F459'),
	(5, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 07:18:35.087974', NULL, 2, 'POS-049D4502'),
	(6, 'COMPLETADA', '', '2025-11-13 07:19:39.944664', '2025-11-13 07:21:30.271004', 2, 'POS-A518A580'),
	(7, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 07:21:43.526031', NULL, 2, 'POS-8D0BAA4A'),
	(8, 'PROCESANDO', '', '2025-11-13 07:21:58.960741', NULL, 2, 'POS-41E8B8C7'),
	(9, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 14:15:31.797308', NULL, 2, 'POS-CDE476D4'),
	(10, 'COMPLETADA', '', '2025-11-13 14:15:56.956312', '2025-11-13 14:16:04.531638', 2, 'POS-CDE476D4'),
	(11, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 15:14:16.049903', NULL, 2, 'POS-CDE476D4');

-- Volcando estructura para tabla sistema_negocio.ventas_venta
CREATE TABLE IF NOT EXISTS `ventas_venta` (
  `id` varchar(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `nota` longtext NOT NULL,
  `cliente_documento` varchar(40) NOT NULL,
  `cliente_nombre` varchar(120) NOT NULL,
  `comprobante_pdf` varchar(100) DEFAULT NULL,
  `vendedor_id` int DEFAULT NULL,
  `actualizado` datetime(6) NOT NULL,
  `cliente_id` bigint DEFAULT NULL,
  `descuento_total_ars` decimal(12,2) NOT NULL,
  `impuestos_ars` decimal(12,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `subtotal_ars` decimal(12,2) NOT NULL,
  `total_ars` decimal(12,2) NOT NULL,
  `es_pago_mixto` tinyint(1) NOT NULL,
  `metodo_pago_2` varchar(20) DEFAULT NULL,
  `monto_pago_1` decimal(12,2) DEFAULT NULL,
  `monto_pago_2` decimal(12,2) DEFAULT NULL,
  `descuento_metodo_pago_ars` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_venta_vendedor_id_2f6b0d76_fk_auth_user_id` (`vendedor_id`),
  KEY `ventas_venta_cliente_id_85f33a80_fk_crm_cliente_id` (`cliente_id`),
  CONSTRAINT `ventas_venta_cliente_id_85f33a80_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`),
  CONSTRAINT `ventas_venta_vendedor_id_2f6b0d76_fk_auth_user_id` FOREIGN KEY (`vendedor_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla sistema_negocio.ventas_venta: ~49 rows (aproximadamente)
INSERT INTO `ventas_venta` (`id`, `fecha`, `metodo_pago`, `nota`, `cliente_documento`, `cliente_nombre`, `comprobante_pdf`, `vendedor_id`, `actualizado`, `cliente_id`, `descuento_total_ars`, `impuestos_ars`, `status`, `subtotal_ars`, `total_ars`, `es_pago_mixto`, `metodo_pago_2`, `monto_pago_1`, `monto_pago_2`, `descuento_metodo_pago_ars`) VALUES
	('1', '2025-11-11 20:09:48.089697', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-0686AF2B.pdf', NULL, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00),
	('2', '2025-11-11 20:13:01.217921', 'efectivo', '', '123123123', 'gordero 1', 'comprobantes/comprobante_POS-7C627328.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00),
	('3', '2025-11-11 20:22:27.187346', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-6A89ADAE.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00),
	('4', '2025-11-11 20:44:58.355407', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-88CA0C8B.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00),
	('5', '2025-11-12 15:22:13.767144', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-CF4E18B1.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00),
	('POS-00EA9703', '2025-11-12 22:17:54.183117', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-00EA9703.pdf', 2, '2025-11-12 22:17:54.346782', NULL, 0.00, 0.00, 'COMPLETADO', 50000.00, 50000.00, 0, NULL, NULL, NULL, 0.00),
	('POS-040397B8', '2025-11-13 04:02:07.491310', 'EFECTIVO_ARS', 'caca', '', 's', 'comprobantes/comprobante_POS-040397B8.pdf', 2, '2025-11-13 04:02:07.774856', 2, 2533.30, 1824.63, 'COMPLETADO', 11222.00, 10513.33, 0, NULL, NULL, NULL, 0.00),
	('POS-049D4502', '2025-11-13 07:17:04.318906', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-049D4502.pdf', 2, '2025-11-13 07:17:04.576610', NULL, 260794.50, 0.00, 'COMPLETADO', 1738630.00, 1477835.50, 0, NULL, NULL, NULL, 0.00),
	('POS-0E5CFD36', '2025-11-13 00:00:21.101847', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-0E5CFD36.pdf', 2, '2025-11-13 00:00:21.296106', NULL, 0.00, 0.00, 'COMPLETADO', 12222.00, 12222.00, 1, 'EFECTIVO_ARS', 1222.00, 11000.00, 0.00),
	('POS-119A299D', '2025-11-12 18:07:21.145364', 'EFECTIVO_USD', '', '', '', 'comprobantes/comprobante_POS-119A299D.pdf', 2, '2025-11-12 18:07:21.190508', NULL, 12.00, 2097.48, 'COMPLETADO', 10000.00, 12085.48, 0, NULL, NULL, NULL, 0.00),
	('POS-130AD6CE', '2025-11-12 23:23:04.328608', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-130AD6CE.pdf', 2, '2025-11-12 23:23:04.632146', NULL, 0.00, 0.00, 'COMPLETADO', 121.00, 121.00, 0, NULL, NULL, NULL, 0.00),
	('POS-1E7960FF', '2025-11-13 03:44:33.887235', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-1E7960FF.pdf', 2, '2025-11-13 03:44:34.102633', NULL, 0.00, 363117.30, 'COMPLETADO', 1729130.00, 2092247.30, 0, NULL, NULL, NULL, 0.00),
	('POS-20F0E7F3', '2025-11-13 07:23:37.277469', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-20F0E7F3.pdf', 2, '2025-11-13 07:23:37.458667', NULL, 0.00, 0.00, 'COMPLETADO', 9500.00, 9500.00, 0, NULL, NULL, NULL, 0.00),
	('POS-248DDA43', '2025-11-12 23:47:12.393869', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-248DDA43.pdf', 2, '2025-11-12 23:47:12.601363', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 0, NULL, NULL, NULL, 0.00),
	('POS-298C6FD3', '2025-11-12 20:41:38.952500', 'TRANSFERENCIA', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-298C6FD3.pdf', 2, '2025-11-12 20:41:39.122907', 1, 1222.00, 1843.38, 'COMPLETADO', 10000.00, 10621.38, 0, NULL, NULL, NULL, 0.00),
	('POS-3650B009', '2025-11-12 23:54:24.248014', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-3650B009.pdf', 2, '2025-11-12 23:54:24.431187', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 1, 'EFECTIVO_ARS', 122.00, 9878.00, 0.00),
	('POS-39941E37', '2025-11-12 22:07:47.675612', 'TRANSFERENCIA', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-39941E37.pdf', 2, '2025-11-12 22:07:47.844889', 1, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 0, NULL, NULL, NULL, 0.00),
	('POS-3BABAE79', '2025-11-12 19:21:00.021769', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-3BABAE79.pdf', 2, '2025-11-12 19:21:00.158587', NULL, 6060606.00, 1272727.26, 'COMPLETADO', 12121212.00, 7333333.26, 0, NULL, NULL, NULL, 0.00),
	('POS-41E8B8C7', '2025-11-13 05:27:20.990994', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-41E8B8C7.pdf', 2, '2025-11-13 05:27:21.142723', NULL, 975.00, 1160.25, 'CANCELADO', 6500.00, 6685.25, 0, NULL, NULL, NULL, 0.00),
	('POS-4B6258AE', '2025-11-12 18:41:40.039495', 'EFECTIVO_ARS', 'asdasd', '', '', 'comprobantes/comprobante_POS-4B6258AE.pdf', 2, '2025-11-12 18:41:40.155953', NULL, 12.00, 2097.48, 'COMPLETADO', 10000.00, 12085.48, 0, NULL, NULL, NULL, 0.00),
	('POS-553AE394', '2025-11-12 20:34:26.173955', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-553AE394.pdf', 2, '2025-11-12 20:34:26.326001', 1, 1200.00, 1848.00, 'COMPLETADO', 10000.00, 10648.00, 0, NULL, NULL, NULL, 0.00),
	('POS-5773F459', '2025-11-13 06:50:19.659311', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-5773F459.pdf', 2, '2025-11-13 06:50:20.269159', NULL, 1425.00, 0.00, 'CANCELADO', 9500.00, 8075.00, 0, NULL, NULL, NULL, 0.00),
	('POS-5BEC9024', '2025-11-12 20:52:37.049452', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-5BEC9024.pdf', 2, '2025-11-12 20:52:37.258244', NULL, 12.00, 0.00, 'COMPLETADO', 1500.00, 1488.00, 0, NULL, NULL, NULL, 0.00),
	('POS-5D3E5CE4', '2025-11-12 20:25:57.543526', 'TARJETA', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-5D3E5CE4.pdf', 2, '2025-11-12 20:25:57.699048', 1, 35.00, 66.15, 'COMPLETADO', 350.00, 381.15, 0, NULL, NULL, NULL, 0.00),
	('POS-6251D818', '2025-11-12 17:58:54.795182', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-6251D818.pdf', 2, '2025-11-12 17:58:54.866074', NULL, 12.00, 2097.48, 'COMPLETADO', 10000.00, 12085.48, 0, NULL, NULL, NULL, 0.00),
	('POS-65B108DF', '2025-11-12 21:38:39.249947', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-65B108DF.pdf', 2, '2025-11-12 21:38:39.400957', NULL, 1346.64, 2073.83, 'COMPLETADO', 11222.00, 11949.19, 0, NULL, NULL, NULL, 0.00),
	('POS-796712CB', '2025-11-12 20:53:08.464769', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-796712CB.pdf', 2, '2025-11-12 20:53:08.597025', NULL, 0.00, 0.00, 'COMPLETADO', 1999.00, 1999.00, 0, NULL, NULL, NULL, 0.00),
	('POS-8D0BAA4A', '2025-11-13 04:02:47.967546', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-8D0BAA4A.pdf', 2, '2025-11-13 04:02:48.166005', NULL, 0.00, 0.00, 'COMPLETADO', 11.00, 11.00, 0, NULL, NULL, NULL, 0.00),
	('POS-90825F5D', '2025-11-12 21:36:40.280224', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-90825F5D.pdf', 2, '2025-11-12 21:36:40.452042', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 0, NULL, NULL, NULL, 0.00),
	('POS-92C3F826', '2025-11-12 23:09:49.886234', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-92C3F826.pdf', 2, '2025-11-12 23:09:50.056432', NULL, 0.00, 0.00, 'COMPLETADO', 21212.00, 21212.00, 0, NULL, NULL, NULL, 0.00),
	('POS-9EB7FA22', '2025-11-12 22:13:24.934916', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-9EB7FA22.pdf', 2, '2025-11-12 22:13:25.102620', NULL, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 0, NULL, NULL, NULL, 0.00),
	('POS-A074FD78', '2025-11-13 05:33:48.483253', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-A074FD78.pdf', 2, '2025-11-13 05:33:48.634537', 1, 750.00, 10447.50, 'COMPLETADO', 50500.00, 60197.50, 1, 'TARJETA', 5000.00, 45500.00, 0.00),
	('POS-A4518974', '2025-11-12 22:01:07.471405', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-A4518974.pdf', 2, '2025-11-12 22:01:07.610354', NULL, 0.00, 0.00, 'COMPLETADO', 20000.00, 20000.00, 0, NULL, NULL, NULL, 0.00),
	('POS-A518A580', '2025-11-13 06:18:20.885089', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-A518A580.pdf', 2, '2025-11-13 06:18:21.049358', NULL, 0.00, 0.00, 'COMPLETADO', 9990.00, 9990.00, 0, NULL, NULL, NULL, 0.00),
	('POS-ABFC278E', '2025-11-12 23:43:15.684592', 'EFECTIVO_ARS', 'COn funda', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-ABFC278E.pdf', 2, '2025-11-12 23:43:15.918130', 1, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 1, 'TRANSFERENCIA', 250000.00, 1479130.00, 0.00),
	('POS-B0240418', '2025-11-12 20:00:17.929528', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B0240418.pdf', 2, '2025-11-12 20:00:18.038066', NULL, 1200.00, 1848.00, 'COMPLETADO', 10000.00, 10648.00, 0, NULL, NULL, NULL, 0.00),
	('POS-B627CAD1', '2025-11-12 18:14:47.961261', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B627CAD1.pdf', 2, '2025-11-12 18:14:48.098310', NULL, 0.00, 0.00, 'COMPLETADO', 12121212.00, 12121212.00, 0, NULL, NULL, NULL, 0.00),
	('POS-B80FE78F', '2025-11-12 22:21:27.655169', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B80FE78F.pdf', 2, '2025-11-12 22:21:27.782262', NULL, 0.00, 2545454.52, 'COMPLETADO', 12121212.00, 14666666.52, 0, NULL, NULL, NULL, 0.00),
	('POS-BE12561B', '2025-11-12 16:58:29.669824', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-BE12561B.pdf', 2, '2025-11-12 16:58:29.698736', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 0, NULL, NULL, NULL, 0.00),
	('POS-C21BAE7C', '2025-11-12 21:58:46.683945', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-C21BAE7C.pdf', 2, '2025-11-12 21:58:46.858811', NULL, 0.00, 363117.30, 'COMPLETADO', 1729130.00, 2092247.30, 0, NULL, NULL, NULL, 0.00),
	('POS-CB216F2A', '2025-11-12 18:04:34.598211', 'EFECTIVO_ARS', 'ascasc', '', '', 'comprobantes/comprobante_POS-CB216F2A.pdf', 2, '2025-11-12 18:04:34.648647', NULL, 1200.00, 1848.00, 'COMPLETADO', 10000.00, 10648.00, 0, NULL, NULL, NULL, 0.00),
	('POS-CDE476D4', '2025-11-13 14:15:02.716818', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-CDE476D4.pdf', 2, '2025-11-13 14:15:02.956888', 1, 1425.00, 1695.75, 'COMPLETADO', 9500.00, 9770.75, 1, 'EFECTIVO_ARS', 3500.00, 6000.00, 1425.00),
	('POS-D4BF06D2', '2025-11-13 07:42:42.517379', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-D4BF06D2.pdf', 2, '2025-11-13 07:42:42.701696', NULL, 840.00, 999.60, 'COMPLETADO', 5600.00, 5759.60, 0, NULL, NULL, NULL, 0.00),
	('POS-D990084C', '2025-11-12 23:41:57.742660', 'TRANSFERENCIA', 'hola asdasdasd', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-D990084C.pdf', 2, '2025-11-12 23:41:58.009839', 1, 0.00, 0.00, 'PENDIENTE_PAGO', 10000.00, 10000.00, 1, 'EFECTIVO_ARS', 1222.00, 8778.00, 0.00),
	('POS-DF47FA7E', '2025-11-12 21:53:35.425668', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-DF47FA7E.pdf', 2, '2025-11-12 21:53:35.623968', NULL, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 0, NULL, NULL, NULL, 0.00),
	('POS-ECB1CCF8', '2025-11-12 23:15:39.290686', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-ECB1CCF8.pdf', 2, '2025-11-12 23:15:39.505819', 1, 12.00, 2352.00, 'COMPLETADO', 11212.00, 13552.00, 0, NULL, NULL, NULL, 0.00),
	('POS-F5DB5517', '2025-11-12 20:10:17.624549', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-F5DB5517.pdf', 2, '2025-11-12 20:10:17.723034', 1, 11515163.40, 0.00, 'COMPLETADO', 12131212.00, 616048.60, 0, NULL, NULL, NULL, 0.00),
	('POS-F74FFB14', '2025-11-12 23:44:59.184877', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-F74FFB14.pdf', 2, '2025-11-12 23:44:59.357497', NULL, 0.00, 0.00, 'COMPLETADO', 1212.00, 1212.00, 0, NULL, NULL, NULL, 0.00),
	('POS-FE370894', '2025-11-12 23:06:06.550541', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-FE370894.pdf', 2, '2025-11-12 23:06:06.703033', 1, 12.00, 0.00, 'COMPLETADO', 1300.00, 1288.00, 0, NULL, NULL, NULL, 0.00);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
