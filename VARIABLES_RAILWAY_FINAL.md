# 🔑 Variables Finales para Railway con MySQL

## ✅ Variables Automáticas de Railway (NO configurar)

Railway inyecta estas automáticamente cuando agregas MySQL:

- ✅ `MYSQL_URL` - URL privada de MySQL
- ✅ `MYSQL_PUBLIC_URL` - URL pública de MySQL
- ✅ `MYSQLDATABASE` - Nombre de la base de datos
- ✅ `MYSQLUSER` - Usuario
- ✅ `MYSQLPASSWORD` - Contraseña
- ✅ `MYSQLHOST` - Host
- ✅ `MYSQLPORT` - Puerto (3306)
- ✅ `MYSQL_ROOT_PASSWORD` - Contraseña root

**NO las agregues manualmente**, Railway las inyecta automáticamente.

---

## 📋 Variables que SÍ debes Configurar

En Railway Dashboard → **Variables**, agregar estas:

```env
# ============================================
# DJANGO (OBLIGATORIAS)
# ============================================
DJANGO_SECRET_KEY=GENERAR-NUEVA-KEY-AQUI
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
DJANGO_SETTINGS_MODULE=core.settings_railway

# ============================================
# BUNNY STORAGE (OBLIGATORIAS)
# ============================================
USE_BUNNY_STORAGE=true
BUNNY_STORAGE_KEY=tu-ftp-password-de-bunny
BUNNY_STORAGE_ZONE=nombre-de-tu-zona
BUNNY_STORAGE_REGION=ny
BUNNY_STORAGE_URL=https://tu-zona.b-cdn.net

# ============================================
# CORS (OBLIGATORIAS para frontend)
# ============================================
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app

# ============================================
# SERVICIOS EXTERNOS
# ============================================
GEMINI_API_KEY=tu-api-key-de-google-gemini
```

---

## 🔑 Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar el resultado y usarlo en `DJANGO_SECRET_KEY`.

---

## ✅ Resumen

### Variables Automáticas (Railway las inyecta):
- ✅ `MYSQL_URL` o `MYSQL_PUBLIC_URL`
- ✅ `MYSQLDATABASE`, `MYSQLUSER`, `MYSQLPASSWORD`, etc.

### Variables Manuales (Tú las configuras):
- ✅ `DJANGO_SECRET_KEY` (generar nueva)
- ✅ `DJANGO_DEBUG=False`
- ✅ `DJANGO_ALLOWED_HOSTS=*.railway.app`
- ✅ `DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app`
- ✅ `USE_BUNNY_STORAGE=true`
- ✅ `BUNNY_STORAGE_KEY`, `BUNNY_STORAGE_ZONE`, `BUNNY_STORAGE_URL`
- ✅ `CORS_ALLOWED_ORIGINS`
- ✅ `GEMINI_API_KEY`

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

---

**¡Listo!** El proyecto está configurado para MySQL en Railway.

