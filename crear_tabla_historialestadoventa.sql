-- ============================================
-- CREAR TABLA ventas_historialestadoventa
-- Resuelve el error: Table 'railway.ventas_historialestadoventa' doesn't exist
-- ============================================

USE railway;

SET FOREIGN_KEY_CHECKS = 0;

-- Verificar si la tabla existe
SET @table_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa'
);

-- Crear tabla si no existe
SET @sql = IF(@table_exists = 0,
    'CREATE TABLE `ventas_historialestadoventa` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `estado_anterior` varchar(30) DEFAULT NULL,
      `estado_nuevo` varchar(30) NOT NULL,
      `nota` longtext DEFAULT NULL,
      `creado` datetime(6) NOT NULL,
      `usuario_id` int(11) DEFAULT NULL,
      `venta_id` varchar(20) NOT NULL,
      PRIMARY KEY (`id`),
      KEY `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` (`usuario_id`),
      KEY `ventas_hist_venta_i_65b196_idx` (`venta_id`, `creado`),
      CONSTRAINT `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL,
      CONSTRAINT `ventas_historialestadoventa_venta_id_4f46ae91_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci',
    'SELECT "Tabla ventas_historialestadoventa ya existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Si la tabla ya existe, verificar y agregar índices/foreign keys faltantes
-- Verificar si existe el índice de usuario
SET @idx_usuario_exists = (
    SELECT COUNT(*) 
    FROM information_schema.STATISTICS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa' 
      AND INDEX_NAME = 'ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id'
);

SET @sql = IF(@table_exists > 0 AND @idx_usuario_exists = 0,
    'ALTER TABLE `ventas_historialestadoventa` ADD KEY `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` (`usuario_id`)',
    'SELECT "Índice usuario ya existe o tabla no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar si existe el índice compuesto
SET @idx_venta_exists = (
    SELECT COUNT(*) 
    FROM information_schema.STATISTICS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa' 
      AND INDEX_NAME = 'ventas_hist_venta_i_65b196_idx'
);

SET @sql = IF(@table_exists > 0 AND @idx_venta_exists = 0,
    'ALTER TABLE `ventas_historialestadoventa` ADD KEY `ventas_hist_venta_i_65b196_idx` (`venta_id`, `creado`)',
    'SELECT "Índice venta ya existe o tabla no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar si existe el foreign key de usuario
SET @fk_usuario_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLE_CONSTRAINTS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_historialestadoventa' 
      AND CONSTRAINT_NAME = 'ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id' 
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

-- Verificar que auth_user existe y tiene PRIMARY KEY
SET @auth_user_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'auth_user'
);

SET @auth_user_pk = (
    SELECT COUNT(*) 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'auth_user' 
      AND COLUMN_NAME = 'id' 
      AND CONSTRAINT_NAME = 'PRIMARY'
);

SET @sql = IF(@table_exists > 0 AND @fk_usuario_exists = 0 AND @auth_user_exists > 0 AND @auth_user_pk > 0,
    'ALTER TABLE `ventas_historialestadoventa` ADD CONSTRAINT `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL',
    'SELECT "Foreign key usuario ya existe, tabla no existe, o auth_user no tiene PK" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar si existe el foreign key de venta
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
    'SELECT "Foreign key venta ya existe, tabla no existe, o ventas_venta no tiene PK" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;

-- Verificar resultado final
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ Tabla ventas_historialestadoventa EXISTE'
        ELSE '❌ ERROR: Tabla NO se pudo crear'
    END AS estado_final
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_historialestadoventa';

-- Mostrar estructura de la tabla
SELECT 
    COLUMN_NAME,
    COLUMN_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_KEY,
    EXTRA
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_historialestadoventa'
ORDER BY ORDINAL_POSITION;

