-- ============================================
-- SQL PARA AGREGAR COLUMNAS FALTANTES
-- Ejecutar en MySQL Workbench después de crear las tablas
-- ============================================

USE railway;

-- Agregar columnas faltantes a inventario_productovariante
-- Verificar y agregar qr_code
SET @col_exists = (
  SELECT COUNT(*) 
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_productovariante' 
  AND COLUMN_NAME = 'qr_code'
);

SET @sql = IF(@col_exists = 0,
  'ALTER TABLE `inventario_productovariante` ADD COLUMN `qr_code` varchar(255) DEFAULT NULL AFTER `codigo_barras`;',
  'SELECT "Columna qr_code ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar y agregar nombre_variante (si no existe o tiene tamaño incorrecto)
SET @col_exists = (
  SELECT COUNT(*) 
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_productovariante' 
  AND COLUMN_NAME = 'nombre_variante'
);

SET @sql = IF(@col_exists = 0,
  'ALTER TABLE `inventario_productovariante` ADD COLUMN `nombre_variante` varchar(200) NOT NULL DEFAULT "" AFTER `sku`;',
  'SELECT "Columna nombre_variante ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Si nombre_variante existe pero tiene tamaño incorrecto, modificarla
SET @col_size = (
  SELECT CHARACTER_MAXIMUM_LENGTH
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = 'railway'
  AND TABLE_NAME = 'inventario_productovariante'
  AND COLUMN_NAME = 'nombre_variante'
);

SET @sql = IF(@col_size IS NOT NULL AND @col_size < 200,
  'ALTER TABLE `inventario_productovariante` MODIFY COLUMN `nombre_variante` varchar(200) NOT NULL DEFAULT "";',
  'SELECT "Columna nombre_variante tiene tamaño correcto" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar columnas agregadas
SELECT 
  COLUMN_NAME,
  DATA_TYPE,
  CHARACTER_MAXIMUM_LENGTH,
  IS_NULLABLE,
  COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'railway'
AND TABLE_NAME = 'inventario_productovariante'
AND COLUMN_NAME IN ('qr_code', 'nombre_variante', 'sku', 'stock_actual', 'stock_minimo', 'activo')
ORDER BY COLUMN_NAME;

SELECT '✅ Columnas verificadas/agregadas exitosamente' AS resultado;

