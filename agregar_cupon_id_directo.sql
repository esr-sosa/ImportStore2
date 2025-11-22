-- ============================================
-- AGREGAR cupon_id A ventas_venta (MÉTODO DIRECTO)
-- Ejecutar en MySQL Workbench
-- ============================================

USE railway;

-- Verificar si la columna existe
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ La columna cupon_id YA EXISTE'
        ELSE '❌ La columna cupon_id NO EXISTE'
    END AS estado
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_venta'
  AND COLUMN_NAME = 'cupon_id';

-- Ver estructura actual de ventas_venta
SELECT 
    COLUMN_NAME,
    COLUMN_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_KEY
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_venta'
  AND COLUMN_NAME IN ('descuento_cupon_ars', 'cupon_id', 'observaciones')
ORDER BY ORDINAL_POSITION;

-- Intentar agregar la columna (usando procedimiento para manejar errores)
SET FOREIGN_KEY_CHECKS = 0;

DELIMITER //
CREATE PROCEDURE AddCuponIdColumn()
BEGIN
    DECLARE column_exists INT DEFAULT 0;
    
    -- Verificar si la columna existe
    SELECT COUNT(*) INTO column_exists
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'ventas_venta'
      AND COLUMN_NAME = 'cupon_id';
    
    -- Si no existe, agregarla
    IF column_exists = 0 THEN
        -- Intentar agregar después de descuento_cupon_ars
        SET @sql = 'ALTER TABLE `ventas_venta` ADD COLUMN `cupon_id` bigint(20) DEFAULT NULL';
        
        -- Verificar si existe la columna descuento_cupon_ars para usarla como referencia
        SET @ref_col_exists = 0;
        SELECT COUNT(*) INTO @ref_col_exists
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'ventas_venta'
          AND COLUMN_NAME = 'descuento_cupon_ars';
        
        IF @ref_col_exists > 0 THEN
            SET @sql = CONCAT(@sql, ' AFTER `descuento_cupon_ars`');
        END IF;
        
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SELECT '✅ Columna cupon_id agregada exitosamente' AS resultado;
    ELSE
        SELECT 'ℹ️ Columna cupon_id ya existe' AS resultado;
    END IF;
END //
DELIMITER ;

CALL AddCuponIdColumn();
DROP PROCEDURE AddCuponIdColumn;

-- Agregar índice si no existe
SET @idx_exists = (
    SELECT COUNT(*) 
    FROM information_schema.STATISTICS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_venta' 
      AND INDEX_NAME = 'ventas_venta_cupon_id_idx'
);

SET @sql = IF(@idx_exists = 0,
    'ALTER TABLE `ventas_venta` ADD KEY `ventas_venta_cupon_id_idx` (`cupon_id`)',
    'SELECT "Índice ya existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key si ventas_cupon existe
SET @cupon_table_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_cupon'
);

SET @fk_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLE_CONSTRAINTS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'ventas_venta' 
      AND CONSTRAINT_NAME = 'ventas_venta_cupon_id_fk' 
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

SET @sql = IF(@cupon_table_exists > 0 AND @fk_exists = 0,
    'ALTER TABLE `ventas_venta` ADD CONSTRAINT `ventas_venta_cupon_id_fk` FOREIGN KEY (`cupon_id`) REFERENCES `ventas_cupon` (`id`) ON DELETE SET NULL',
    'SELECT "Foreign key ya existe o ventas_cupon no existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;

-- Verificar resultado final
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ cupon_id agregada exitosamente'
        ELSE '❌ ERROR: cupon_id NO se pudo agregar'
    END AS resultado_final
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_venta'
  AND COLUMN_NAME = 'cupon_id';

