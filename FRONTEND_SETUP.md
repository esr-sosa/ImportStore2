# 🚀 Frontend E-commerce - Guía de Instalación y Uso

## ✅ Lo que se ha creado

### Backend (Django)
- ✅ **APIs REST completas** en `/sistema_negocio/core/api_views.py`:
  - `/api/configuraciones/` - Configuración de la tienda
  - `/api/categorias/` - Lista de categorías
  - `/api/productos/` - Catálogo con filtros
  - `/api/productos/destacados/` - Productos destacados
  - `/api/productos/{id}/` - Detalle de producto
  - `/api/login/` - Autenticación
  - `/api/usuario/` - Usuario actual
  - `/api/carrito/` - Gestión del carrito
  - `/api/pedido/` - Crear pedidos

- ✅ **CORS configurado** para permitir requests del frontend
- ✅ **Botón "Ir a la Web"** agregado en el dashboard del sistema

### Frontend (Next.js)
- ✅ **Proyecto completo** en `/frontend/` con:
  - Next.js 14 + React 18
  - TailwindCSS para estilos
  - Framer Motion para animaciones
  - Zustand para estado global
  - Axios para llamadas API

- ✅ **Páginas implementadas**:
  - Landing page con productos destacados
  - Catálogo de productos con filtros
  - Detalle de producto con galería
  - Carrito de compras
  - Checkout
  - Login/Autenticación
  - Panel de usuario
  - Página de categorías

- ✅ **Componentes reutilizables**:
  - Navbar (con búsqueda y carrito)
  - Footer (con información de contacto)
  - ProductCard
  - PriceTag

## 📦 Instalación

### 1. Instalar dependencias del backend

```bash
cd sistema_negocio
source venv/bin/activate  # En Mac/Linux
# o venv\Scripts\activate en Windows

pip install django-cors-headers==4.3.1
```

### 2. Instalar dependencias del frontend

```bash
cd frontend
npm install
```

### 3. Configurar variables de entorno

**Backend** (`.env` en `sistema_negocio/`):
```env
# Opcional: URL del frontend (para el botón en el dashboard)
FRONTEND_URL=http://localhost:3000
```

**Frontend** (`.env.local` en `frontend/`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏃 Ejecución

### 1. Iniciar el backend

```bash
cd sistema_negocio
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

El backend estará en: `http://localhost:8000`

### 2. Iniciar el frontend

```bash
cd frontend
npm run dev
```

El frontend estará en: `http://localhost:3000`

## 🎨 Características del Frontend

### Diseño
- ✨ Estilo minimalista tipo Apple
- 📱 Totalmente responsive (mobile, tablet, desktop)
- 🎨 Adaptación automática de colores y logo desde el backend
- 🎭 Animaciones suaves con Framer Motion

### Funcionalidades
- 🛒 Carrito de compras completo
- 🔐 Autenticación de usuarios (sesiones Django)
- 💳 Checkout y creación de pedidos
- 🔍 Búsqueda y filtros avanzados
- 📱 Modo mayorista/minorista según permisos
- 🏷️ Códigos QR en productos
- 📸 Galería de imágenes

### Personalización Automática
El frontend se adapta automáticamente a:
- **Color principal**: Desde `ConfiguracionSistema.color_principal`
- **Logo**: Desde `ConfiguracionSistema.logo`
- **Nombre**: Desde `ConfiguracionSistema.nombre_comercial`
- **Contacto**: WhatsApp, email, teléfono, dirección
- **Horarios**: Mostrados en el footer
- **Redes sociales**: Instagram, Facebook

## 🔧 Configuración Adicional

### Cambiar la URL del frontend en el dashboard

Edita `sistema_negocio/dashboard/views.py` línea ~550:

```python
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
```

O agrega en tu `.env`:
```env
FRONTEND_URL=https://tu-dominio.com
```

### Permitir más orígenes CORS

Edita `sistema_negocio/core/settings.py` y agrega más URLs en `CORS_ALLOWED_ORIGINS`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://tu-dominio.com",  # Agregar tu dominio
]
```

## 📝 Notas Importantes

1. **Autenticación**: El frontend usa sesiones de Django (cookies). Asegúrate de que CORS esté configurado correctamente.

2. **Imágenes**: Las imágenes se sirven desde `/media/` del backend. Asegúrate de que `MEDIA_URL` y `MEDIA_ROOT` estén configurados.

3. **Stock**: Los productos sin stock no se muestran en el catálogo público.

4. **Precios**: El frontend muestra precios según el tipo seleccionado (minorista/mayorista).

## 🐛 Solución de Problemas

### Error de CORS
- Verifica que `django-cors-headers` esté instalado
- Verifica que `CORS_ALLOWED_ORIGINS` incluya la URL del frontend
- Verifica que `CORS_ALLOW_CREDENTIALS = True`

### Imágenes no se muestran
- Verifica que `MEDIA_URL` y `MEDIA_ROOT` estén configurados
- Verifica que las imágenes existan en el directorio `media/`
- Verifica que `next.config.js` tenga los dominios correctos en `images.domains`

### Error al agregar al carrito
- Verifica que el usuario esté autenticado
- Verifica que el producto tenga stock
- Verifica que el producto tenga precio configurado

## 🚀 Próximos Pasos

1. **Personalizar diseño**: Edita los componentes en `frontend/components/`
2. **Agregar más funcionalidades**: Historial de pedidos, wishlist, etc.
3. **Optimizar imágenes**: Configurar un CDN o servicio de imágenes
4. **SEO**: Agregar meta tags y sitemap
5. **Analytics**: Integrar Google Analytics o similar

## 📚 Documentación

- **Next.js**: https://nextjs.org/docs
- **TailwindCSS**: https://tailwindcss.com/docs
- **Framer Motion**: https://www.framer.com/motion/
- **Zustand**: https://github.com/pmndrs/zustand

