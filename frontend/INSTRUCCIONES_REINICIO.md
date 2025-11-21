# Instrucciones para aplicar los cambios de botones

## Pasos necesarios:

### 1. Detener el servidor de desarrollo
Si tienes el servidor corriendo (npm run dev o yarn dev), detenlo con `Ctrl+C`

### 2. Limpiar la caché de Next.js
Ejecuta estos comandos en la terminal:

```bash
cd frontend
rm -rf .next
```

### 3. Reiniciar el servidor
```bash
npm run dev
# o
yarn dev
```

### 4. Limpiar la caché del navegador
- **Chrome/Edge**: Presiona `Ctrl+Shift+Delete` (Windows) o `Cmd+Shift+Delete` (Mac)
- Selecciona "Imágenes y archivos en caché"
- Haz clic en "Borrar datos"
- O simplemente presiona `Ctrl+F5` (Windows) o `Cmd+Shift+R` (Mac) para forzar recarga

### 5. Verificar los cambios
Los botones ahora deberían:
- ✅ Mostrarse con el color correcto desde el inicio (sin cambios de color)
- ✅ Tener texto blanco visible sobre fondo coloreado
- ✅ No tener problemas de contraste

## Si el problema persiste:

1. Cierra completamente el navegador y vuelve a abrirlo
2. Prueba en modo incógnito/privado
3. Verifica que el archivo `frontend/app/globals.css` tenga la clase `.btn-primary`

