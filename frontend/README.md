# ImportStore Frontend - E-commerce Premium

Frontend completo tipo Apple para el sistema de gestión ImportStore.

## 🚀 Características

- ✨ Diseño minimalista estilo Apple
- 📱 Totalmente responsive (mobile, tablet, desktop)
- 🎨 Adaptación automática de colores y logo desde el backend
- 🛒 Carrito de compras completo
- 🔐 Autenticación de usuarios
- 💳 Checkout y creación de pedidos
- 🎭 Animaciones suaves con Framer Motion
- 🔍 Búsqueda y filtros avanzados

## 📦 Instalación

```bash
# Instalar dependencias
npm install

# Crear archivo de configuración
cp .env.local.example .env.local

# Editar .env.local con la URL de tu backend
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏃 Ejecución

```bash
# Modo desarrollo
npm run dev

# El frontend estará disponible en http://localhost:3000
```

## 🏗️ Build para Producción

```bash
# Generar build
npm run build

# Ejecutar en producción
npm start
```

## 📁 Estructura del Proyecto

```
frontend/
├── app/                    # Páginas (Next.js App Router)
│   ├── page.tsx           # Landing page
│   ├── productos/         # Catálogo y detalle
│   ├── carrito/           # Carrito de compras
│   ├── checkout/          # Checkout
│   ├── login/             # Autenticación
│   └── usuario/           # Panel de usuario
├── components/             # Componentes reutilizables
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── ProductCard.tsx
│   └── PriceTag.tsx
├── lib/                    # Utilidades y API client
│   └── api.ts
├── stores/                 # Zustand stores
│   ├── cartStore.ts
│   ├── authStore.ts
│   └── configStore.ts
└── public/                 # Archivos estáticos
```

## 🔌 APIs Consumidas

El frontend consume las siguientes APIs del backend Django:

- `GET /api/configuraciones/` - Configuración de la tienda
- `GET /api/categorias/` - Lista de categorías
- `GET /api/productos/` - Lista de productos (con filtros)
- `GET /api/productos/destacados/` - Productos destacados
- `GET /api/productos/{id}/` - Detalle de producto
- `POST /api/login/` - Iniciar sesión
- `GET /api/usuario/` - Usuario actual
- `GET /api/carrito/` - Obtener carrito
- `POST /api/carrito/` - Agregar al carrito
- `DELETE /api/carrito/item/{index}/` - Eliminar del carrito
- `POST /api/carrito/limpiar/` - Limpiar carrito
- `POST /api/pedido/` - Crear pedido

## 🎨 Personalización

El frontend se adapta automáticamente a la configuración del backend:

- **Color principal**: Se toma de `ConfiguracionSistema.color_principal`
- **Logo**: Se muestra si está configurado en `ConfiguracionSistema.logo`
- **Nombre**: Se usa `ConfiguracionSistema.nombre_comercial`
- **Información de contacto**: WhatsApp, email, teléfono, dirección
- **Horarios**: Se muestran en el footer
- **Redes sociales**: Instagram, Facebook

## 🔧 Configuración

Edita `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Notas

- El frontend usa sesiones de Django para autenticación (cookies)
- Asegúrate de que CORS esté configurado en el backend
- Las imágenes se sirven desde `/media/` del backend

