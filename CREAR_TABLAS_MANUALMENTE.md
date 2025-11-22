# Crear Tablas Manualmente en MySQL Workbench

Si las migraciones automáticas fallan, puedes crear las tablas manualmente ejecutando el SQL de las migraciones iniciales.

## Opción 1: Generar SQL desde tu máquina local

1. **Conéctate a tu base de datos Railway desde tu máquina local:**
   ```bash
   # Obtén las credenciales de Railway MySQL
   # Luego ejecuta estos comandos localmente:
   cd sistema_negocio
   python manage.py sqlmigrate inventario 0001 > inventario_0001.sql
   python manage.py sqlmigrate ventas 0001 > ventas_0001.sql
   ```

2. **Abre los archivos `.sql` generados y copia el contenido**

3. **En MySQL Workbench:**
   - Conéctate a tu base de datos Railway
   - Selecciona la base de datos `railway`
   - Abre una nueva pestaña de SQL
   - Pega el SQL copiado
   - Ejecuta (Ctrl+Enter o botón Execute)

## Opción 2: Usar el comando generate_create_tables_sql

1. **Ejecuta el comando localmente:**
   ```bash
   cd sistema_negocio
   python manage.py generate_create_tables_sql
   ```

2. **Sigue las instrucciones que muestra el comando**

## Opción 3: Ejecutar SQL directamente en MySQL Workbench

Si prefieres, puedes ejecutar este SQL directamente (ajusta según tu esquema):

```sql
-- Primero, asegúrate de estar en la base de datos correcta
USE railway;

-- Crear tabla inventario_categoria (si no existe)
CREATE TABLE IF NOT EXISTS `inventario_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla inventario_proveedor (si no existe)
CREATE TABLE IF NOT EXISTS `inventario_proveedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL UNIQUE,
  `contacto` varchar(150),
  `telefono` varchar(20),
  `email` varchar(254),
  `fecha_creacion` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla inventario_producto (si no existe)
CREATE TABLE IF NOT EXISTS `inventario_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `descripcion` longtext,
  `codigo_barras` varchar(13) UNIQUE,
  `imagen_codigo_barras` varchar(100),
  `fecha_creacion` datetime(6) NOT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL,
  `categoria_id` bigint,
  `proveedor_id` bigint,
  PRIMARY KEY (`id`),
  KEY `inventario_producto_categoria_id_fk` (`categoria_id`),
  KEY `inventario_producto_proveedor_id_fk` (`proveedor_id`),
  CONSTRAINT `inventario_producto_categoria_id_fk` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`) ON DELETE SET NULL,
  CONSTRAINT `inventario_producto_proveedor_id_fk` FOREIGN KEY (`proveedor_id`) REFERENCES `inventario_proveedor` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla inventario_productovariante (si no existe)
CREATE TABLE IF NOT EXISTS `inventario_productovariante` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_variante` varchar(150) NOT NULL,
  `stock` int unsigned NOT NULL DEFAULT 0,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_productovariante_producto_id_nombre_variante_uniq` (`producto_id`, `nombre_variante`),
  CONSTRAINT `inventario_productovariante_producto_id_fk` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla inventario_precio (si no existe)
CREATE TABLE IF NOT EXISTS `inventario_precio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_precio` varchar(20) NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `precio_venta_normal` decimal(10,2) NOT NULL,
  `precio_venta_minimo` decimal(10,2) NOT NULL,
  `precio_venta_descuento` decimal(10,2),
  `variante_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_precio_variante_id_tipo_precio_uniq` (`variante_id`, `tipo_precio`),
  CONSTRAINT `inventario_precio_variante_id_fk` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla ventas_venta (si no existe)
-- NOTA: Esta tabla puede tener una estructura diferente según tus migraciones
-- Es mejor usar el SQL generado por sqlmigrate
```

## Después de crear las tablas

1. **Marca las migraciones iniciales como aplicadas:**
   ```sql
   INSERT INTO django_migrations (app, name, applied) VALUES
   ('inventario', '0001_initial', NOW()),
   ('ventas', '0001_initial', NOW())
   ON DUPLICATE KEY UPDATE applied = NOW();
   ```

2. **Luego ejecuta las migraciones restantes desde Railway o localmente:**
   ```bash
   python manage.py migrate
   ```

## Verificar que las tablas se crearon

```sql
-- Verificar tablas de inventario
SHOW TABLES LIKE 'inventario_%';

-- Verificar tablas de ventas
SHOW TABLES LIKE 'ventas_%';

-- Ver estructura de una tabla
DESCRIBE inventario_producto;
DESCRIBE ventas_venta;
```

