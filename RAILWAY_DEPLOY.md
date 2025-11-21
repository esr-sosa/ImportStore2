# 🚂 Guía de Deploy en Railway + Bunny.net

## 📋 Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración de Bunny Storage](#configuración-de-bunny-storage)
3. [Deploy en Railway](#deploy-en-railway)
4. [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
5. [Migraciones](#migraciones)
6. [Tests](#tests)
7. [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos Previos

- Cuenta en [Railway](https://railway.app/)
- Cuenta en [Bunny.net](https://bunny.net/)
- Git instalado
- Repositorio del proyecto en GitHub/GitLab

---

## 🟧 Configuración de Bunny Storage

### 1. Crear Storage Zone en Bunny.net

1. Iniciar sesión en [Bunny.net](https://bunny.net/)
2. Ir a **Storage** → **Add Storage Zone**
3. Configurar:
   - **Name**: `importstore-storage` (o el nombre que prefieras)
   - **Region**: Elegir la más cercana (ej: `New York`, `Los Angeles`, `Singapore`)
   - **Replication**: Opcional
4. Guardar y copiar:
   - **Storage Zone Name**
   - **FTP Password** (esta es tu `BUNNY_STORAGE_KEY`)
   - **CDN URL** (ej: `https://importstore-storage.b-cdn.net`)

### 2. Configurar Pull Zone (Opcional pero recomendado)

1. Ir a **CDN** → **Add Pull Zone**
2. Configurar:
   - **Name**: `importstore-cdn`
   - **Origin URL**: Dejar vacío (usar Storage Zone)
   - **Storage Zone**: Seleccionar la zona creada
3. Guardar y copiar la **CDN URL**

---

## 🚂 Deploy en Railway

### Opción 1: Deploy desde GitHub (Recomendado)

1. **Conectar repositorio**:
   - Ir a [Railway Dashboard](https://railway.app/dashboard)
   - Click en **New Project** → **Deploy from GitHub repo**
   - Seleccionar tu repositorio

2. **Crear servicio de base de datos**:
   - En el proyecto, click en **+ New** → **Database** → **Add PostgreSQL**
   - Railway creará automáticamente la base de datos
   - Copiar la **DATABASE_URL** (se inyecta automáticamente)

3. **Configurar servicio de backend**:
   - Railway detectará automáticamente el `Dockerfile.railway`
   - Si no, configurar manualmente:
     - **Build Command**: (dejar vacío, usa Dockerfile)
     - **Start Command**: (se usa el CMD del Dockerfile)

4. **Configurar variables de entorno**:
   - Ver sección [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)

### Opción 2: Deploy con Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Agregar servicio PostgreSQL
railway add postgresql

# Deploy
railway up
```

---

## ⚙️ Configuración de Variables de Entorno

Configurar estas variables en Railway Dashboard → **Variables**:

### Variables Obligatorias

```env
# Django
DJANGO_SECRET_KEY=tu-secret-key-super-segura
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app

# Base de datos (Railway inyecta automáticamente DATABASE_URL)
# Si no, usar estas:
DB_ENGINE=postgresql
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=5432

# Bunny Storage
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password-de-bunny
BUNNY_STORAGE_ZONE=importstore-storage
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://importstore-storage.b-cdn.net

# CORS (URLs de tu frontend)
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio.com

# Servicios externos
GEMINI_API_KEY=tu-api-key-de-google-gemini
```

### Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🔄 Migraciones

### Migraciones Automáticas en Railway

Railway ejecutará automáticamente las migraciones en el `startCommand` del Dockerfile.

### Migraciones Manuales

```bash
# Conectarse al servicio
railway shell

# Ejecutar migraciones
cd sistema_negocio
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### Script de Migración

```bash
# En Railway, agregar variable de entorno:
RAILWAY_RUN_MIGRATIONS=true

# O ejecutar manualmente después del deploy
railway run python sistema_negocio/manage.py migrate
```

---

## 🧪 Tests

### Test de Conexión a Bunny

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
# Verificar endpoint
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

## 📝 Comandos Útiles

### Local (Desarrollo)

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.railway.example .env
# Editar .env con tus valores

# Ejecutar migraciones
cd sistema_negocio
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Tests
python scripts/test_bunny.py
python scripts/test_railway.py
```

### Railway (Producción)

```bash
# Ver logs
railway logs

# Conectarse al servicio
railway shell

# Ejecutar comandos Django
railway run python sistema_negocio/manage.py migrate
railway run python sistema_negocio/manage.py createsuperuser
railway run python sistema_negocio/manage.py collectstatic

# Ver variables de entorno
railway variables

# Abrir dashboard
railway open
```

---

## 🔍 Troubleshooting

### Error: "Database connection failed"

1. Verificar que `DATABASE_URL` esté configurado en Railway
2. Verificar que el servicio PostgreSQL esté corriendo
3. Revisar logs: `railway logs`

### Error: "Bunny Storage not configured"

1. Verificar que `USE_BUNNY_STORAGE=true`
2. Verificar que todas las variables de Bunny estén configuradas:
   - `BUNNY_STORAGE_KEY`
   - `BUNNY_STORAGE_ZONE`
   - `BUNNY_STORAGE_URL`
3. Ejecutar test: `python scripts/test_bunny.py`

### Error: "Healthcheck failed"

1. Verificar logs: `railway logs`
2. Verificar que el servicio esté corriendo: `railway status`
3. Verificar variables de entorno: `railway variables`

### Error: "Static files not found"

1. Ejecutar collectstatic:
   ```bash
   railway run python sistema_negocio/manage.py collectstatic --noinput
   ```
2. Verificar que WhiteNoise esté configurado en `settings_railway.py`

### Error: "PDF not uploading to Bunny"

1. Verificar configuración de Bunny Storage
2. Verificar permisos de la Storage Zone
3. Revisar logs del backend para ver errores específicos
4. Ejecutar test: `python scripts/test_bunny.py`

---

## 📊 Monitoreo

### Healthcheck Endpoint

Railway usa automáticamente el endpoint `/health/` para monitoreo.

### Logs

```bash
# Ver logs en tiempo real
railway logs --follow

# Ver logs de un servicio específico
railway logs --service backend
```

### Métricas

Railway Dashboard muestra:
- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 🔄 Actualizaciones

### Actualizar Código

```bash
# Hacer push a GitHub
git push origin main

# Railway detectará automáticamente y desplegará
```

### Actualizar Variables de Entorno

1. Ir a Railway Dashboard → **Variables**
2. Editar variables necesarias
3. Railway reiniciará automáticamente el servicio

---

## ✅ Checklist Pre-Deploy

- [ ] Cuenta de Railway creada
- [ ] Cuenta de Bunny.net creada
- [ ] Storage Zone creada en Bunny
- [ ] Variables de entorno configuradas en Railway
- [ ] `DJANGO_SECRET_KEY` generado y configurado
- [ ] `DEBUG=False` en producción
- [ ] Base de datos PostgreSQL creada en Railway
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Tests pasando
- [ ] Healthcheck funcionando

---

## 🎉 ¡Listo!

Tu aplicación debería estar corriendo en Railway con archivos estáticos en Bunny Storage.

**URLs**:
- Backend: `https://tu-proyecto.railway.app`
- Healthcheck: `https://tu-proyecto.railway.app/health/`
- Admin: `https://tu-proyecto.railway.app/admin/`

---

**¿Problemas?** Revisá los logs con `railway logs` o ejecutá los tests de diagnóstico.

