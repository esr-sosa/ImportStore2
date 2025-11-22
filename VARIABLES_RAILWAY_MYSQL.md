# 🔑 Variables de Entorno para Railway con MySQL

## ✅ Variables que Railway Inyecta Automáticamente

Cuando creas un servicio MySQL en Railway, estas variables se inyectan automáticamente:

- ✅ `MYSQL_URL` - URL privada de MySQL
- ✅ `MYSQL_PUBLIC_URL` - URL pública de MySQL (si está habilitada)
- ✅ `MYSQLDATABASE` - Nombre de la base de datos
- ✅ `MYSQLUSER` - Usuario de MySQL
- ✅ `MYSQLPASSWORD` - Contraseña de MySQL
- ✅ `MYSQLHOST` - Host de MySQL
- ✅ `MYSQLPORT` - Puerto de MySQL (3306)
- ✅ `MYSQL_ROOT_PASSWORD` - Contraseña root

**NO necesitas configurar estas manualmente**, Railway las inyecta automáticamente.

---

## 📋 Variables que SÍ debes Configurar

En Railway Dashboard → **Variables**, agregar estas:

### 1. Django Settings (OBLIGATORIAS)

```env
DJANGO_SECRET_KEY=GENERAR-NUEVA-KEY-AQUI
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
```

**Generar SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Settings Module (OPCIONAL pero recomendado)

```env
DJANGO_SETTINGS_MODULE=core.settings_railway
```

### 3. Bunny Storage (OBLIGATORIAS si usas Bunny)

```env
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password-de-bunny-storage
BUNNY_STORAGE_ZONE=nombre-de-tu-zona
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://tu-zona.b-cdn.net
```

### 4. CORS (OBLIGATORIAS para frontend)

```env
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio.com
```

### 5. Servicios Externos

```env
GEMINI_API_KEY=tu-api-key-de-google-gemini
```

---

## 📝 Lista Completa de Variables

```env
# ============================================
# DJANGO (OBLIGATORIAS)
# ============================================
DJANGO_SECRET_KEY=django-insecure-genera-una-key-nueva-y-segura
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
DJANGO_SETTINGS_MODULE=core.settings_railway

# ============================================
# BUNNY STORAGE (OBLIGATORIAS)
# ============================================
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password
BUNNY_STORAGE_ZONE=tu-zona
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://tu-zona.b-cdn.net

# ============================================
# CORS
# ============================================
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app

# ============================================
# SERVICIOS EXTERNOS
# ============================================
GEMINI_API_KEY=tu-api-key
```

---

## ✅ Variables Automáticas de Railway (NO configurar manualmente)

Estas se inyectan automáticamente cuando agregas MySQL:

- ✅ `MYSQL_URL` - Se usa automáticamente
- ✅ `MYSQL_PUBLIC_URL` - Se usa automáticamente si está disponible
- ✅ `MYSQLDATABASE` - Se usa automáticamente
- ✅ `MYSQLUSER` - Se usa automáticamente
- ✅ `MYSQLPASSWORD` - Se usa automáticamente
- ✅ `MYSQLHOST` - Se usa automáticamente
- ✅ `MYSQLPORT` - Se usa automáticamente
- ✅ `MYSQL_ROOT_PASSWORD` - Se usa automáticamente

**NO las agregues manualmente**, Railway las inyecta.

---

## 🔍 Verificar Configuración

```bash
railway variables
```

Debe mostrar:
- ✅ Variables de MySQL (automáticas, inyectadas por Railway)
- ✅ Variables de Django (configuradas manualmente)
- ✅ Variables de Bunny Storage (configuradas manualmente)

---

## 🚀 Después de Configurar

1. **Hacer commit y push**:
   ```bash
   git add .
   git commit -m "Configurar para MySQL en Railway"
   git push origin main
   ```

2. **Verificar logs**:
   ```bash
   railway logs
   ```
   
   Deberías ver:
   ```
   ✅ Usando settings_railway (MySQL detectado)
   📦 Recopilando archivos estáticos...
   🔄 Ejecutando migraciones...
   🚀 Iniciando servidor...
   ```

3. **Verificar healthcheck**:
   ```bash
   curl https://tu-proyecto.railway.app/health/
   ```
   
   Debe retornar:
   ```json
   {
     "status": "healthy",
     "checks": {
       "database": "healthy (mysql)",
       "bunny_storage": "healthy"
     }
   }
   ```

---

## ✅ Checklist

- [ ] Servicio MySQL agregado en Railway
- [ ] Variables de Django configuradas
- [ ] Variables de Bunny Storage configuradas
- [ ] `DJANGO_SECRET_KEY` generado y configurado
- [ ] `CORS_ALLOWED_ORIGINS` configurado con URL del frontend
- [ ] Código pusheado a GitHub
- [ ] Railway redeployado automáticamente
- [ ] Logs sin errores
- [ ] Healthcheck funcionando

---

**¡Listo!** El proyecto ahora está configurado para usar MySQL en Railway.

