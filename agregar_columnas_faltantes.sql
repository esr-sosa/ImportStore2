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

-- Agregar columnas faltantes a inventario_categoria
-- Verificar y agregar parent_id
SET @col_exists = (
  SELECT COUNT(*) 
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_categoria' 
  AND COLUMN_NAME = 'parent_id'
);

SET @sql = IF(@col_exists = 0,
  'ALTER TABLE `inventario_categoria` ADD COLUMN `parent_id` bigint(20) DEFAULT NULL AFTER `nombre`;',
  'SELECT "Columna parent_id ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar y agregar descripcion
SET @col_exists = (
  SELECT COUNT(*) 
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_categoria' 
  AND COLUMN_NAME = 'descripcion'
);

SET @sql = IF(@col_exists = 0,
  'ALTER TABLE `inventario_categoria` ADD COLUMN `descripcion` longtext NOT NULL AFTER `parent_id`;',
  'SELECT "Columna descripcion ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar y agregar garantia_dias
SET @col_exists = (
  SELECT COUNT(*) 
  FROM information_schema.COLUMNS 
  WHERE TABLE_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_categoria' 
  AND COLUMN_NAME = 'garantia_dias'
);

SET @sql = IF(@col_exists = 0,
  'ALTER TABLE `inventario_categoria` ADD COLUMN `garantia_dias` int(10) UNSIGNED DEFAULT NULL AFTER `descripcion`;',
  'SELECT "Columna garantia_dias ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key self-reference si no existe
SET @fk_exists = (
  SELECT COUNT(*) 
  FROM information_schema.TABLE_CONSTRAINTS 
  WHERE CONSTRAINT_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_categoria' 
  AND CONSTRAINT_NAME = 'inventario_categoria_parent_id_fk'
);

SET @sql = IF(@fk_exists = 0,
  'ALTER TABLE `inventario_categoria` ADD CONSTRAINT `inventario_categoria_parent_id_fk` FOREIGN KEY (`parent_id`) REFERENCES `inventario_categoria` (`id`) ON DELETE CASCADE;',
  'SELECT "Foreign key parent_id ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Modificar nombre para que sea varchar(120) en lugar de 100
ALTER TABLE `inventario_categoria` 
  MODIFY COLUMN `nombre` varchar(120) NOT NULL;

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

SELECT 
  COLUMN_NAME,
  DATA_TYPE,
  CHARACTER_MAXIMUM_LENGTH,
  IS_NULLABLE,
  COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'railway'
AND TABLE_NAME = 'inventario_categoria'
AND COLUMN_NAME IN ('parent_id', 'descripcion', 'garantia_dias', 'nombre')
ORDER BY COLUMN_NAME;

SELECT '✅ Columnas verificadas/agregadas exitosamente' AS resultado;

