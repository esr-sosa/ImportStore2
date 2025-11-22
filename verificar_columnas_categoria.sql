-- ============================================
-- VERIFICAR ESTRUCTURA DE inventario_categoria
-- ============================================

USE railway;

-- Ver todas las columnas de inventario_categoria
SELECT 
    COLUMN_NAME,
    COLUMN_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_KEY,
    EXTRA
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'inventario_categoria'
ORDER BY ORDINAL_POSITION;

-- Verificar si existen las columnas necesarias
SELECT 
    CASE WHEN COUNT(*) > 0 THEN '✅ Existe' ELSE '❌ No existe' END AS parent_id,
    CASE WHEN COUNT(*) > 0 THEN '✅ Existe' ELSE '❌ No existe' END AS descripcion,
    CASE WHEN COUNT(*) > 0 THEN '✅ Existe' ELSE '❌ No existe' END AS garantia_dias
FROM (
    SELECT 'parent_id' AS columna, COUNT(*) AS cnt
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'inventario_categoria'
      AND COLUMN_NAME = 'parent_id'
    UNION ALL
    SELECT 'descripcion' AS columna, COUNT(*) AS cnt
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'inventario_categoria'
      AND COLUMN_NAME = 'descripcion'
    UNION ALL
    SELECT 'garantia_dias' AS columna, COUNT(*) AS cnt
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'inventario_categoria'
      AND COLUMN_NAME = 'garantia_dias'
) AS checks;

