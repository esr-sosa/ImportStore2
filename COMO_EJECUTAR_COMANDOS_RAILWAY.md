# 🚀 Cómo Ejecutar Comandos Django en Railway

## ✅ Opción 1: Automático (Ya Configurado)

**¡Buenas noticias!** El comando `fix_inventario_schema` ya está configurado para ejecutarse **automáticamente** cada vez que Railway hace un deploy.

Esto significa que:
- Cuando hagas `git push`, Railway hará un nuevo deploy
- El script `start_railway.sh` ejecutará automáticamente el comando
- Las columnas se crearán automáticamente si faltan

**No necesitas hacer nada manual**, solo hacer push de los cambios.

---

## 🔧 Opción 2: Railway CLI (Recomendado para comandos manuales)

### Instalar Railway CLI

```bash
# macOS
brew install railway

# O con npm
npm i -g @railway/cli
```

### Autenticarse

```bash
railway login
```

### Ejecutar el comando

```bash
# Conectarse al proyecto
railway link

# O especificar el proyecto directamente
railway run --service <nombre-del-servicio> python manage.py fix_inventario_schema
```

### Ejemplo completo:

```bash
# 1. Ir al directorio del proyecto
cd /Users/emanuelsosa/Documents/GitHub/ImportStore

# 2. Conectarse a Railway
railway link

# 3. Ejecutar el comando
railway run python manage.py fix_inventario_schema
```

---

## 🌐 Opción 3: Desde Railway Dashboard (Web Console)

### Paso 1: Abrir Railway Dashboard
1. Ve a [railway.app](https://railway.app/)
2. Inicia sesión
3. Selecciona tu proyecto

### Paso 2: Abrir la Terminal
1. Click en tu servicio (Backend)
2. Ve a la pestaña **"Deployments"** o **"Logs"**
3. Busca el botón **"Shell"** o **"Terminal"** (si está disponible)
4. O ve a **"Settings"** → **"Service"** → **"Shell"**

### Paso 3: Ejecutar el comando
```bash
cd sistema_negocio
python manage.py fix_inventario_schema
```

**Nota:** No todos los planes de Railway tienen acceso a la terminal web. Si no ves esta opción, usa Railway CLI.

---

## 📋 Opción 4: Forzar un Nuevo Deploy

Si quieres que el comando se ejecute automáticamente (ya está configurado):

```bash
# Hacer un commit vacío para forzar un nuevo deploy
git commit --allow-empty -m "Force Railway rebuild para ejecutar fix_inventario_schema"
git push origin main
```

Railway hará un nuevo deploy y el script ejecutará automáticamente:
- ✅ Crear migraciones pendientes
- ✅ Ejecutar migraciones
- ✅ **Ejecutar fix_inventario_schema** (crear columnas faltantes)
- ✅ Iniciar el servidor

---

## 🔍 Verificar que Funcionó

### Desde los Logs de Railway:

1. Ve a Railway Dashboard → Tu Proyecto → Tu Servicio
2. Click en **"Deployments"** → Selecciona el último deploy
3. Busca en los logs:
   ```
   🔧 Verificando y creando columnas faltantes en inventario...
   ✓ inventario_productovariante.sku creada exitosamente
   ✓ inventario_productovariante.stock_actual creada exitosamente
   ...
   ✓ Caché del inspector limpiado
   ```

### Desde la Aplicación:

1. Abre tu dashboard en Railway
2. Ve a la sección de Inventario
3. Si las columnas se crearon correctamente, **no verás el mensaje de error** sobre columnas faltantes

---

## 🛠️ Otros Comandos Útiles

### Ver estado de migraciones:
```bash
railway run python manage.py showmigrations
```

### Crear migraciones:
```bash
railway run python manage.py makemigrations
```

### Ejecutar migraciones:
```bash
railway run python manage.py migrate
```

### Ver qué columnas faltan (dry-run):
```bash
railway run python manage.py fix_inventario_schema --dry-run
```

---

## ⚠️ Solución de Problemas

### Error: "railway: command not found"
- Instala Railway CLI (ver Opción 2)

### Error: "No project linked"
- Ejecuta `railway link` en el directorio del proyecto

### El comando no se ejecuta automáticamente
- Verifica que `start_railway.sh` esté en el repositorio
- Verifica que `railway.json` use el script correcto
- Revisa los logs del deploy para ver qué está pasando

### Las columnas aún no se crean
- Revisa los logs de Railway para ver errores
- Ejecuta el comando manualmente con Railway CLI
- Verifica que la base de datos esté conectada correctamente

---

## 📝 Resumen Rápido

**Para ejecutar manualmente:**
```bash
railway run python manage.py fix_inventario_schema
```

**Para que se ejecute automáticamente:**
```bash
git push origin main
# (Ya está configurado en start_railway.sh)
```

---

**¡Listo!** Con estas opciones podrás ejecutar cualquier comando de Django en Railway. 🚀

