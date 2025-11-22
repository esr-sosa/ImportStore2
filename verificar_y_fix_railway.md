# 🔧 Solución para Error 500 en Railway

## Problema Identificado

1. **Error Principal**: Railway está usando `ConfiguracionSistema.carga()` que no existe
   - El código local ya está correcto usando `ConfiguracionSistema.obtener_unica()`
   - Esto indica que Railway está usando una versión antigua del código

2. **Migraciones Pendientes**: Django detecta cambios en modelos `core` y `ventas`

## Solución Paso a Paso

### 1. Verificar que el código esté commiteado

```bash
git status
git log --oneline -5  # Ver últimos commits
```

### 2. Asegurar que el código esté pusheado a GitHub

```bash
git push origin main
```

### 3. Forzar nuevo build en Railway

1. Ve a tu proyecto en Railway
2. Ve a la pestaña "Deployments"
3. Haz clic en "Redeploy" o "Deploy Latest Commit"
4. O simplemente haz un commit vacío para forzar un nuevo build:
   ```bash
   git commit --allow-empty -m "Force Railway rebuild"
   git push origin main
   ```

### 4. Crear migraciones pendientes (localmente primero)

Si tienes acceso local con Django instalado:

```bash
cd sistema_negocio
python manage.py makemigrations core
python manage.py makemigrations ventas
```

Luego commitea y pushea las migraciones:

```bash
git add sistema_negocio/core/migrations/
git add sistema_negocio/ventas/migrations/
git commit -m "Crear migraciones pendientes para core y ventas"
git push origin main
```

### 5. Verificar el código en Railway

El archivo `sistema_negocio/core/views.py` línea 29 debe tener:

```python
sistema = ConfiguracionSistema.obtener_unica()
```

NO debe tener:
```python
sistema = ConfiguracionSistema.carga()  # ❌ INCORRECTO
```

## Verificación Post-Deploy

Después del nuevo deploy, verifica:

1. Los logs de Railway no deben mostrar el error `AttributeError: type object 'ConfiguracionSistema' has no attribute 'carga'`
2. La aplicación debe cargar correctamente en `/acceso/`
3. Las migraciones deben aplicarse correctamente

## Si el problema persiste

1. Verifica que Railway esté usando el branch correcto (main)
2. Verifica que el Dockerfile esté copiando el código correcto
3. Revisa los logs de Railway para ver qué versión del código se está usando
4. Considera limpiar el caché de Railway o hacer un deploy desde cero

