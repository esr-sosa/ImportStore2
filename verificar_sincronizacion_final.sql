-- ============================================
-- VERIFICACIÓN FINAL DE SINCRONIZACIÓN
-- Confirma que todas las correcciones se aplicaron correctamente
-- ============================================

USE railway;

-- 1. Verificar cupon_id en ventas_venta
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;
SELECT '1. VERIFICACIÓN: cupon_id en ventas_venta' AS verificacion;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;

-- Verificar existencia
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ cupon_id EXISTE'
        ELSE '❌ cupon_id NO EXISTE'
    END AS estado_columna
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_venta'
  AND COLUMN_NAME = 'cupon_id';

-- Mostrar detalles
SELECT 
    COLUMN_NAME,
    COLUMN_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_venta'
  AND COLUMN_NAME = 'cupon_id';

SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ Índice EXISTE'
        ELSE '❌ Índice NO EXISTE'
    END AS estado_indice
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND INDEX_NAME = 'ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id';

SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ Foreign Key EXISTE'
        ELSE '❌ Foreign Key NO EXISTE'
    END AS estado_fk,
    CONSTRAINT_NAME
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_venta' 
  AND CONSTRAINT_NAME = 'ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

-- 2. Verificar foreign keys en ventas_historialestadoventa
SELECT '' AS espacio;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;
SELECT '2. VERIFICACIÓN: Foreign Keys en ventas_historialestadoventa' AS verificacion;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;

SELECT 
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ventas_historialestadoventa'
  AND CONSTRAINT_NAME IN (
    'ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id',
    'ventas_historialestadoventa_venta_id_4f46ae91_fk_ventas_venta_id'
  )
ORDER BY CONSTRAINT_NAME;

SELECT 
    CASE 
        WHEN COUNT(*) >= 2 THEN CONCAT('✅ ', COUNT(*), ' Foreign Key(s) EXISTEN')
        ELSE CONCAT('⚠️ Solo ', COUNT(*), ' Foreign Key(s) encontrado(s) - Se esperaban 2')
    END AS resumen_fks
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'ventas_historialestadoventa' 
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

-- 3. Verificar auth_user tiene PRIMARY KEY
SELECT '' AS espacio;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;
SELECT '3. VERIFICACIÓN: auth_user PRIMARY KEY' AS verificacion;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;

SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ auth_user.id tiene PRIMARY KEY'
        ELSE '❌ auth_user.id NO tiene PRIMARY KEY'
    END AS estado_pk
FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'auth_user' 
  AND COLUMN_NAME = 'id' 
  AND CONSTRAINT_NAME = 'PRIMARY';

-- 4. Resumen final
SELECT '' AS espacio;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;
SELECT '✅ RESUMEN FINAL' AS resumen;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS separador;

SELECT 
    'Si todas las verificaciones muestran ✅, la sincronización fue exitosa.' AS mensaje,
    'Reinicia la aplicación Django en Railway para aplicar los cambios.' AS siguiente_paso;

