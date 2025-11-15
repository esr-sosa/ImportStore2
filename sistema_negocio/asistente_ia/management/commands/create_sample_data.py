# asistente_ia/management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from asistente_ia.models import AssistantQuickReply, AssistantPlaybook, AssistantKnowledgeArticle


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para respuestas rápidas, playbooks y conocimiento'

    def handle(self, *args, **options):
        # Respuestas rápidas
        quick_replies_data = [
            {
                'titulo': 'Consultar stock de iPhone',
                'prompt': '¿Qué modelos de iPhone tenemos en stock? Muestra stock, precios y SKU de cada uno.',
                'categoria': 'inventario',
                'orden': 1,
            },
            {
                'titulo': 'Productos con bajo stock',
                'prompt': 'Muestra todos los productos que tienen stock por debajo del mínimo configurado.',
                'categoria': 'inventario',
                'orden': 2,
            },
            {
                'titulo': 'Ventas del día',
                'prompt': '¿Cuántas ventas se realizaron hoy? Muestra el total y un resumen.',
                'categoria': 'ventas',
                'orden': 1,
            },
            {
                'titulo': 'Productos más vendidos',
                'prompt': 'Muestra los 10 productos más vendidos en el último mes con sus cantidades.',
                'categoria': 'ventas',
                'orden': 2,
            },
            {
                'titulo': 'Precio de un producto',
                'prompt': 'Necesito consultar el precio de un producto. ¿Cómo busco por SKU o nombre?',
                'categoria': 'soporte',
                'orden': 1,
            },
            {
                'titulo': 'Agregar nuevo producto',
                'prompt': '¿Cuál es el proceso para agregar un nuevo producto al inventario?',
                'categoria': 'soporte',
                'orden': 2,
            },
            {
                'titulo': 'Reporte de ingresos',
                'prompt': 'Genera un reporte de ingresos del mes actual con totales por día.',
                'categoria': 'finanzas',
                'orden': 1,
            },
            {
                'titulo': 'Productos sin precio',
                'prompt': 'Muestra todos los productos que no tienen precio configurado.',
                'categoria': 'inventario',
                'orden': 3,
            },
        ]

        self.stdout.write('Creando respuestas rápidas...')
        for data in quick_replies_data:
            reply, created = AssistantQuickReply.objects.get_or_create(
                titulo=data['titulo'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Creada: {reply.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Ya existe: {reply.titulo}'))

        # Playbooks - Enfocados en gestión empresarial interna
        playbooks_data = [
            {
                'titulo': 'Proceso de Venta en POS',
                'descripcion': 'Guía paso a paso para realizar una venta completa desde el POS.',
                'pasos': [
                    {
                        'titulo': 'Buscar productos',
                        'descripcion': 'Usar el buscador del POS para encontrar productos por nombre o SKU. Verificar stock disponible antes de agregar.'
                    },
                    {
                        'titulo': 'Agregar al carrito',
                        'descripcion': 'Seleccionar variantes (color, capacidad, etc.) y cantidad. El sistema valida stock automáticamente.'
                    },
                    {
                        'titulo': 'Aplicar descuentos',
                        'descripcion': 'Si corresponde, aplicar descuentos por cantidad, promociones o ajustes manuales. Verificar que el total sea correcto.'
                    },
                    {
                        'titulo': 'Registrar pago',
                        'descripcion': 'Seleccionar método de pago (efectivo, tarjeta, transferencia, mixto). Ingresar monto recibido y calcular vuelto si aplica.'
                    },
                    {
                        'titulo': 'Emitir comprobante',
                        'descripcion': 'Generar comprobante de venta. Verificar que todos los datos sean correctos antes de enviar al cliente.'
                    },
                    {
                        'titulo': 'Verificar actualización',
                        'descripcion': 'Confirmar que el stock se actualizó correctamente y que la venta quedó registrada en el sistema.'
                    },
                ],
                'es_template': True,
            },
            {
                'titulo': 'Carga de Nuevo Inventario',
                'descripcion': 'Proceso completo para recibir y cargar nueva mercadería al sistema.',
                'pasos': [
                    {
                        'titulo': 'Verificar factura del proveedor',
                        'descripcion': 'Revisar la factura recibida y comparar productos, cantidades y precios con lo recibido físicamente.'
                    },
                    {
                        'titulo': 'Inspeccionar mercadería',
                        'descripcion': 'Verificar que todos los productos estén en buen estado, sin daños, y que coincidan con la factura.'
                    },
                    {
                        'titulo': 'Crear/Actualizar productos',
                        'descripcion': 'Ir a Inventario > Añadir producto. Si el producto ya existe, actualizar stock. Si es nuevo, crear con todos los datos (nombre, categoría, atributos, SKU).'
                    },
                    {
                        'titulo': 'Configurar precios',
                        'descripcion': 'Establecer precios minorista y mayorista en ARS según la política de la empresa. Verificar márgenes de ganancia.'
                    },
                    {
                        'titulo': 'Registrar stock inicial',
                        'descripcion': 'Ingresar la cantidad recibida como stock actual. Configurar stock mínimo si corresponde.'
                    },
                    {
                        'titulo': 'Generar etiquetas',
                        'descripcion': 'Ir a Inventario > Descargar etiquetas seleccionadas. Imprimir etiquetas de precio para todos los productos nuevos.'
                    },
                    {
                        'titulo': 'Verificar en dashboard',
                        'descripcion': 'Confirmar que los productos aparecen correctamente en el inventario y que el valor del catálogo se actualizó.'
                    },
                ],
                'es_template': True,
            },
            {
                'titulo': 'Análisis de Ventas y Reportes',
                'descripcion': 'Cómo generar y analizar reportes de ventas para tomar decisiones de negocio.',
                'pasos': [
                    {
                        'titulo': 'Consultar ventas del día',
                        'descripcion': 'Usar el asistente IA: "¿Cuántas ventas se realizaron hoy?" o ir al dashboard para ver estadísticas en tiempo real.'
                    },
                    {
                        'titulo': 'Analizar productos más vendidos',
                        'descripcion': 'Preguntar al asistente: "Muestra los productos más vendidos del mes" para identificar tendencias.'
                    },
                    {
                        'titulo': 'Revisar ingresos',
                        'descripcion': 'Consultar ingresos totales del mes y comparar con períodos anteriores para evaluar crecimiento.'
                    },
                    {
                        'titulo': 'Identificar productos con bajo stock',
                        'descripcion': 'Usar el asistente o el dashboard para ver productos que necesitan reposición urgente.'
                    },
                    {
                        'titulo': 'Tomar decisiones',
                        'descripcion': 'Basarse en los datos para decidir qué productos reponer, qué promociones hacer, o qué ajustar en precios.'
                    },
                ],
                'es_template': True,
            },
            {
                'titulo': 'Gestión de Precios y Actualizaciones',
                'descripcion': 'Proceso para actualizar precios de productos existentes en el inventario.',
                'pasos': [
                    {
                        'titulo': 'Identificar productos a actualizar',
                        'descripcion': 'Usar el asistente: "Muestra productos sin precio" o revisar el inventario manualmente.'
                    },
                    {
                        'titulo': 'Calcular nuevos precios',
                        'descripcion': 'Considerar costo, margen de ganancia deseado, competencia y política de precios de la empresa.'
                    },
                    {
                        'titulo': 'Actualizar en el sistema',
                        'descripcion': 'Ir a Inventario > Editar producto o usar la edición rápida directamente desde el dashboard. Actualizar precios minorista y/o mayorista.'
                    },
                    {
                        'titulo': 'Regenerar etiquetas',
                        'descripcion': 'Si los precios cambiaron, generar nuevas etiquetas para los productos afectados.'
                    },
                    {
                        'titulo': 'Verificar cambios',
                        'descripcion': 'Confirmar que los precios se actualizaron correctamente y que aparecen bien en el POS y dashboard.'
                    },
                ],
                'es_template': True,
            },
        ]

        self.stdout.write('\nCreando playbooks...')
        for data in playbooks_data:
            playbook, created = AssistantPlaybook.objects.get_or_create(
                titulo=data['titulo'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Creado: {playbook.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Ya existe: {playbook.titulo}'))

        # Artículos de conocimiento
        knowledge_data = [
            {
                'titulo': 'Política de Garantías',
                'resumen': 'Información sobre las garantías que ofrecemos y los plazos de cobertura.',
                'contenido': '''POLÍTICA DE GARANTÍAS - ImportStore

Todos nuestros productos cuentan con garantía de 6 meses contra defectos de fabricación.

Cobertura:
- Defectos de fabricación
- Fallas de componentes
- Problemas de funcionamiento

No cubre:
- Daños por mal uso
- Daños físicos por caídas o golpes
- Desgaste normal del producto
- Modificaciones no autorizadas

Proceso de garantía:
1. El cliente debe presentar el comprobante de compra
2. Se evalúa si el problema está cubierto
3. Se ofrece reparación, cambio o reembolso según corresponda
4. El proceso se completa en un plazo máximo de 15 días hábiles

Para más información, contactar con el área de atención al cliente.''',
                'tags': 'garantía, política, cliente, servicio',
                'destacado': True,
            },
            {
                'titulo': 'Cómo Buscar Productos en el Sistema',
                'resumen': 'Guía para buscar productos por SKU, nombre o categoría en el inventario.',
                'contenido': '''CÓMO BUSCAR PRODUCTOS EN EL SISTEMA

El sistema de inventario permite buscar productos de varias formas:

1. Por SKU:
   - Ingresar el código SKU completo en el buscador
   - Ejemplo: "IPHONE-16-128GB-TITANIO-NEGRO"

2. Por Nombre:
   - Escribir parte del nombre del producto
   - El sistema buscará coincidencias parciales
   - Ejemplo: "iPhone 16" mostrará todos los modelos iPhone 16

3. Por Categoría:
   - Filtrar por categoría desde el panel de inventario
   - Categorías disponibles: Celulares, Accesorios, etc.

4. Por Código de Barras:
   - Escanear el código de barras con el lector
   - El sistema identificará automáticamente el producto

Tips:
- Usar el asistente IA para búsquedas más complejas
- Los resultados muestran stock, precios y SKU
- Se puede exportar la lista de resultados a CSV''',
                'tags': 'búsqueda, inventario, SKU, producto',
                'destacado': False,
            },
            {
                'titulo': 'Proceso de Plan Canje',
                'resumen': 'Cómo calcular y procesar un canje de iPhone usado por uno nuevo.',
                'contenido': '''PROCESO DE PLAN CANJE

El Plan Canje permite que los clientes entreguen su iPhone usado a cambio de uno nuevo, recibiendo un descuento según el estado del equipo.

Pasos:

1. Evaluar el iPhone usado:
   - Verificar modelo, capacidad y color
   - Revisar estado físico (pantalla, marco, botones, cámara)
   - Consultar salud de batería
   - Verificar accesorios incluidos (caja original)

2. Calcular valor:
   - El sistema calcula automáticamente el valor base
   - Aplica descuentos según estado y batería
   - Muestra el valor final en USD y ARS

3. Seleccionar iPhone nuevo:
   - Elegir el modelo que el cliente desea adquirir
   - Verificar disponibilidad en stock

4. Calcular diferencia:
   - El sistema muestra la diferencia a pagar
   - Se puede ajustar manualmente si es necesario

5. Procesar canje:
   - Registrar el IMEI del iPhone usado
   - Completar la venta del iPhone nuevo
   - Actualizar inventario

Configuración:
- Los valores base y descuentos se configuran en /iphones/plan-canje/config/
- Se pueden ajustar según políticas de la empresa''',
                'tags': 'plan canje, iPhone, usado, descuento',
                'destacado': True,
            },
            {
                'titulo': 'Uso del Asistente IA (ISAC)',
                'resumen': 'Guía para aprovechar al máximo el asistente inteligente del sistema.',
                'contenido': '''USO DEL ASISTENTE IA (ISAC)

ISAC es tu asistente inteligente que te ayuda a gestionar el negocio de manera eficiente.

Funcionalidades principales:

1. Consultas de Inventario:
   - "¿Qué iPhone 16 tenemos en stock?"
   - "Muestra productos con bajo stock"
   - "¿Cuál es el precio del SKU X?"

2. Análisis de Ventas:
   - "Ventas del día de hoy"
   - "Productos más vendidos este mes"
   - "Total de ingresos del mes"

3. Respuestas Rápidas:
   - Usa las respuestas rápidas del panel lateral
   - Son consultas predefinidas para ahorrar tiempo

4. Playbooks:
   - Consulta procesos paso a paso
   - Guías para operaciones comunes

5. Centro de Conocimiento:
   - Accede a artículos con información importante
   - Políticas, procedimientos y guías

Tips:
- Sé específico en tus preguntas
- ISAC entiende contexto de conversaciones anteriores
- Usa lenguaje natural, no necesitas comandos especiales''',
                'tags': 'ISAC, asistente, IA, ayuda',
                'destacado': True,
            },
            {
                'titulo': 'Configuración de Precios',
                'resumen': 'Cómo establecer y actualizar precios minorista y mayorista.',
                'contenido': '''CONFIGURACIÓN DE PRECIOS

El sistema permite configurar precios en dos modalidades: Minorista y Mayorista.

Precios Minoristas:
- Precio de venta al público final
- Se muestra en la tienda y POS
- Puede tener descuentos promocionales

Precios Mayoristas:
- Precio para compras al por mayor
- Generalmente con descuento sobre minorista
- Requiere validación según políticas

Cómo actualizar precios:

1. Desde el Inventario:
   - Ir a la lista de productos
   - Hacer clic en el precio editable
   - Ingresar nuevo valor
   - Guardar cambios

2. Desde el Producto:
   - Editar el producto específico
   - Modificar precios en la sección correspondiente
   - Guardar cambios

3. Actualización masiva:
   - Usar la función de exportar/importar CSV
   - Modificar precios en el archivo
   - Importar de vuelta al sistema

Consideraciones:
- Los precios se pueden configurar en ARS o USD
- El sistema calcula conversiones automáticamente
- Los cambios se registran en el historial''',
                'tags': 'precios, minorista, mayorista, configuración',
                'destacado': False,
            },
        ]

        self.stdout.write('\nCreando artículos de conocimiento...')
        for data in knowledge_data:
            article, created = AssistantKnowledgeArticle.objects.get_or_create(
                titulo=data['titulo'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Creado: {article.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Ya existe: {article.titulo}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Datos de ejemplo creados exitosamente!'))

