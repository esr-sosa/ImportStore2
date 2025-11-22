# 🔗 Cómo Obtener la URL de tu Proyecto en Railway

## 📍 Método 1: Desde Railway Dashboard (Más Fácil)

### Paso 1: Ir a Railway Dashboard
1. Abrir [railway.app](https://railway.app/)
2. Iniciar sesión
3. Seleccionar tu proyecto

### Paso 2: Encontrar la URL
1. En la página del proyecto, verás tu servicio (Backend)
2. Click en el servicio
3. Ir a la pestaña **"Settings"** o **"Deployments"**
4. Buscar la sección **"Domains"** o **"Public URL"**
5. Ahí verás la URL, algo como:
   ```
   https://tu-proyecto-production-xxxx.up.railway.app
   ```

### Paso 3: Copiar la URL
- Click en el botón **"Copy"** o copiar manualmente la URL

---

## 📍 Método 2: Desde la Página Principal del Proyecto

1. En Railway Dashboard → Tu Proyecto
2. En la parte superior, verás un botón con un ícono de **"globo"** o **"link"**
3. Click ahí y te mostrará la URL pública
4. También puede aparecer directamente en la tarjeta del servicio

---

## 📍 Método 3: Generar un Dominio Público

Si no tienes una URL pública:

1. Ir a Railway Dashboard → Tu Proyecto → Tu Servicio
2. Ir a **"Settings"** → **"Networking"**
3. Click en **"Generate Domain"** o **"Add Domain"**
4. Railway generará una URL automáticamente

---

## 🔍 Ejemplo de URL

Las URLs de Railway suelen verse así:

```
https://backend-production-xxxx.up.railway.app
```

O si configuraste un dominio personalizado:

```
https://api.tu-dominio.com
```

---

## ✅ Verificar que Funciona

Una vez que tengas la URL:

### 1. Probar Healthcheck
```bash
curl https://tu-url.railway.app/health/
```

O abrir en el navegador:
```
https://tu-url.railway.app/health/
```

Debería retornar:
```json
{
  "status": "healthy",
  "checks": {
    "database": "healthy (mysql)"
  }
}
```

### 2. Probar el Backend
```bash
curl https://tu-url.railway.app/
```

O abrir en el navegador:
```
https://tu-url.railway.app/
```

---

## 📋 Resumen Rápido

1. **Railway Dashboard** → Tu Proyecto
2. **Click en el servicio** (Backend)
3. **Settings** → **Domains** o buscar **Public URL**
4. **Copiar la URL**

---

## 💡 Tip

Si no ves una URL pública, Railway puede estar esperando a que el servicio esté completamente desplegado. Espera unos minutos y vuelve a revisar.

---

**¡Listo!** Con esa URL podrás acceder a tu backend y también la usarás para configurar el frontend.

