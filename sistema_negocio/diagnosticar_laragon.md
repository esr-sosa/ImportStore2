# Diagnóstico de Laragon que se cierra solo

## Pasos para diagnosticar:

### 1. Verificar los logs de Laragon
- Abrí Laragon
- Click en "Logs" o "Ver logs"
- Buscá errores recientes

### 2. Verificar puertos ocupados
Laragon usa estos puertos por defecto:
- MySQL: 3306
- Apache: 80
- Nginx: 443

### 3. Verificar servicios de Windows
- Abrí "Servicios" (Win+R → services.msc)
- Buscá servicios de MySQL o Apache
- Verificá si están corriendo o fallando

### 4. Ejecutar como Administrador
- Click derecho en Laragon → "Ejecutar como administrador"

### 5. Verificar antivirus
- Algunos antivirus bloquean Laragon
- Agregá Laragon a las excepciones

### 6. Revisar Event Viewer de Windows
- Win+R → eventvwr.msc
- Windows Logs → Application
- Buscá errores relacionados con MySQL o Apache

