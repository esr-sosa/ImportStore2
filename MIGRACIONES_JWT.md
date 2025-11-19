# Migraciones necesarias para JWT y nuevos modelos

## Pasos para aplicar las migraciones

```bash
cd sistema_negocio
source venv/bin/activate  # En Mac/Linux
# o venv\Scripts\activate en Windows

# Crear migraciones
python manage.py makemigrations core

# Aplicar migraciones
python manage.py migrate core
```

## Modelos nuevos creados

1. **PerfilUsuario**: Extiende el modelo User con:
   - `tipo_usuario` (MINORISTA/MAYORISTA)
   - `telefono`, `direccion`, `ciudad`, `codigo_postal`
   - `documento`, `fecha_nacimiento`

2. **DireccionEnvio**: Direcciones de envío de usuarios
   - Relación con User
   - Campos de dirección completos
   - Soporte para dirección principal

3. **Favorito**: Productos favoritos
   - Relación User -> ProductoVariante
   - Unique constraint para evitar duplicados

## Notas importantes

- Los modelos están en `sistema_negocio/core/models.py`
- Las migraciones se crearán automáticamente al ejecutar `makemigrations`
- Asegúrate de tener una copia de seguridad de la BD antes de migrar

