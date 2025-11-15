# 📱 Guía Completa: Conectar WhatsApp Business API

## 🎯 **PASO 1: Crear una App en Meta for Developers**

1. **Ir a Meta for Developers**
   - Entrá a: https://developers.facebook.com/
   - Iniciá sesión con tu cuenta de Facebook

2. **Crear una App**
   - Click en "Mis Apps" → "Crear App"
   - Seleccioná "Negocio" como tipo de app
   - Completá:
     - **Nombre de la app**: `ImportStore WhatsApp` (o el que prefieras)
     - **Email de contacto**: Tu email
     - **Propósito comercial**: Seleccioná el que corresponda

3. **Agregar WhatsApp**
   - En el dashboard de tu app, buscá "WhatsApp" en el menú
   - Click en "Configurar" o "Agregar producto"
   - Seleccioná "WhatsApp Business API"

---

## 🎯 **PASO 2: Obtener el Access Token**

1. **Ir a WhatsApp → Configuración API**
   - En el menú lateral, click en "WhatsApp" → "Configuración API"

2. **Obtener Token Temporal (para pruebas)**
   - En la sección "Token de acceso temporal"
   - Click en "Generar token"
   - **Copiá este token** (lo vas a necesitar para el `.env`)

3. **Token Permanente (para producción)**
   - Para producción, necesitás crear un token permanente
   - Esto requiere verificar tu negocio en Meta Business Manager
   - Por ahora, usá el token temporal para pruebas

---

## 🎯 **PASO 3: Obtener el Phone Number ID**

1. **En la misma página de "Configuración API"**
   - Buscá la sección "Identificador de número de teléfono"
   - **Copiá el ID** (es un número largo, tipo: `123456789012345`)

2. **Si no tenés un número de teléfono:**
   - Meta te da un número de prueba temporal
   - O podés agregar tu número real (requiere verificación)

---

## 🎯 **PASO 4: Configurar el Webhook**

### **4.1. Crear un Token de Verificación**

1. **Elegí un token secreto** (puede ser cualquier string, ej: `mi_token_secreto_123`)
2. **Guardalo** porque lo vas a usar en el `.env`

### **4.2. Configurar el Webhook en Meta**

1. **En WhatsApp → Configuración API**
   - Scroll hasta "Webhook"
   - Click en "Configurar webhook"

2. **Completar los campos:**
   - **URL de devolución de llamada**: 
     ```
     https://tu-dominio.com/webhook/
     ```
     ⚠️ **IMPORTANTE**: 
     - Si estás en desarrollo local, necesitás usar **ngrok** o similar
     - Ejemplo con ngrok: `https://abc123.ngrok-free.app/webhook/`
   
   - **Token de verificación**: 
     ```
     mi_token_secreto_123
     ```
     (El mismo que pusiste en el `.env`)

3. **Suscribirse a campos:**
   - Marcá: `messages`
   - Click en "Verificar y guardar"

### **4.3. Configurar ngrok (para desarrollo local)**

Si estás probando en local, necesitás exponer tu servidor:

```bash
# Instalar ngrok (si no lo tenés)
# Descargalo de: https://ngrok.com/download

# Ejecutar ngrok
ngrok http 8000
```

Esto te va a dar una URL tipo: `https://abc123.ngrok-free.app`

**Usá esa URL** en la configuración del webhook:
```
https://abc123.ngrok-free.app/webhook/
```

---

## 🎯 **PASO 5: Configurar el archivo .env**

1. **Abrí el archivo `.env`** en `sistema_negocio/.env`

2. **Agregá estas variables:**

```env
# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=tu_access_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_123
```

**Ejemplo:**
```env
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_123
```

---

## 🎯 **PASO 6: Verificar que Funciona**

1. **Iniciá el servidor Django:**
   ```bash
   python manage.py runserver
   ```

2. **Verificá el webhook:**
   - Meta va a hacer una petición GET a tu webhook para verificar
   - Si todo está bien, deberías ver en la consola: "Webhook verificado con éxito!"

3. **Enviá un mensaje de prueba:**
   - Desde WhatsApp, enviá un mensaje al número de prueba
   - Deberías ver el mensaje aparecer en el panel de chat: `/chat/`

---

## 🔍 **Troubleshooting (Solución de Problemas)**

### **Error: "Configuración de WhatsApp faltante"**
- Verificá que las 3 variables estén en el `.env`
- Verificá que no haya espacios extra
- Reiniciá el servidor Django

### **Error: "Webhook verification failed"**
- Verificá que el `WHATSAPP_VERIFY_TOKEN` en el `.env` sea **exactamente igual** al que pusiste en Meta
- Verificá que la URL del webhook sea accesible públicamente (usá ngrok si estás en local)

### **Error: "Invalid OAuth access token"**
- El token puede haber expirado (los tokens temporales duran 24 horas)
- Generá un nuevo token en Meta for Developers
- Actualizá el `.env` y reiniciá el servidor

### **No llegan mensajes al webhook**
- Verificá que el webhook esté suscrito a "messages"
- Verificá que la URL del webhook sea correcta
- Verificá los logs de Django para ver si hay errores

### **ngrok no funciona**
- Verificá que ngrok esté corriendo
- Verificá que el puerto sea el correcto (8000 por defecto)
- Actualizá la URL del webhook en Meta si cambió

---

## 📋 **Checklist de Configuración**

- [ ] App creada en Meta for Developers
- [ ] WhatsApp agregado como producto
- [ ] Access Token obtenido y guardado en `.env`
- [ ] Phone Number ID obtenido y guardado en `.env`
- [ ] Verify Token creado y guardado en `.env`
- [ ] Webhook configurado en Meta (con URL pública)
- [ ] Webhook verificado exitosamente
- [ ] Suscripción a "messages" activada
- [ ] Servidor Django corriendo
- [ ] Mensaje de prueba enviado y recibido

---

## 🔗 **URLs Importantes**

- **Meta for Developers**: https://developers.facebook.com/
- **Tu App Dashboard**: https://developers.facebook.com/apps/
- **WhatsApp API Docs**: https://developers.facebook.com/docs/whatsapp
- **ngrok**: https://ngrok.com/

---

## 💡 **Tips**

1. **Tokens temporales**: Los tokens temporales duran 24 horas. Para producción, necesitás un token permanente.

2. **Número de prueba**: Meta te da un número de prueba que solo puede recibir mensajes de números verificados. Para enviar a cualquier número, necesitás verificar tu negocio.

3. **Límites**: En modo de prueba, hay límites de mensajes. Para producción, necesitás verificar tu negocio.

4. **Webhook público**: El webhook DEBE ser accesible desde internet. No puede ser `localhost` o `127.0.0.1`.

---

## 🚀 **Próximos Pasos**

Una vez que todo funcione:

1. **Verificar tu negocio** en Meta Business Manager para obtener tokens permanentes
2. **Agregar tu número real** de WhatsApp Business
3. **Configurar respuestas automáticas** (ya está implementado con IA)
4. **Configurar plantillas de mensajes** para mensajes promocionales

---

¿Necesitás ayuda con algún paso específico? 🚀

