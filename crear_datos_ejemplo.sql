-- ============================================
-- SQL PARA CREAR DATOS DE EJEMPLO
-- Ejecutar en MySQL Workbench para tener productos de prueba
-- ============================================

USE railway;

-- Crear categorías de ejemplo
INSERT INTO `inventario_categoria` (`id`, `nombre`, `parent_id`, `descripcion`, `garantia_dias`) VALUES
(1, 'Accesorios', NULL, 'Accesorios para dispositivos móviles', 90),
(2, 'Celulares', NULL, 'Teléfonos celulares y smartphones', 365),
(3, 'Fundas', 1, 'Fundas y protectores', 90)
ON DUPLICATE KEY UPDATE nombre=nombre;

-- Crear proveedor de ejemplo
INSERT INTO `inventario_proveedor` (`id`, `nombre`, `contacto`, `telefono`, `email`, `fecha_creacion`, `activo`) VALUES
(1, 'Proveedor Principal', 'Juan Pérez', '1234567890', 'proveedor@example.com', NOW(), 1)
ON DUPLICATE KEY UPDATE nombre=nombre;

-- Crear productos de ejemplo
INSERT INTO `inventario_producto` (`id`, `nombre`, `descripcion`, `actualizado`, `categoria_id`, `proveedor_id`, `estado`, `seo_descripcion`, `seo_titulo`, `activo`, `codigo_barras`, `imagen_codigo_barras`, `creado`) VALUES
(1, 'Cargador 20w', 'Cargador rápido de 20W para iPhone', NOW(), 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, NOW()),
(2, 'iPhone 15 Pro', 'iPhone 15 Pro 256GB', NOW(), 2, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, NOW()),
(3, 'Funda Protectora', 'Funda protectora para iPhone', NOW(), 3, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, NOW())
ON DUPLICATE KEY UPDATE nombre=nombre;

-- Crear variantes de ejemplo
INSERT INTO `inventario_productovariante` (`id`, `producto_id`, `sku`, `nombre_variante`, `codigo_barras`, `qr_code`, `atributo_1`, `atributo_2`, `stock_actual`, `stock_minimo`, `activo`, `creado`, `actualizado`, `stock`, `peso`) VALUES
(1, 1, 'CARG-20W-001', 'Cargador 20W Blanco', NULL, NULL, 'Color', 'Blanco', 10, 2, 1, NOW(), NOW(), 10, 0.10),
(2, 1, 'CARG-20W-002', 'Cargador 20W Negro', NULL, NULL, 'Color', 'Negro', 15, 2, 1, NOW(), NOW(), 15, 0.10),
(3, 2, 'IPHONE-15-PRO-256GB-TITANIO', 'iPhone 15 Pro 256GB Titanio Natural', NULL, NULL, 'Capacidad', '256GB', 5, 1, 1, NOW(), NOW(), 5, 0.20),
(4, 3, 'FUNDA-IPHONE-001', 'Funda Protectora Transparente', NULL, NULL, 'Tipo', 'Transparente', 20, 5, 1, NOW(), NOW(), 20, 0.05)
ON DUPLICATE KEY UPDATE sku=sku;

-- Crear precios de ejemplo
INSERT INTO `inventario_precio` (`id`, `variante_id`, `tipo`, `precio`, `moneda`, `activo`, `creado`, `actualizado`) VALUES
(1, 1, 'MINORISTA', 15000.00, 'ARS', 1, NOW(), NOW()),
(2, 1, 'MAYORISTA', 12000.00, 'ARS', 1, NOW(), NOW()),
(3, 2, 'MINORISTA', 15000.00, 'ARS', 1, NOW(), NOW()),
(4, 2, 'MAYORISTA', 12000.00, 'ARS', 1, NOW(), NOW()),
(5, 3, 'MINORISTA', 1200000.00, 'ARS', 1, NOW(), NOW()),
(6, 3, 'MAYORISTA', 1000000.00, 'ARS', 1, NOW(), NOW()),
(7, 4, 'MINORISTA', 5000.00, 'ARS', 1, NOW(), NOW()),
(8, 4, 'MAYORISTA', 4000.00, 'ARS', 1, NOW(), NOW())
ON DUPLICATE KEY UPDATE precio=precio;

-- Verificar datos creados
SELECT '✅ Datos de ejemplo creados' AS resultado;

SELECT 
  p.id,
  p.nombre AS producto,
  c.nombre AS categoria,
  COUNT(v.id) AS variantes,
  SUM(v.stock_actual) AS stock_total
FROM inventario_producto p
LEFT JOIN inventario_categoria c ON p.categoria_id = c.id
LEFT JOIN inventario_productovariante v ON v.producto_id = p.id
WHERE p.activo = 1
GROUP BY p.id, p.nombre, c.nombre
ORDER BY p.nombre;

