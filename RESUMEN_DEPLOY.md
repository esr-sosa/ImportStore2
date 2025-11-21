# 📦 Resumen Completo - Deploy Railway + Bunny.net

## ✅ Archivos Creados

### 🟦 Backend (Django)

1. **`sistema_negocio/core/storage.py`**
   - Storage backend para Bunny Storage
   - Permite usar Bunny como backend de archivos de Django

2. **`sistema_negocio/core/utils_bunny.py`**
   - Cliente para interactuar con Bunny Storage API
   - Funciones helper: `upload_pdf_to_bunny()`, `upload_image_to_bunny()`

3. **`sistema_negocio/core/settings_railway.py`**
   - Settings específicos para Railway
   - Configuración de PostgreSQL, WhiteNoise, Bunny Storage

4. **`sistema_negocio/core/healthcheck.py`**
   - Endpoint `/health/` para monitoreo
   - Verifica base de datos y Bunny Storage

5. **`sistema_negocio/ventas/pdf.py`** (modificado)
   - Generación de PDFs ahora sube automáticamente a Bunny Storage
   - Guarda URL en `venta.comprobante_url`

6. **`sistema_negocio/ventas/models.py`** (modificado)
   - Agregado campo `comprobante_url` al modelo `Venta`

7. **`sistema_negocio/core/urls.py`** (modificado)
   - Agregado endpoint `/health/`

### 🐳 Docker

8. **`Dockerfile.railway`**
   - Dockerfile optimizado para Railway
   - Multi-stage build, healthcheck incluido

9. **`railway.json`**
   - Configuración de Railway
   - Build y deploy commands

### 📝 Scripts y Tests

10. **`scripts/test_bunny.py`**
    - Tests de conexión a Bunny Storage
    - Tests de subida de archivos, PDFs e imágenes

11. **`scripts/test_railway.py`**
    - Tests de configuración de Railway
    - Tests de base de datos, settings, healthcheck

### 📚 Documentación

12. **`RAILWAY_DEPLOY.md`**
    - Guía completa de deploy paso a paso
    - Configuración de Bunny Storage
    - Troubleshooting

13. **`.env.railway.example`**
    - Template de variables de entorno para Railway

### 📦 Dependencias

14. **`requirements.txt`** (modificado)
    - Agregado `dj-database-url==2.1.0` para parsear DATABASE_URL

---

## 🚀 Comandos para Deploy

### 1. Preparación Local

```bash
# Clonar repositorio
git clone <tu-repositorio>
cd ImportStore

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.railway.example .env
# Editar .env con tus valores

# Ejecutar migraciones (incluye el nuevo campo comprobante_url)
cd sistema_negocio
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Tests locales
python scripts/test_bunny.py
python scripts/test_railway.py
```

### 2. Deploy en Railway

#### Opción A: Desde GitHub (Recomendado)

1. **Push a GitHub**:
   ```bash
   git add .
   git commit -m "Preparar deploy Railway + Bunny"
   git push origin main
   ```

2. **En Railway Dashboard**:
   - New Project → Deploy from GitHub repo
   - Seleccionar repositorio
   - Railway detectará automáticamente `Dockerfile.railway`

3. **Crear PostgreSQL**:
   - + New → Database → Add PostgreSQL
   - Railway inyectará automáticamente `DATABASE_URL`

4. **Configurar Variables de Entorno**:
   - Ver sección de variables más abajo

#### Opción B: Con Railway CLI

```bash
# Instalar CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar
railway init

# Agregar PostgreSQL
railway add postgresql

# Configurar variables (ver más abajo)
railway variables set DJANGO_SECRET_KEY=tu-secret-key
# ... etc

# Deploy
railway up
```

### 3. Migraciones en Railway

Las migraciones se ejecutan automáticamente en el `startCommand` del Dockerfile.

Para ejecutar manualmente:

```bash
railway run python sistema_negocio/manage.py migrate
railway run python sistema_negocio/manage.py createsuperuser
```

---

## 🔑 Variables de Entorno Necesarias

### En Railway Dashboard → Variables

```env
# ============================================
# DJANGO
# ============================================
DJANGO_SECRET_KEY=generar-con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app

# ============================================
# BASE DE DATOS (Railway inyecta automáticamente)
# ============================================
# DATABASE_URL se inyecta automáticamente cuando agregás PostgreSQL
# Si necesitás variables separadas:
# DB_ENGINE=postgresql
# DB_NAME=railway
# DB_USER=postgres
# DB_PASSWORD=...
# DB_HOST=containers-us-west-xxx.railway.app
# DB_PORT=5432

# ============================================
# BUNNY STORAGE
# ============================================
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password-de-bunny
BUNNY_STORAGE_ZONE=importstore-storage
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://importstore-storage.b-cdn.net

# ============================================
# CORS
# ============================================
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio.com

# ============================================
# SERVICIOS EXTERNOS
# ============================================
GEMINI_API_KEY=tu-api-key-de-google-gemini
```

### Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🧪 Tests

### Test de Bunny Storage

```bash
# Local
python scripts/test_bunny.py

# En Railway
railway run python scripts/test_bunny.py
```

### Test de Railway

```bash
# Local (con .env configurado)
python scripts/test_railway.py

# En Railway
railway run python scripts/test_railway.py
```

### Test de Healthcheck

```bash
curl https://tu-proyecto.railway.app/health/
```

Debería retornar:
```json
{
  "status": "healthy",
  "checks": {
    "database": "healthy",
    "bunny_storage": "healthy"
  }
}
```

---

## 📋 Checklist Final

### Pre-Deploy

- [ ] Cuenta de Railway creada
- [ ] Cuenta de Bunny.net creada
- [ ] Storage Zone creada en Bunny
- [ ] Variables de entorno configuradas
- [ ] `DJANGO_SECRET_KEY` generado
- [ ] `DEBUG=False`
- [ ] Migraciones creadas (`makemigrations`)
- [ ] Tests pasando localmente

### Post-Deploy

- [ ] Servicio corriendo en Railway
- [ ] Base de datos conectada
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Healthcheck funcionando (`/health/`)
- [ ] Test de Bunny Storage pasando
- [ ] PDFs subiendo a Bunny Storage
- [ ] Admin accesible (`/admin/`)

---

## 🔍 Troubleshooting Rápido

### Error: Database connection failed
```bash
railway logs
# Verificar DATABASE_URL en Railway variables
```

### Error: Bunny Storage not configured
```bash
railway run python scripts/test_bunny.py
# Verificar variables: USE_BUNNY_STORAGE, BUNNY_STORAGE_KEY, etc.
```

### Error: Healthcheck failed
```bash
curl https://tu-proyecto.railway.app/health/
railway logs
```

### Error: PDFs no se suben
```bash
# Verificar logs
railway logs | grep bunny
# Ejecutar test
railway run python scripts/test_bunny.py
```

---

## 📚 Documentación Adicional

- **Guía completa**: Ver `RAILWAY_DEPLOY.md`
- **Variables de entorno**: Ver `.env.railway.example`
- **Tests**: Ver `scripts/test_bunny.py` y `scripts/test_railway.py`

---

## 🎉 ¡Listo para Deploy!

Tu proyecto está completamente preparado para desplegar en Railway con Bunny Storage.

**Próximos pasos**:
1. Configurar Bunny Storage (ver `RAILWAY_DEPLOY.md`)
2. Hacer deploy en Railway
3. Configurar variables de entorno
4. Ejecutar migraciones
5. ¡Disfrutar! 🚀

---

**¿Dudas?** Revisá `RAILWAY_DEPLOY.md` para la guía completa paso a paso.

