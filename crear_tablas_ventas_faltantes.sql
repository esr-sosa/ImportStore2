-- ============================================
-- SQL PARA CREAR TABLAS FALTANTES DE VENTAS
-- Ejecutar en MySQL Workbench para crear las tablas que faltan
-- ============================================

USE railway;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. CREAR TABLA ventas_carritoremoto
-- ============================================

DROP TABLE IF EXISTS `ventas_carritoremoto`;

-- Crear tabla sin foreign key primero
CREATE TABLE `ventas_carritoremoto` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `items` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`items`)),
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ventas_carritoremoto_usuario_id_uniq` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Agregar foreign key después (solo si auth_user existe)
SET @user_table_exists = 0;
SELECT COUNT(*) INTO @user_table_exists 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'auth_user';

SET @fk_exists = 0;
SELECT COUNT(*) INTO @fk_exists 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE CONSTRAINT_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_carritoremoto' 
  AND CONSTRAINT_NAME = 'ventas_carritoremoto_usuario_id_fk' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql = IF(@user_table_exists > 0 AND @fk_exists = 0,
  'ALTER TABLE `ventas_carritoremoto` ADD CONSTRAINT `ventas_carritoremoto_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE',
  'SELECT "Foreign key ventas_carritoremoto_usuario_id_fk ya existe o auth_user no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================
-- 2. CREAR TABLA ventas_solicitudimpresion
-- ============================================

DROP TABLE IF EXISTS `ventas_solicitudimpresion`;

-- Crear tabla sin foreign keys primero
CREATE TABLE `ventas_solicitudimpresion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `estado` varchar(20) NOT NULL,
  `error` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `procesado` datetime(6) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `venta_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_solicitudimpresion_usuario_id_idx` (`usuario_id`),
  KEY `ventas_solicitudimpresion_venta_id_idx` (`venta_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Agregar foreign key a auth_user (solo si existe)
SET @user_table_exists = 0;
SELECT COUNT(*) INTO @user_table_exists 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'auth_user';

SET @fk_exists = 0;
SELECT COUNT(*) INTO @fk_exists 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE CONSTRAINT_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_solicitudimpresion' 
  AND CONSTRAINT_NAME = 'ventas_solicitudimpresion_usuario_id_fk' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql = IF(@user_table_exists > 0 AND @fk_exists = 0,
  'ALTER TABLE `ventas_solicitudimpresion` ADD CONSTRAINT `ventas_solicitudimpresion_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE',
  'SELECT "Foreign key ventas_solicitudimpresion_usuario_id_fk ya existe o auth_user no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key a ventas_venta (solo si existe)
SET @venta_table_exists = 0;
SELECT COUNT(*) INTO @venta_table_exists 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta';

SET @fk_exists = 0;
SELECT COUNT(*) INTO @fk_exists 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE CONSTRAINT_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_solicitudimpresion' 
  AND CONSTRAINT_NAME = 'ventas_solicitudimpresion_venta_id_fk' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql = IF(@venta_table_exists > 0 AND @fk_exists = 0,
  'ALTER TABLE `ventas_solicitudimpresion` ADD CONSTRAINT `ventas_solicitudimpresion_venta_id_fk` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`) ON DELETE CASCADE',
  'SELECT "Foreign key ventas_solicitudimpresion_venta_id_fk ya existe o ventas_venta no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================
-- 3. AGREGAR COLUMNA cupon_id A ventas_venta
-- ============================================

-- Verificar si la columna ya existe antes de agregarla
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND COLUMN_NAME = 'cupon_id';

SET @sql = IF(@col_exists = 0,
  'ALTER TABLE `ventas_venta` ADD COLUMN `cupon_id` bigint(20) DEFAULT NULL AFTER `descuento_cupon_ars`',
  'SELECT "Columna cupon_id ya existe en ventas_venta" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar índice y foreign key si la columna fue creada
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND COLUMN_NAME = 'cupon_id';

SET @fk_exists = 0;
SELECT COUNT(*) INTO @fk_exists 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE CONSTRAINT_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND CONSTRAINT_NAME = 'ventas_venta_cupon_id_fk' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

-- Agregar índice si no existe
SET @idx_exists = 0;
SELECT COUNT(*) INTO @idx_exists 
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND INDEX_NAME = 'ventas_venta_cupon_id_idx';

SET @sql = IF(@col_exists > 0 AND @idx_exists = 0,
  'ALTER TABLE `ventas_venta` ADD KEY `ventas_venta_cupon_id_idx` (`cupon_id`)',
  'SELECT "Índice ventas_venta_cupon_id_idx ya existe o columna no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key si no existe
SET @fk_exists = 0;
SELECT COUNT(*) INTO @fk_exists 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE CONSTRAINT_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND CONSTRAINT_NAME = 'ventas_venta_cupon_id_fk' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql = IF(@col_exists > 0 AND @fk_exists = 0,
  'ALTER TABLE `ventas_venta` ADD CONSTRAINT `ventas_venta_cupon_id_fk` FOREIGN KEY (`cupon_id`) REFERENCES `ventas_cupon` (`id`) ON DELETE SET NULL',
  'SELECT "Foreign key ventas_venta_cupon_id_fk ya existe o columna no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- VERIFICACIÓN
-- ============================================

SELECT '✅ Tablas y columnas creadas exitosamente' AS resultado;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'railway' 
AND table_name IN (
  'ventas_carritoremoto',
  'ventas_solicitudimpresion'
)
ORDER BY table_name;

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'railway' 
AND table_name = 'ventas_venta' 
AND column_name = 'cupon_id';

