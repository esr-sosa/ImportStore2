# 🚂 Instrucciones Rápidas - Deploy en Railway

## ⚠️ Error Resuelto: MySQL Connection Refused

El error que estabas viendo (`Can't connect to MySQL server on 'localhost'`) ha sido resuelto. Los cambios aplicados:

1. ✅ `settings.py` ahora detecta automáticamente `DATABASE_URL`
2. ✅ `Dockerfile.railway` configurado para usar `settings_railway`
3. ✅ Script `start_railway.sh` que detecta el entorno automáticamente

## 🚀 Pasos para Deploy

### 1. Hacer Commit y Push

```bash
git add .
git commit -m "Fix: Detectar DATABASE_URL automáticamente para Railway"
git push origin main
```

### 2. En Railway Dashboard

1. **Verificar que PostgreSQL esté agregado**:
   - Debe haber un servicio PostgreSQL en tu proyecto
   - Railway inyecta automáticamente `DATABASE_URL`

2. **Verificar Variables de Entorno**:
   - Ir a **Variables** en Railway Dashboard
   - Verificar que `DATABASE_URL` esté presente (se inyecta automáticamente)
   - Agregar si falta:
     ```
     DJANGO_SETTINGS_MODULE=core.settings_railway
     ```

3. **Variables Requeridas**:
   ```env
   DJANGO_SECRET_KEY=tu-secret-key-generado
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=*.railway.app
   DJANGO_CSRF_TRUSTED_ORIGINS=https://*.railway.app
   
   USE_BUNNY_STORAGE=true
   BUNNY_STORAGE_KEY=tu-ftp-password
   BUNNY_STORAGE_ZONE=tu-zona
   BUNNY_STORAGE_REGION=ny
   BUNNY_STORAGE_URL=https://tu-zona.b-cdn.net
   
   CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
   GEMINI_API_KEY=tu-api-key
   ```

### 3. Verificar Deploy

Después del push, Railway redeployará automáticamente. Verificar logs:

```bash
railway logs
```

Deberías ver:
```
✅ Usando settings_railway (DATABASE_URL detectado)
📦 Recopilando archivos estáticos...
🔄 Ejecutando migraciones...
🚀 Iniciando servidor...
```

## 🔍 Si el Error Persiste

### Opción 1: Forzar settings_railway

En Railway Dashboard → Variables, agregar:
```
DJANGO_SETTINGS_MODULE=core.settings_railway
```

### Opción 2: Verificar DATABASE_URL

```bash
railway variables
```

Debe mostrar `DATABASE_URL` con formato:
```
postgresql://postgres:password@host:port/dbname
```

### Opción 3: Reiniciar Servicio

```bash
railway restart
```

## ✅ Verificación Final

1. **Healthcheck**:
   ```bash
   curl https://tu-proyecto.railway.app/health/
   ```
   
   Debe retornar:
   ```json
   {
     "status": "healthy",
     "checks": {
       "database": "healthy",
       "bunny_storage": "healthy"
     }
   }
   ```

2. **Admin**:
   ```
   https://tu-proyecto.railway.app/admin/
   ```

3. **Logs sin errores**:
   ```bash
   railway logs
   ```

---

**El error debería estar resuelto ahora.** Si persiste, verificar que `DATABASE_URL` esté configurado en Railway.

