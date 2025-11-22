# 🌐 Generar Dominio Público en Railway

## 📍 Pasos para Obtener la URL

### Paso 1: Ir a la Sección Networking

En Railway Dashboard → Tu Proyecto → Tu Servicio (importstore2):

1. Scroll hacia abajo hasta la sección **"Networking"**
2. Verás **"Public Networking"**

### Paso 2: Generar Dominio

1. En **"Public Networking"**, busca el botón **"Generate Domain"**
2. **Click en "Generate Domain"**
3. Railway generará automáticamente una URL como:
   ```
   https://importstore2-production-xxxx.up.railway.app
   ```

### Paso 3: Copiar la URL

1. Una vez generada, verás la URL en la sección **"Domains"**
2. Click en el botón **"Copy"** o copia manualmente la URL

---

## ✅ Verificar que Funciona

Una vez que tengas la URL:

### 1. Probar Healthcheck

Abre en el navegador:
```
https://tu-url.railway.app/health/
```

Debería mostrar:
```json
{
  "status": "healthy",
  "checks": {
    "database": "healthy (mysql)"
  }
}
```

### 2. Probar el Backend

Abre en el navegador:
```
https://tu-url.railway.app/
```

Debería mostrar la página de inicio de Django o redirigir al login.

---

## 📋 Resumen Rápido

1. **Railway Dashboard** → Tu Proyecto → Servicio "importstore2"
2. **Scroll a "Networking"**
3. **Click en "Generate Domain"**
4. **Copiar la URL generada**

---

## 💡 Nota

- La URL será algo como: `https://importstore2-production-xxxx.up.railway.app`
- Esta URL es pública y accesible desde internet
- La necesitarás para configurar el frontend y CORS

---

**¡Listo!** Una vez que generes el dominio, tendrás la URL pública de tu backend.

