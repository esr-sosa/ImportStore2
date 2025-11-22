-- ============================================
-- SQL PARA IMPORTAR EN MYSQL WORKBENCH
-- Usar: Server -> Data Import -> Import from Self-Contained File
-- ============================================

USE railway;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- TABLAS DE INVENTARIO
-- ============================================

-- 1. Categoría (sin dependencias, pero tiene self-reference)
DROP TABLE IF EXISTS `inventario_categoria`;
CREATE TABLE `inventario_categoria` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `parent_id` bigint(20) DEFAULT NULL,
  `descripcion` longtext NOT NULL DEFAULT '',
  `garantia_dias` int(10) UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_categoria_parent_id_idx` (`parent_id`),
  KEY `idx_categoria_nombre` (`nombre`),
  KEY `idx_categoria_parent` (`parent_id`),
  UNIQUE KEY `unique_categoria_nombre_parent` (`nombre`, `parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Agregar foreign key self-reference después de crear la tabla
ALTER TABLE `inventario_categoria`
  ADD CONSTRAINT `inventario_categoria_parent_id_fk` 
  FOREIGN KEY (`parent_id`) REFERENCES `inventario_categoria` (`id`) ON DELETE CASCADE;

-- 2. Proveedor (sin dependencias)
DROP TABLE IF EXISTS `inventario_proveedor`;
CREATE TABLE `inventario_proveedor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `contacto` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_proveedor_nombre_uniq` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Producto (depende de categoria y proveedor)
DROP TABLE IF EXISTS `inventario_producto`;
CREATE TABLE `inventario_producto` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `actualizado` datetime(6) DEFAULT NULL,
  `categoria_id` bigint(20) DEFAULT NULL,
  `proveedor_id` bigint(20) DEFAULT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'ACTIVO',
  `seo_descripcion` varchar(160) DEFAULT NULL,
  `seo_titulo` varchar(70) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `codigo_barras` varchar(64) DEFAULT NULL,
  `imagen_codigo_barras` varchar(255) DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_producto_categoria_id_idx` (`categoria_id`),
  KEY `inventario_producto_proveedor_id_idx` (`proveedor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. ProductoVariante (depende de producto)
DROP TABLE IF EXISTS `inventario_productovariante`;
CREATE TABLE `inventario_productovariante` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `producto_id` bigint(20) NOT NULL,
  `sku` varchar(64) NOT NULL,
  `nombre_variante` varchar(200) NOT NULL DEFAULT '',
  `codigo_barras` varchar(64) DEFAULT NULL,
  `qr_code` varchar(255) DEFAULT NULL,
  `atributo_1` varchar(120) NOT NULL DEFAULT '',
  `atributo_2` varchar(120) NOT NULL DEFAULT '',
  `stock_actual` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 0,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `stock` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `peso` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_productovariante_sku_uniq` (`sku`),
  KEY `inventario_productovariante_producto_id_idx` (`producto_id`),
  KEY `idx_var_sku` (`sku`),
  KEY `idx_var_activo` (`activo`),
  KEY `idx_var_stock` (`stock_actual`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Precio (depende de variante)
DROP TABLE IF EXISTS `inventario_precio`;
CREATE TABLE `inventario_precio` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL DEFAULT 'MINORISTA',
  `precio` decimal(12,2) NOT NULL,
  `moneda` varchar(10) NOT NULL DEFAULT 'USD',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `variante_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_precio_variante_id_idx` (`variante_id`),
  KEY `idx_precio_activo` (`activo`),
  KEY `idx_precio_var_tipo_mon` (`variante_id`, `tipo`, `moneda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLAS DE VENTAS
-- ============================================

-- 6. Cupón (sin dependencias)
DROP TABLE IF EXISTS `ventas_cupon`;
CREATE TABLE `ventas_cupon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `descripcion` varchar(200) NOT NULL DEFAULT '',
  `tipo_descuento` varchar(20) NOT NULL DEFAULT 'PORCENTAJE',
  `valor_descuento` decimal(10,2) NOT NULL,
  `monto_minimo` decimal(12,2) NOT NULL DEFAULT 0.00,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_fin` datetime(6) NOT NULL,
  `usos_maximos` int(11) NOT NULL DEFAULT 0,
  `usos_actuales` int(11) NOT NULL DEFAULT 0,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `solo_mayoristas` tinyint(1) NOT NULL DEFAULT 0,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ventas_cupon_codigo_uniq` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Venta (depende de cupon, cliente, vendedor - pero estos pueden no existir)
DROP TABLE IF EXISTS `ventas_venta`;
CREATE TABLE `ventas_venta` (
  `id` varchar(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `nota` longtext NOT NULL,
  `cliente_documento` varchar(40) NOT NULL DEFAULT '',
  `cliente_nombre` varchar(120) NOT NULL DEFAULT '',
  `comprobante_url` varchar(500) DEFAULT NULL,
  `vendedor_id` int(11) DEFAULT NULL,
  `cliente_id` bigint(20) DEFAULT NULL,
  `descuento_total_ars` decimal(12,2) NOT NULL DEFAULT 0.00,
  `impuestos_ars` decimal(12,2) NOT NULL DEFAULT 0.00,
  `status` varchar(30) NOT NULL DEFAULT 'PENDIENTE_PAGO',
  `subtotal_ars` decimal(12,2) NOT NULL DEFAULT 0.00,
  `total_ars` decimal(12,2) NOT NULL DEFAULT 0.00,
  `es_pago_mixto` tinyint(1) NOT NULL DEFAULT 0,
  `metodo_pago_2` varchar(20) DEFAULT NULL,
  `monto_pago_1` decimal(12,2) DEFAULT NULL,
  `monto_pago_2` decimal(12,2) DEFAULT NULL,
  `descuento_metodo_pago_ars` decimal(12,2) NOT NULL DEFAULT 0.00,
  `motivo_cancelacion` longtext DEFAULT NULL,
  `origen` varchar(10) NOT NULL DEFAULT 'POS',
  `estado_pago` varchar(20) NOT NULL DEFAULT 'pendiente',
  `estado_entrega` varchar(20) NOT NULL DEFAULT 'pendiente',
  `observaciones` longtext DEFAULT NULL,
  `descuento_cupon_ars` decimal(12,2) NOT NULL DEFAULT 0.00,
  `cupon_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_venta_cliente_id_idx` (`cliente_id`),
  KEY `ventas_venta_cupon_id_idx` (`cupon_id`),
  KEY `ventas_venta_vendedor_id_idx` (`vendedor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. DetalleVenta (depende de venta y variante)
DROP TABLE IF EXISTS `ventas_detalleventa`;
CREATE TABLE `ventas_detalleventa` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sku` varchar(60) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL,
  `precio_unitario_ars_congelado` decimal(12,2) NOT NULL,
  `subtotal_ars` decimal(12,2) NOT NULL,
  `variante_id` bigint(20) DEFAULT NULL,
  `venta_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_detalleventa_variante_id_idx` (`variante_id`),
  KEY `ventas_detalleventa_venta_id_idx` (`venta_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- AGREGAR FOREIGN KEYS
-- ============================================

-- Foreign keys de inventario_producto
ALTER TABLE `inventario_producto`
  ADD CONSTRAINT `inventario_producto_categoria_id_fk` 
  FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`) ON DELETE SET NULL;

ALTER TABLE `inventario_producto`
  ADD CONSTRAINT `inventario_producto_proveedor_id_fk` 
  FOREIGN KEY (`proveedor_id`) REFERENCES `inventario_proveedor` (`id`) ON DELETE SET NULL;

-- Foreign key de inventario_productovariante
ALTER TABLE `inventario_productovariante`
  ADD CONSTRAINT `inventario_productovariante_producto_id_fk` 
  FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`) ON DELETE CASCADE;

-- Foreign key de inventario_precio
ALTER TABLE `inventario_precio`
  ADD CONSTRAINT `inventario_precio_variante_id_fk` 
  FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`) ON DELETE CASCADE;

-- Foreign keys de ventas_detalleventa
ALTER TABLE `ventas_detalleventa`
  ADD CONSTRAINT `ventas_detalleventa_variante_id_fk` 
  FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`) ON DELETE SET NULL;

ALTER TABLE `ventas_detalleventa`
  ADD CONSTRAINT `ventas_detalleventa_venta_id_fk` 
  FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`) ON DELETE CASCADE;

-- Nota: Las foreign keys de ventas_venta (cliente_id, cupon_id, vendedor_id) 
-- se agregan solo si esas tablas existen. Si fallan, no es problema porque son opcionales.

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- VERIFICACIÓN
-- ============================================

SELECT '✅ Tablas creadas exitosamente' AS resultado;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'railway' 
AND table_name IN (
  'inventario_categoria',
  'inventario_proveedor',
  'inventario_producto',
  'inventario_productovariante',
  'inventario_precio',
  'ventas_cupon',
  'ventas_venta',
  'ventas_detalleventa'
)
ORDER BY table_name;

