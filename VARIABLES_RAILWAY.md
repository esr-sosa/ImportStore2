# 🔑 Variables de Entorno para Railway

## ⚠️ IMPORTANTE: Usar PostgreSQL, NO MySQL

Railway ofrece PostgreSQL de forma nativa y es lo que está configurado en el proyecto. **NO uses MySQL**.

## 📋 Variables Necesarias en Railway

### 1. Base de Datos (Automático)

**NO necesitas configurar estas variables manualmente.** Railway las inyecta automáticamente cuando agregas PostgreSQL:

- ✅ `DATABASE_URL` - Se inyecta automáticamente (formato: `postgresql://postgres:password@host:port/dbname`)
- ✅ `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` - También se inyectan automáticamente

**Acción**: Solo necesitas agregar el servicio PostgreSQL en Railway Dashboard → + New → Database → Add PostgreSQL

---

### 2. Django Settings (OBLIGATORIAS)

```env
DJANGO_SECRET_KEY=django-insecure-genera-una-key-nueva-y-segura-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
```

**Generar SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 3. Settings Module (OPCIONAL pero recomendado)

```env
DJANGO_SETTINGS_MODULE=core.settings_railway
```

**Nota**: El script `start_railway.sh` detecta automáticamente `DATABASE_URL` y usa `settings_railway`, pero puedes forzarlo con esta variable.

---

### 4. Bunny Storage (OBLIGATORIAS si usas Bunny)

```env
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password-de-bunny-storage
BUNNY_STORAGE_ZONE=nombre-de-tu-zona
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://tu-zona.b-cdn.net
```

**Cómo obtenerlas**:
1. Ir a [Bunny.net](https://bunny.net/) → Storage
2. Crear Storage Zone
3. Copiar: FTP Password (es `BUNNY_STORAGE_KEY`), Zone Name, CDN URL

---

### 5. CORS (OBLIGATORIAS para frontend)

```env
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio.com
```

Reemplazar con las URLs reales de tu frontend.

---

### 6. Servicios Externos

```env
GEMINI_API_KEY=tu-api-key-de-google-gemini
```

---

## 🚫 Variables que NO debes poner

**NO pongas estas variables** (son para MySQL, no las necesitas):

- ❌ `MYSQL_DATABASE`
- ❌ `MYSQL_PUBLIC_URL`
- ❌ `MYSQL_ROOT_PASSWORD`
- ❌ `MYSQL_URL`
- ❌ `MYSQLDATABASE`
- ❌ `MYSQLHOST`
- ❌ `MYSQLPASSWORD`
- ❌ `MYSQLPORT`
- ❌ `MYSQLUSER`

---

## ✅ Checklist de Variables en Railway

### Paso 1: Agregar PostgreSQL

1. En Railway Dashboard → Tu Proyecto
2. Click en **+ New** → **Database** → **Add PostgreSQL**
3. Railway creará automáticamente la base de datos
4. Railway inyectará automáticamente `DATABASE_URL`

### Paso 2: Configurar Variables

Ir a **Variables** en Railway y agregar:

- [ ] `DJANGO_SECRET_KEY` (generar nueva)
- [ ] `DJANGO_DEBUG=False`
- [ ] `DJANGO_ALLOWED_HOSTS=*.railway.app`
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app`
- [ ] `DJANGO_SETTINGS_MODULE=core.settings_railway` (opcional)
- [ ] `USE_BUNNY_STORAGE=true`
- [ ] `BUNNY_STORAGE_KEY=...`
- [ ] `BUNNY_STORAGE_ZONE=...`
- [ ] `BUNNY_STORAGE_REGION=ny`
- [ ] `BUNNY_STORAGE_URL=https://...`
- [ ] `CORS_ALLOWED_ORIGINS=https://...`
- [ ] `GEMINI_API_KEY=...`

### Paso 3: Verificar

```bash
railway variables
```

Debe mostrar:
- ✅ `DATABASE_URL` (automático de PostgreSQL)
- ✅ Todas las variables de Django
- ✅ Todas las variables de Bunny Storage

---

## 📝 Ejemplo Completo de Variables

```env
# Django
DJANGO_SECRET_KEY=django-insecure-abc123xyz789...
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
DJANGO_SETTINGS_MODULE=core.settings_railway

# Bunny Storage
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password-aqui
BUNNY_STORAGE_ZONE=importstore-storage
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://importstore-storage.b-cdn.net

# CORS
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app

# Servicios
GEMINI_API_KEY=tu-api-key-aqui
```

---

## 🔍 Verificar que Funciona

Después de configurar las variables:

```bash
# Ver logs
railway logs

# Deberías ver:
# ✅ Usando settings_railway (DATABASE_URL detectado)
# 📦 Recopilando archivos estáticos...
# 🔄 Ejecutando migraciones...
# 🚀 Iniciando servidor...
```

---

## ⚠️ Si ves errores de MySQL

Si aún ves errores de MySQL, significa que:

1. **No agregaste PostgreSQL**: Agrega el servicio PostgreSQL en Railway
2. **Variables de MySQL presentes**: Elimina todas las variables que empiezan con `MYSQL`
3. **DATABASE_URL no está presente**: Verifica que PostgreSQL esté agregado y corriendo

---

**Resumen**: Usa PostgreSQL (se agrega automáticamente), configura las variables de Django y Bunny Storage, y elimina cualquier variable de MySQL.

