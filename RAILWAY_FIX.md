# 🔧 Fix para Error de MySQL en Railway

## Problema

Railway está intentando conectarse a MySQL en `localhost` cuando debería usar PostgreSQL a través de `DATABASE_URL`.

## Solución Aplicada

### 1. Detección Automática de DATABASE_URL

Se modificó `sistema_negocio/core/settings.py` para detectar automáticamente `DATABASE_URL` y usar PostgreSQL si está presente.

### 2. Dockerfile Actualizado

- Agregado `ENV DJANGO_SETTINGS_MODULE=core.settings_railway`
- Creado script `start_railway.sh` que detecta automáticamente el entorno

### 3. Script de Inicio Inteligente

El script `start_railway.sh`:
- Detecta si `DATABASE_URL` está presente
- Usa `settings_railway` automáticamente
- Ejecuta migraciones y collectstatic
- Inicia Gunicorn

## Verificación

### En Railway Dashboard

1. **Verificar Variables de Entorno**:
   - `DATABASE_URL` debe estar presente (Railway lo inyecta automáticamente)
   - `DJANGO_SETTINGS_MODULE` puede estar configurado como `core.settings_railway` (opcional, el script lo detecta)

2. **Verificar Logs**:
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

### Si el Error Persiste

1. **Forzar settings_railway**:
   En Railway Dashboard → Variables, agregar:
   ```
   DJANGO_SETTINGS_MODULE=core.settings_railway
   ```

2. **Verificar DATABASE_URL**:
   ```bash
   railway variables
   ```
   
   Debe mostrar `DATABASE_URL` con formato:
   ```
   postgresql://postgres:password@host:port/dbname
   ```

3. **Reiniciar el servicio**:
   ```bash
   railway restart
   ```

## Cambios Realizados

1. ✅ `settings.py` - Detecta `DATABASE_URL` automáticamente
2. ✅ `Dockerfile.railway` - Configurado para usar `settings_railway`
3. ✅ `start_railway.sh` - Script inteligente de inicio
4. ✅ `settings_railway.py` - Ya estaba configurado correctamente

## Próximos Pasos

1. Hacer commit y push:
   ```bash
   git add .
   git commit -m "Fix: Detectar DATABASE_URL automáticamente para Railway"
   git push origin main
   ```

2. Railway detectará el cambio y redeployará automáticamente

3. Verificar logs después del deploy

---

**El error debería estar resuelto ahora.** Si persiste, verificar que `DATABASE_URL` esté configurado en Railway.

