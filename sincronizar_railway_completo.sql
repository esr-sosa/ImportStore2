-- ============================================
-- SCRIPT DE SINCRONIZACIÓN COMPLETO
-- Sincroniza Railway con la base de datos original
-- Basado en comparación entre sistema_negocio.sql y Untitled.sql
-- ============================================

USE railway;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. AGREGAR cupon_id A ventas_venta
-- ============================================
SET @col_exists = (
    SELECT COUNT(*) 
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'ventas_venta'
      AND COLUMN_NAME = 'cupon_id'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE `ventas_venta` ADD COLUMN `cupon_id` bigint(20) DEFAULT NULL AFTER `descuento_cupon_ars`',
    'SELECT "Columna cupon_id ya existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar índice para cupon_id
SET @idx_exists = (
    SELECT COUNT(*) 
    FROM information_schema.STATISTICS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_venta' 
      AND INDEX_NAME = 'ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id'
);

SET @sql = IF(@idx_exists = 0,
    'ALTER TABLE `ventas_venta` ADD KEY `ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id` (`cupon_id`)',
    'SELECT "Índice cupon_id ya existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key para cupon_id
SET @fk_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLE_CONSTRAINTS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_venta' 
      AND CONSTRAINT_NAME = 'ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id' 
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

SET @cupon_table_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_cupon'
);

SET @sql = IF(@fk_exists = 0 AND @cupon_table_exists > 0,
    'ALTER TABLE `ventas_venta` ADD CONSTRAINT `ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id` FOREIGN KEY (`cupon_id`) REFERENCES `ventas_cupon` (`id`) ON DELETE SET NULL',
    'SELECT "Foreign key cupon_id ya existe o ventas_cupon no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================
-- 2. AGREGAR FOREIGN KEYS A ventas_historialestadoventa
-- ============================================

-- Verificar que la tabla existe
SET @table_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa'
);

-- Verificar que auth_user tiene PRIMARY KEY
SET @auth_user_pk = (
    SELECT COUNT(*) 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'auth_user' 
      AND COLUMN_NAME = 'id' 
      AND CONSTRAINT_NAME = 'PRIMARY'
);

-- Si auth_user no tiene PK, agregarla
SET @sql = IF(@auth_user_pk = 0,
    'ALTER TABLE `auth_user` ADD PRIMARY KEY (`id`)',
    'SELECT "auth_user ya tiene PRIMARY KEY" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key usuario_id
SET @fk_usuario_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLE_CONSTRAINTS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa' 
      AND CONSTRAINT_NAME = 'ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id' 
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

SET @sql = IF(@table_exists > 0 AND @fk_usuario_exists = 0,
    'ALTER TABLE `ventas_historialestadoventa` ADD CONSTRAINT `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL',
    'SELECT "Foreign key usuario_id ya existe o tabla no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key venta_id
SET @fk_venta_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLE_CONSTRAINTS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa' 
      AND CONSTRAINT_NAME = 'ventas_historialestadoventa_venta_id_4f46ae91_fk_ventas_venta_id' 
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

SET @venta_table_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_venta'
);

SET @venta_pk = (
    SELECT COUNT(*) 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_venta' 
      AND COLUMN_NAME = 'id' 
      AND CONSTRAINT_NAME = 'PRIMARY'
);

SET @sql = IF(@table_exists > 0 AND @fk_venta_exists = 0 AND @venta_table_exists > 0 AND @venta_pk > 0,
    'ALTER TABLE `ventas_historialestadoventa` ADD CONSTRAINT `ventas_historialestadoventa_venta_id_4f46ae91_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`) ON DELETE CASCADE',
    'SELECT "Foreign key venta_id ya existe, tabla no existe, o ventas_venta no tiene PK" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 3. VERIFICACIÓN FINAL
-- ============================================

SELECT '✅ Verificación de cupon_id en ventas_venta' AS verificacion;
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ cupon_id EXISTE'
        ELSE '❌ cupon_id NO EXISTE'
    END AS estado
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_venta'
  AND COLUMN_NAME = 'cupon_id';

SELECT '✅ Verificación de foreign keys en ventas_historialestadoventa' AS verificacion;
SELECT 
    CASE 
        WHEN COUNT(*) >= 2 THEN '✅ Foreign keys EXISTEN'
        ELSE CONCAT('⚠️ Solo ', COUNT(*), ' foreign key(s) encontrado(s)')
    END AS estado
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_historialestadoventa' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SELECT '✅ Script de sincronización completado' AS mensaje_final;

