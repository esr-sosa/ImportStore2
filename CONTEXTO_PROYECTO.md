# Contexto del Proyecto ImportStore

## Descripción General

**ImportStore** es un sistema completo de gestión de negocio (ERP) desarrollado con Django (backend) y Next.js/React (frontend). El sistema incluye gestión de inventario, ventas (POS y web), clientes, configuración mayorista con descuentos por cantidad, y un panel de administración personalizado con estética futurista.

## Stack Tecnológico

### Backend
- **Django 5.2.8** - Framework principal
- **MariaDB 10.4** - Base de datos
- **Django REST Framework** - APIs REST
- **JWT Authentication** - Autenticación de usuarios
- **ReportLab** - Generación de PDFs
- **HTMX** - Actualizaciones dinámicas en templates
- **Gemini AI API** - Chat con IA para clientes

### Frontend
- **Next.js 14+** - Framework React
- **React** - Biblioteca UI
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos
- **Zustand** - Gestión de estado
- **Framer Motion** - Animaciones
- **Lottie/Three.js** - Animaciones 3D (planeado)

## Arquitectura del Sistema

### Aplicaciones Django Principales

1. **`core`** - Usuarios, autenticación JWT, perfiles, solicitudes mayoristas, chat IA
2. **`inventario`** - Productos, variantes, precios, categorías, stock
3. **`ventas`** - Ventas POS, ventas web, carritos, comprobantes PDF
4. **`configuracion`** - Configuración del sistema, escalas de precios mayoristas
5. **`crm`** - Clientes
6. **`iphones`** - Gestión especializada de iPhones
7. **`caja`** - Gestión de caja diaria
8. **`locales`** - Gestión de locales/sucursales

## Funcionalidades Principales Implementadas

### 1. Sistema de Ventas

#### POS (Punto de Venta)
- Terminal de ventas con búsqueda de productos en tiempo real
- Carrito compartido entre dispositivos (POS remoto)
- Cambio de modo de precio: Minorista / Mayorista
- Aplicación automática de descuentos por escalas (si es mayorista)
- Descuentos por método de pago
- Pago mixto (múltiples métodos)
- Generación de comprobantes PDF
- Gestión de clientes con búsqueda por nombre, DNI, email, teléfono

#### Ventas Web
- Carrito de compras persistente
- Checkout con validación de stock
- Aplicación de cupones de descuento
- Aplicación automática de descuentos por escalas (usuarios mayoristas)
- Generación de pedidos con estados de pago y entrega
- Notificaciones internas al backend cuando hay nuevas ventas

### 2. Sistema de Precios Mayoristas

#### Configuración de Escalas de Descuento
- **Panel de administración completo** para gestionar escalas de descuento
- Rangos de cantidad configurables (ej: 1-10, 11-40, 41-100, 101-300, 301+)
- Porcentaje de descuento por rango
- Orden de aplicación de escalas
- Activación/desactivación individual de escalas
- Aplicación automática en:
  - Carrito web (frontend)
  - Checkout web
  - POS (punto de venta)
  - Ventas locales

#### Configuración de Mínimos Mayoristas
- Monto mínimo de compra para usuarios mayoristas
- Cantidad mínima de unidades para usuarios mayoristas
- Validación automática al crear pedidos

### 3. Gestión de Usuarios y Perfiles

#### Registro y Autenticación
- Registro normal: siempre crea usuarios "minorista"
- Solicitud de cuenta mayorista: formulario separado
- Autenticación JWT
- Perfiles de usuario con: nombre, apellido, email, DNI, teléfono, dirección, tipo de cuenta

#### Solicitudes Mayoristas
- Panel en backend para gestionar solicitudes
- Aprobación/rechazo de solicitudes
- Actualización automática del tipo de usuario a "MAYORISTA" al aprobar
- Notificaciones por email (preparado)

### 4. Panel de Administración Personalizado

- **Estética futurista**: fondos glassmorphism, colores neón suaves, animaciones
- **Gestión completa desde el panel** (sin necesidad de Django Admin para operaciones comunes)
- **Gestión de escalas de precio**: CRUD completo con HTMX
- **Dashboard de inventario**: edición rápida de stock y precios (doble clic)
- **Lista unificada de ventas**: web, local, mayorista con filtros
- **Gestión de estados**: estado de pago y estado de entrega para cada venta

### 5. Frontend Web (Next.js)

#### Características
- **SPA completo**: sin recargas de página
- **Actualizaciones en tiempo real**: carrito, precios, descuentos
- **Visualización de descuentos**: muestra descuentos por escalas aplicados en tiempo real
- **Perfil de usuario**: edición de datos, cambio de contraseña, historial de pedidos
- **Historial de pedidos**: muestra todos los pedidos (web y POS) vinculados por DNI/email
- **Descarga de comprobantes PDF**: solo para pedidos pagados/completados
- **Chat con IA**: asistente que reconoce usuarios autenticados y tiene contexto de sus pedidos

### 6. Gestión de Inventario

#### Características
- **Edición rápida**: doble clic para editar stock y precios
- **Precios múltiples**: minorista/mayorista, ARS/USD
- **Gestión de iPhones**: módulo especializado con conversión USD a ARS
- **Categorías y productos**: gestión completa
- **Stock mínimo**: alertas visuales

### 7. Sistema de Estados de Ventas

#### Estados de Pago
- `pendiente` - Pendiente de pago
- `pagado` - Pagado
- `error` - Error en el pago
- `cancelado` - Cancelado

#### Estados de Entrega
- `pendiente` - Pendiente
- `preparando` - En preparación
- `enviado` - Enviado/En tránsito
- `entregado` - Entregado
- `retirado` - Retirado (ventas locales)

#### Historial de Estados
- Registro completo de cambios de estado
- Fecha y usuario que realizó el cambio

## Modelos de Datos Principales

### Venta
```python
- id (string único)
- fecha
- cliente (ForeignKey)
- cliente_nombre, cliente_documento
- origen: WEB, LOCAL, MAYORISTA
- estado_pago: pendiente, pagado, error, cancelado
- estado_entrega: pendiente, preparando, enviado, entregado, retirado
- metodo_pago
- subtotal_ars, descuento_total_ars, impuestos_ars, total_ars
- cupon (ForeignKey, opcional)
- descuento_cupon_ars
- observaciones
- status (compatibilidad con sistema antiguo)
```

### EscalaPrecioMayorista
```python
- configuracion (ForeignKey)
- cantidad_minima (int)
- cantidad_maxima (int, nullable)
- porcentaje_descuento (Decimal)
- activo (boolean)
- orden (int)
```

### ConfiguracionSistema
```python
- precios_escala_activos (boolean)
- monto_minimo_mayorista (Decimal)
- cantidad_minima_mayorista (int)
- ... otros campos de configuración
```

### SolicitudMayorista
```python
- nombre, apellido, email, telefono
- documento (DNI, obligatorio)
- cuit_cuil
- nombre_empresa
- mensaje
- estado: pendiente, aprobada, rechazada
- fecha_solicitud
```

## Flujos de Trabajo Principales

### 1. Venta Web
1. Usuario agrega productos al carrito
2. Sistema calcula descuentos por escalas (si es mayorista)
3. Usuario aplica cupón (opcional)
4. Checkout con validación de stock
5. Creación de venta con `origen=WEB`, `estado_pago=pendiente`, `estado_entrega=pendiente`
6. Notificación interna al backend
7. Decremento de stock

### 2. Venta POS
1. Vendedor cambia modo de precio (Minorista/Mayorista)
2. Búsqueda de productos (muestra precios según modo)
3. Agregar al carrito (aplica descuentos por escalas si es mayorista)
4. Selección de cliente (opcional)
5. Aplicación de descuentos
6. Creación de venta con `origen=LOCAL`, `estado_pago=pagado`, `estado_entrega=retirado`
7. Generación de comprobante PDF

### 3. Aplicación de Descuentos por Escalas
1. Usuario mayorista agrega productos al carrito
2. Sistema verifica si `precios_escala_activos = True`
3. Para cada producto, calcula el precio según la cantidad y las escalas configuradas
4. Aplica el descuento correspondiente
5. Muestra el descuento en tiempo real en el frontend
6. Al crear la venta, registra los descuentos en las observaciones

## Características Técnicas Importantes

### Compatibilidad
- **MariaDB 10.4**: No soporta `RETURNING` clause en algunos casos
- **Sesiones Django**: Se usa para mantener el modo de precio (minorista/mayorista) en el POS
- **HTMX**: Para actualizaciones dinámicas sin recargar página en el backend
- **Zustand con persistencia**: Para mantener el carrito en localStorage

### Validaciones Implementadas
- Stock antes de crear ventas
- Monto mínimo y cantidad mínima para mayoristas
- Validación de cupones (fechas, usos, monto mínimo)
- Validación de escalas (cantidad máxima >= cantidad mínima)

### Optimizaciones
- `select_related` y `prefetch_related` para optimizar queries
- `transaction.atomic()` para operaciones críticas
- `select_for_update()` para prevenir race conditions en stock

## Estado Actual del Proyecto

### Funcionalidades Completadas ✅
- Sistema de ventas POS completo
- Sistema de ventas web completo
- Gestión de escalas de descuento mayorista
- Aplicación automática de descuentos en todos los flujos
- Panel de administración personalizado
- Edición rápida de stock y precios
- Cambio de modo de precio en POS
- Chat con IA contextual
- Perfil de usuario con edición
- Historial de pedidos
- Generación de PDFs

### Características de Diseño
- Estética futurista con glassmorphism
- Animaciones suaves
- Responsive design
- Modo oscuro/claro

### Próximas Mejoras Sugeridas (Opcional)
- Animaciones 3D más avanzadas (Lottie/Three.js)
- Mascot animado en login (estilo Wall-E)
- Notificaciones en tiempo real más avanzadas
- Autocompletado inteligente en búsqueda

## Estructura de Archivos Clave

```
sistema_negocio/
├── core/
│   ├── models.py (PerfilUsuario, SolicitudMayorista, NotificacionInterna)
│   ├── jwt_views.py (APIs de autenticación, pedidos, chat)
│   ├── api_views.py (carrito, configuraciones, pedidos)
│   └── urls.py
├── ventas/
│   ├── models.py (Venta, DetalleVenta, Cupon, HistorialEstadoVenta)
│   ├── views.py (POS, APIs de ventas)
│   ├── pdf.py (generación de comprobantes)
│   └── templates/ventas/pos.html
├── configuracion/
│   ├── models.py (ConfiguracionSistema, EscalaPrecioMayorista)
│   ├── views.py (panel, CRUD de escalas)
│   ├── forms.py (formularios con validación de booleanos)
│   └── templates/configuracion/_panel_content.html
├── inventario/
│   ├── models.py (Producto, ProductoVariante, Precio, Categoria)
│   ├── views.py (dashboard, APIs de stock/precios)
│   └── templates/inventario/dashboard.html
└── frontend/
    ├── app/ (Next.js pages)
    ├── stores/ (Zustand: authStore, cartStore)
    └── lib/api.ts (cliente API)
```

## Notas Importantes para Desarrollo

1. **Sesiones Django**: El modo de precio se guarda en `request.session["modo_precio"]`
2. **Descuentos por escalas**: Se calculan en `ConfiguracionSistema.obtener_precio_con_escala()`
3. **Validación de booleanos**: Los checkboxes HTML no envían valor si no están marcados, se maneja en `ConfiguracionSistemaForm.clean()`
4. **HTMX**: Se usa para actualizaciones dinámicas en el panel de configuración
5. **Edición rápida**: Doble clic para editar stock/precios en inventario
6. **PDFs**: Se generan bajo demanda, no se guardan en el modelo Venta

## APIs Principales

### Frontend → Backend
- `POST /api/auth/registro/` - Registro de usuario
- `POST /api/auth/login/` - Login JWT
- `GET /api/auth/usuario/` - Usuario actual
- `GET /api/carrito/` - Obtener carrito (con descuentos calculados)
- `POST /api/carrito/` - Actualizar carrito
- `POST /api/pedido/crear/` - Crear pedido web
- `GET /api/pedidos/` - Historial de pedidos
- `GET /api/configuraciones/` - Configuración del sistema (incluye escalas)
- `POST /api/chat/cliente/` - Chat con IA

### Backend Interno
- `POST /ventas/api/cambiar-modo-precio/` - Cambiar modo precio en sesión
- `POST /ventas/api/crear/` - Crear venta desde POS
- `POST /inventario/api/actualizar-stock/` - Actualizar stock rápido
- `POST /inventario/api/actualizar-precio/` - Actualizar precio rápido
- `POST /configuracion/escalas/crear/` - Crear escala de precio
- `POST /configuracion/escalas/<id>/editar/` - Editar escala
- `POST /configuracion/escalas/<id>/eliminar/` - Eliminar escala

## Convenciones y Patrones

- **Prefijos de formularios**: `sistema-`, `preferencia-`, `tienda-`, `local-`
- **IDs de ventas**: `POS-XXXXXXXX` para ventas locales, `WEB-XXXXXXXX` para ventas web
- **Estados**: Se usan enums de Django (`TextChoices`)
- **Decimales**: Se usa `Decimal` para todos los cálculos monetarios
- **Timezone**: Se usa `timezone.now()` de Django para fechas

## Problemas Resueltos Recientemente

1. ✅ Error de validación en campos booleanos del formulario de configuración
2. ✅ Edición rápida de stock y precios (doble clic)
3. ✅ Cambio de modo de precio en POS
4. ✅ Aplicación de descuentos por escalas en todos los flujos
5. ✅ Visualización de descuentos en tiempo real en frontend
6. ✅ Gestión completa de escalas desde el panel (sin Django Admin)

## Consideraciones de Producción

- El sistema está preparado para producción
- Compatible con MariaDB 10.4
- Manejo de errores robusto
- Validaciones en frontend y backend
- Transacciones atómicas para operaciones críticas
- Logging de errores

---

**Última actualización**: Noviembre 2025
**Versión Django**: 5.2.8
**Base de datos**: MariaDB 10.4

