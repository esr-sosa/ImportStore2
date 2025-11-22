-- ============================================
-- SQL PARA AGREGAR COLUMNAS FALTANTES A inventario_categoria
-- Ejecutar en MySQL Workbench
-- ============================================

USE railway;

-- Agregar parent_id si no existe
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

-- Agregar descripcion si no existe
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

-- Agregar garantia_dias si no existe
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

-- Modificar nombre para que sea varchar(120) (si no lo es ya)
SET @col_size = (
  SELECT CHARACTER_MAXIMUM_LENGTH
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = 'railway'
  AND TABLE_NAME = 'inventario_categoria'
  AND COLUMN_NAME = 'nombre'
);

SET @sql = IF(@col_size IS NOT NULL AND @col_size < 120,
  'ALTER TABLE `inventario_categoria` MODIFY COLUMN `nombre` varchar(120) NOT NULL;',
  'SELECT "Columna nombre ya tiene tamaño correcto" AS mensaje;'
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

-- Agregar índice idx_categoria_parent si no existe
SET @idx_exists = (
  SELECT COUNT(*) 
  FROM information_schema.STATISTICS 
  WHERE TABLE_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_categoria' 
  AND INDEX_NAME = 'idx_categoria_parent'
);

SET @sql = IF(@idx_exists = 0,
  'ALTER TABLE `inventario_categoria` ADD KEY `idx_categoria_parent` (`parent_id`);',
  'SELECT "Índice idx_categoria_parent ya existe" AS mensaje;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar unique constraint si no existe
SET @unique_exists = (
  SELECT COUNT(*) 
  FROM information_schema.TABLE_CONSTRAINTS 
  WHERE CONSTRAINT_SCHEMA = 'railway' 
  AND TABLE_NAME = 'inventario_categoria' 
  AND CONSTRAINT_NAME = 'unique_categoria_nombre_parent'
);

SET @sql = IF(@unique_exists = 0,
  'ALTER TABLE `inventario_categoria` ADD UNIQUE KEY `unique_categoria_nombre_parent` (`nombre`, `parent_id`);',
  'SELECT "Unique constraint unique_categoria_nombre_parent ya existe" AS mensaje;'
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
AND TABLE_NAME = 'inventario_categoria'
ORDER BY ORDINAL_POSITION;

SELECT '✅ Columnas de inventario_categoria verificadas/agregadas exitosamente' AS resultado;

