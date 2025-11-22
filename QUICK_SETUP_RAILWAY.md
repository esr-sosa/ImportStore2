# ⚡ Setup Rápido en Railway

## 🎯 Pasos Rápidos

### 1. Agregar PostgreSQL (NO MySQL)

En Railway Dashboard:
- Click en **+ New** → **Database** → **Add PostgreSQL**
- Railway inyectará automáticamente `DATABASE_URL`

### 2. Variables Mínimas Necesarias

Copiar y pegar estas variables en Railway Dashboard → **Variables**:

```env
DJANGO_SECRET_KEY=GENERAR-NUEVA-KEY-AQUI
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

### 3. Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar el resultado y pegarlo en `DJANGO_SECRET_KEY`.

---

## ❌ Eliminar Variables de MySQL

Si ya pusiste variables de MySQL, **elimínalas todas**:

- ❌ `MYSQL_DATABASE`
- ❌ `MYSQL_PUBLIC_URL`
- ❌ `MYSQL_ROOT_PASSWORD`
- ❌ `MYSQL_URL`
- ❌ `MYSQLDATABASE`
- ❌ `MYSQLHOST`
- ❌ `MYSQLPASSWORD`
- ❌ `MYSQLPORT`
- ❌ `MYSQLUSER`

**Eliminar todas estas variables** en Railway Dashboard → Variables.

---

## ✅ Verificar

```bash
railway variables
```

Debe mostrar:
- ✅ `DATABASE_URL` (automático, formato `postgresql://...`)
- ✅ Variables de Django
- ✅ Variables de Bunny Storage
- ❌ NO debe mostrar variables de MySQL

---

**¡Listo!** Railway debería funcionar correctamente ahora.

