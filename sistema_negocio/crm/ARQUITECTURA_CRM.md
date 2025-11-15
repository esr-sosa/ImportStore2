# 🚀 Arquitectura CRM - WhatsApp & Instagram
## Sistema Inteligente de Gestión de Conversaciones

---

## 📋 **VISIÓN GENERAL**

Sistema CRM integrado que conecta WhatsApp e Instagram con el negocio completo:
- **IA Inteligente (ISAC)** que responde automáticamente consultas de clientes
- **Integración total** con inventario, ventas, y productos
- **Automatizaciones** inteligentes para ventas y seguimiento
- **Panel unificado** para asesores humanos
- **Tiempo real** con WebSockets

---

## 🏗️ **ARQUITECTURA DEL SISTEMA**

### **1. FLUJO DE MENSAJES ENTRANTES**

```
Cliente (WhatsApp/Instagram)
    ↓
Webhook (Meta API)
    ↓
[crm/views.py] → whatsapp_webhook() / instagram_webhook()
    ↓
1. Crear/Actualizar Cliente
2. Crear/Actualizar Conversación
3. Guardar Mensaje
4. Notificar Frontend (WebSocket)
    ↓
¿Requiere IA?
    ↓ SÍ
[asistente_ia/interpreter.py] → ISAC
    ↓
- Consultar inventario
- Buscar productos
- Responder preguntas
- Generar respuestas
    ↓
Enviar respuesta automática
    ↓
¿Requiere intervención humana?
    ↓ SÍ
Asignar a asesor
Notificar en panel
```

### **2. COMPONENTES PRINCIPALES**

#### **A. Webhooks (Entrada de Mensajes)**
- `whatsapp_webhook()` - Recibe mensajes de WhatsApp
- `instagram_webhook()` - Recibe mensajes de Instagram
- Normalización de números de teléfono
- Manejo de diferentes tipos de mensajes (texto, imagen, audio, video)

#### **B. Motor de IA (ISAC CRM)**
- **Análisis de intención**: ¿Qué quiere el cliente?
  - Consulta de producto
  - Consulta de precio
  - Consulta de stock
  - Solicitud de compra
  - Consulta de garantía
  - Reclamo/Problema
  
- **Respuestas automáticas inteligentes**:
  - Buscar productos en inventario
  - Mostrar precios y disponibilidad
  - Sugerir productos similares
  - Responder preguntas frecuentes
  - Generar enlaces de compra

- **Escalamiento inteligente**:
  - Detectar cuando necesita asesor humano
  - Asignar prioridad automática
  - Crear tareas de seguimiento

#### **C. Panel de Asesores**
- Vista unificada de todas las conversaciones
- Filtros por estado, prioridad, fuente
- Chat en tiempo real
- Acciones rápidas:
  - Enviar productos
  - Crear cotización
  - Generar venta
  - Transferir conversación

#### **D. Integraciones**
- **Inventario**: Búsqueda de productos, stock, precios
- **Ventas**: Crear ventas desde el chat
- **Clientes**: Actualizar información automáticamente
- **Historial**: Registrar todas las interacciones

---

## 🎯 **FUNCIONALIDADES CLAVE**

### **1. RESPUESTAS AUTOMÁTICAS INTELIGENTES**

#### **Consultas de Productos**
```
Cliente: "tenes iphone 15?"
ISAC: 
  - Busca en inventario
  - Muestra productos disponibles
  - Precios y stock
  - Enlaces a más info
```

#### **Consultas de Precio**
```
Cliente: "cuanto sale el iphone 15 pro 256gb?"
ISAC:
  - Busca producto específico
  - Muestra precio minorista/mayorista
  - Opción de crear cotización
```

#### **Consultas de Stock**
```
Cliente: "hay stock de cargadores?"
ISAC:
  - Busca en inventario
  - Muestra disponibilidad
  - Sugiere alternativas si no hay
```

#### **Solicitudes de Compra**
```
Cliente: "quiero comprar un iphone 15"
ISAC:
  - Pregunta especificaciones (capacidad, color)
  - Verifica stock
  - Genera cotización
  - Ofrece métodos de pago
  - Crea venta si confirma
```

### **2. AUTOMATIZACIONES INTELIGENTES**

#### **A. Detección de Intención de Compra**
- Analiza mensajes para detectar intención de compra
- Crea automáticamente cotizaciones
- Envía información de pago
- Programa seguimiento

#### **B. Seguimiento Automático**
- Si el cliente no responde en X horas, enviar recordatorio
- Si hay productos en cotización, recordar antes de que expire
- Seguimiento post-venta automático

#### **C. Clasificación de Clientes**
- Detecta automáticamente tipo de cliente (Minorista/Mayorista)
- Asigna etiquetas según comportamiento
- Prioriza conversaciones según valor potencial

#### **D. Sugerencias Inteligentes**
- Sugiere productos relacionados
- Ofrece descuentos según historial
- Recomienda productos en stock

### **3. ACCIONES RÁPIDAS PARA ASESORES**

#### **Desde el Chat:**
- 📦 **Enviar producto**: Seleccionar producto y enviar info al cliente
- 💰 **Crear cotización**: Generar cotización con productos seleccionados
- 🛒 **Crear venta**: Convertir conversación en venta
- 📋 **Ver historial**: Ver compras anteriores del cliente
- 🔄 **Transferir**: Pasar conversación a otro asesor
- ⏰ **Programar seguimiento**: Agendar recordatorio

### **4. INTEGRACIÓN CON VENTAS**

#### **Crear Venta desde Chat**
```
Asesor selecciona productos en el chat
    ↓
Crea venta directamente
    ↓
Genera comprobante PDF
    ↓
Envía comprobante por WhatsApp/Instagram
    ↓
Registra en sistema de ventas
```

---

## 🔧 **IMPLEMENTACIÓN TÉCNICA**

### **1. ESTRUCTURA DE ARCHIVOS**

```
crm/
├── models.py          # Cliente, Conversacion, Mensaje (ya existe)
├── views.py           # Webhooks, panel, acciones
├── services/
│   ├── ai_service.py      # Lógica de IA para CRM
│   ├── whatsapp_service.py   # Envío de mensajes (ya existe)
│   ├── instagram_service.py  # Envío de mensajes Instagram
│   ├── automation_service.py # Automatizaciones
│   └── intent_detector.py    # Detección de intención
├── utils/
│   ├── message_parser.py     # Parsear mensajes
│   ├── product_sender.py     # Enviar productos
│   └── quote_generator.py    # Generar cotizaciones
└── templates/
    └── crm/
        ├── panel_chat.html   # Panel principal (ya existe)
        └── chat_detail.html  # Vista de conversación
```

### **2. NUEVOS MODELOS NECESARIOS**

```python
# crm/models.py

class Cotizacion(models.Model):
    """Cotización generada desde una conversación"""
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.JSONField()  # Lista de productos con precios
    total = models.DecimalField(max_digits=12, decimal_places=2)
    valido_hasta = models.DateTimeField()
    estado = models.CharField(...)  # Pendiente, Aceptada, Rechazada, Expirada
    venta_relacionada = models.ForeignKey(Venta, null=True, blank=True)

class TareaSeguimiento(models.Model):
    """Tareas automáticas de seguimiento"""
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    tipo = models.CharField(...)  # Recordatorio, Seguimiento, Post-venta
    fecha_programada = models.DateTimeField()
    completada = models.BooleanField(default=False)
    mensaje_automatico = models.TextField()

class AccionRapida(models.Model):
    """Acciones rápidas predefinidas"""
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(...)  # Mensaje, Producto, Cotización
    contenido = models.TextField()
    activo = models.BooleanField(default=True)
```

### **3. SERVICIO DE IA PARA CRM**

```python
# crm/services/ai_service.py

def analizar_mensaje_cliente(mensaje: str, historial: list, cliente: Cliente) -> dict:
    """
    Analiza un mensaje del cliente y determina:
    - Intención (consulta, compra, reclamo, etc.)
    - Productos mencionados
    - Urgencia
    - Si requiere intervención humana
    """
    pass

def generar_respuesta_automatica(intencion: str, contexto: dict) -> str:
    """
    Genera respuesta automática basada en:
    - Intención detectada
    - Productos en inventario
    - Historial del cliente
    - Reglas de negocio
    """
    pass

def detectar_escalamiento(mensaje: str, historial: list) -> bool:
    """
    Determina si la conversación necesita intervención humana
    """
    pass
```

---

## 📱 **INTEGRACIÓN WHATSAPP E INSTAGRAM**

### **WhatsApp (Meta Business API)**
- ✅ Webhook ya implementado
- ✅ Envío de mensajes ya implementado
- 🔄 Mejorar: Manejo de imágenes, botones, listas

### **Instagram (Meta Business API)**
- ❌ Webhook pendiente
- ❌ Envío de mensajes pendiente
- 🔄 Similar a WhatsApp pero con API específica

### **Funcionalidades Adicionales**
- **Botones interactivos**: "Ver productos", "Consultar precio", "Hablar con asesor"
- **Listas de productos**: Enviar catálogo interactivo
- **Imágenes de productos**: Enviar fotos automáticamente
- **Ubicación**: Enviar ubicación de tienda
- **Documentos**: Enviar comprobantes, cotizaciones PDF

---

## 🎨 **MEJORAS AL PANEL DE CHAT**

### **Vista de Conversaciones**
- Filtros avanzados (estado, prioridad, fuente, asesor)
- Búsqueda de conversaciones
- Vista de kanban (Abiertas, En seguimiento, Cerradas)
- Notificaciones en tiempo real

### **Vista de Chat Individual**
- Historial completo de mensajes
- Información del cliente (compras anteriores, preferencias)
- Productos sugeridos
- Acciones rápidas
- Notas internas
- Etiquetas

### **Widgets Inteligentes**
- **Productos relacionados**: Sugerencias basadas en la conversación
- **Historial de compras**: Ver qué compró antes
- **Cotizaciones activas**: Ver cotizaciones pendientes
- **Tareas pendientes**: Seguimientos programados

---

## 🚀 **ROADMAP DE IMPLEMENTACIÓN**

### **Fase 1: Mejoras Básicas (Ahora)**
1. ✅ Mejorar detección de intención en ISAC
2. ✅ Integrar búsqueda de productos en respuestas automáticas
3. ✅ Mejorar panel de chat (diseño y funcionalidad)
4. ✅ Agregar acciones rápidas básicas

### **Fase 2: Automatizaciones (Siguiente)**
1. Sistema de cotizaciones automáticas
2. Seguimiento automático
3. Clasificación automática de clientes
4. Sugerencias inteligentes

### **Fase 3: Instagram (Después)**
1. Webhook de Instagram
2. Envío de mensajes por Instagram
3. Panel unificado WhatsApp + Instagram

### **Fase 4: Avanzado (Futuro)**
1. Botones interactivos
2. Catálogos interactivos
3. Integración con pagos
4. Analytics y reportes

---

## 💡 **EJEMPLOS DE USO**

### **Ejemplo 1: Cliente consulta producto**
```
Cliente: "Hola, tenes iphone 15 pro?"
ISAC: "¡Hola! Sí, tenemos iPhone 15 Pro disponible. ¿Qué capacidad necesitás?
      - 128GB
      - 256GB  
      - 512GB
      - 1TB
      
      También tenemos en diferentes colores. ¿Cuál te interesa?"
```

### **Ejemplo 2: Cliente quiere comprar**
```
Cliente: "Quiero el 256gb en azul"
ISAC: "Perfecto! iPhone 15 Pro 256GB Azul está disponible.
      Precio: $1,500,000 ARS
      
      ¿Querés que te prepare la cotización? 
      También podés retirar en tienda o hacemos envío."
```

### **Ejemplo 3: Escalamiento a asesor**
```
Cliente: "Tengo un problema con mi compra anterior"
ISAC: "Entiendo, voy a conectarte con un asesor que te va a ayudar mejor.
      En un momento te atiende."
      
[Asesor recibe notificación]
[Asesor puede ver historial completo]
```

---

## 🔐 **CONSIDERACIONES IMPORTANTES**

1. **Privacidad**: Todos los mensajes se guardan de forma segura
2. **Escalabilidad**: Sistema debe manejar múltiples conversaciones simultáneas
3. **Performance**: Respuestas de IA deben ser rápidas (< 3 segundos)
4. **Fallbacks**: Si la IA falla, escalar a asesor humano
5. **Testing**: Probar con casos reales antes de producción

---

## 📊 **MÉTRICAS Y ANALYTICS**

- Conversaciones atendidas por IA vs humano
- Tiempo de respuesta promedio
- Tasa de conversión (consulta → venta)
- Productos más consultados
- Horarios pico de consultas
- Satisfacción del cliente

---

¿Empezamos con la Fase 1? 🚀

