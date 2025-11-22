-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 22-11-2025 a las 03:14:12
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `railway`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistente_ia_assistantknowledgearticle`
--

CREATE TABLE IF NOT EXISTS `asistente_ia_assistantknowledgearticle` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(140) NOT NULL,
  `resumen` longtext NOT NULL,
  `contenido` longtext NOT NULL,
  `tags` varchar(200) NOT NULL,
  `destacado` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `asistente_ia_assistantknowledgearticle`:
--

--
-- Volcado de datos para la tabla `asistente_ia_assistantknowledgearticle`
--

INSERT INTO `asistente_ia_assistantknowledgearticle` (`id`, `titulo`, `resumen`, `contenido`, `tags`, `destacado`, `actualizado`) VALUES
(2, 'Cómo Buscar Productos en el Sistema', 'Guía para buscar productos por SKU, nombre o categoría en el inventario.', 'CÓMO BUSCAR PRODUCTOS EN EL SISTEMA\n\nEl sistema de inventario permite buscar productos de varias formas:\n\n1. Por SKU:\n   - Ingresar el código SKU completo en el buscador\n   - Ejemplo: \"IPHONE-16-128GB-TITANIO-NEGRO\"\n\n2. Por Nombre:\n   - Escribir parte del nombre del producto\n   - El sistema buscará coincidencias parciales\n   - Ejemplo: \"iPhone 16\" mostrará todos los modelos iPhone 16\n\n3. Por Categoría:\n   - Filtrar por categoría desde el panel de inventario\n   - Categorías disponibles: Celulares, Accesorios, etc.\n\n4. Por Código de Barras:\n   - Escanear el código de barras con el lector\n   - El sistema identificará automáticamente el producto\n\nTips:\n- Usar el asistente IA para búsquedas más complejas\n- Los resultados muestran stock, precios y SKU\n- Se puede exportar la lista de resultados a CSV', 'búsqueda, inventario, SKU, producto', 0, '2025-11-14 20:48:04.422932'),
(3, 'Proceso de Plan Canje', 'Cómo calcular y procesar un canje de iPhone usado por uno nuevo.', 'PROCESO DE PLAN CANJE\n\nEl Plan Canje permite que los clientes entreguen su iPhone usado a cambio de uno nuevo, recibiendo un descuento según el estado del equipo.\n\nPasos:\n\n1. Evaluar el iPhone usado:\n   - Verificar modelo, capacidad y color\n   - Revisar estado físico (pantalla, marco, botones, cámara)\n   - Consultar salud de batería\n   - Verificar accesorios incluidos (caja original)\n\n2. Calcular valor:\n   - El sistema calcula automáticamente el valor base\n   - Aplica descuentos según estado y batería\n   - Muestra el valor final en USD y ARS\n\n3. Seleccionar iPhone nuevo:\n   - Elegir el modelo que el cliente desea adquirir\n   - Verificar disponibilidad en stock\n\n4. Calcular diferencia:\n   - El sistema muestra la diferencia a pagar\n   - Se puede ajustar manualmente si es necesario\n\n5. Procesar canje:\n   - Registrar el IMEI del iPhone usado\n   - Completar la venta del iPhone nuevo\n   - Actualizar inventario\n\nConfiguración:\n- Los valores base y descuentos se configuran en /iphones/plan-canje/config/\n- Se pueden ajustar según políticas de la empresa', 'plan canje, iPhone, usado, descuento', 1, '2025-11-14 20:48:04.426933'),
(4, 'Uso del Asistente IA (ISAC)', 'Guía para aprovechar al máximo el asistente inteligente del sistema.', 'USO DEL ASISTENTE IA (ISAC)\r\n\r\nISAC es tu asistente inteligente que te ayuda a gestionar el negocio de manera eficiente.\r\n\r\nFuncionalidades principales:\r\n\r\n1. Consultas de Inventario:\r\n   - \"¿Qué iPhone 16 tenemos en stock?\"\r\n   - \"Muestra productos con bajo stock\"\r\n   - \"¿Cuál es el precio del SKU X?\"\r\n\r\n2. Análisis de Ventas:\r\n   - \"Ventas del día de hoy\"\r\n   - \"Productos más vendidos este mes\"\r\n   - \"Total de ingresos del mes\"\r\n\r\n3. Respuestas Rápidas:\r\n   - Usa las respuestas rápidas del panel lateral\r\n   - Son consultas predefinidas para ahorrar tiempo\r\n\r\n4. Playbooks:\r\n   - Consulta procesos paso a paso\r\n   - Guías para operaciones comunes\r\n\r\n5. Centro de Conocimiento:\r\n   - Accede a artículos con información importante\r\n   - Políticas, procedimientos y guías\r\n\r\nTips:\r\n- Sé específico en tus preguntas\r\n- ISAC entiende contexto de conversaciones anteriores\r\n- Usa lenguaje natural, no necesitas comandos especiales', 'ISAC, asistente, IA, ayuda', 1, '2025-11-14 21:26:08.830089'),
(5, 'Configuración de Precios', 'Cómo establecer y actualizar precios minorista y mayorista.', 'CONFIGURACIÓN DE PRECIOS\n\nEl sistema permite configurar precios en dos modalidades: Minorista y Mayorista.\n\nPrecios Minoristas:\n- Precio de venta al público final\n- Se muestra en la tienda y POS\n- Puede tener descuentos promocionales\n\nPrecios Mayoristas:\n- Precio para compras al por mayor\n- Generalmente con descuento sobre minorista\n- Requiere validación según políticas\n\nCómo actualizar precios:\n\n1. Desde el Inventario:\n   - Ir a la lista de productos\n   - Hacer clic en el precio editable\n   - Ingresar nuevo valor\n   - Guardar cambios\n\n2. Desde el Producto:\n   - Editar el producto específico\n   - Modificar precios en la sección correspondiente\n   - Guardar cambios\n\n3. Actualización masiva:\n   - Usar la función de exportar/importar CSV\n   - Modificar precios en el archivo\n   - Importar de vuelta al sistema\n\nConsideraciones:\n- Los precios se pueden configurar en ARS o USD\n- El sistema calcula conversiones automáticamente\n- Los cambios se registran en el historial', 'precios, minorista, mayorista, configuración', 0, '2025-11-14 20:48:04.436942');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistente_ia_assistantplaybook`
--

CREATE TABLE IF NOT EXISTS `asistente_ia_assistantplaybook` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(120) NOT NULL,
  `descripcion` longtext NOT NULL,
  `pasos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`pasos`)),
  `es_template` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `asistente_ia_assistantplaybook`:
--

--
-- Volcado de datos para la tabla `asistente_ia_assistantplaybook`
--

INSERT INTO `asistente_ia_assistantplaybook` (`id`, `titulo`, `descripcion`, `pasos`, `es_template`, `actualizado`) VALUES
(4, 'Proceso de Venta en POS', 'Guía paso a paso para realizar una venta completa desde el POS.', '[{\"titulo\": \"Buscar productos\", \"descripcion\": \"Usar el buscador del POS para encontrar productos por nombre o SKU. Verificar stock disponible antes de agregar.\"}, {\"titulo\": \"Agregar al carrito\", \"descripcion\": \"Seleccionar variantes (color, capacidad, etc.) y cantidad. El sistema valida stock automáticamente.\"}, {\"titulo\": \"Aplicar descuentos\", \"descripcion\": \"Si corresponde, aplicar descuentos por cantidad, promociones o ajustes manuales. Verificar que el total sea correcto.\"}, {\"titulo\": \"Registrar pago\", \"descripcion\": \"Seleccionar método de pago (efectivo, tarjeta, transferencia, mixto). Ingresar monto recibido y calcular vuelto si aplica.\"}, {\"titulo\": \"Emitir comprobante\", \"descripcion\": \"Generar comprobante de venta. Verificar que todos los datos sean correctos antes de enviar al cliente.\"}, {\"titulo\": \"Verificar actualización\", \"descripcion\": \"Confirmar que el stock se actualizó correctamente y que la venta quedó registrada en el sistema.\"}]', 1, '2025-11-14 20:59:24.921080'),
(5, 'Carga de Nuevo Inventario', 'Proceso completo para recibir y cargar nueva mercadería al sistema.', '[{\"titulo\": \"Verificar factura del proveedor\", \"descripcion\": \"Revisar la factura recibida y comparar productos, cantidades y precios con lo recibido físicamente.\"}, {\"titulo\": \"Inspeccionar mercadería\", \"descripcion\": \"Verificar que todos los productos estén en buen estado, sin daños, y que coincidan con la factura.\"}, {\"titulo\": \"Crear/Actualizar productos\", \"descripcion\": \"Ir a Inventario > Añadir producto. Si el producto ya existe, actualizar stock. Si es nuevo, crear con todos los datos (nombre, categoría, atributos, SKU).\"}, {\"titulo\": \"Configurar precios\", \"descripcion\": \"Establecer precios minorista y mayorista en ARS según la política de la empresa. Verificar márgenes de ganancia.\"}, {\"titulo\": \"Registrar stock inicial\", \"descripcion\": \"Ingresar la cantidad recibida como stock actual. Configurar stock mínimo si corresponde.\"}, {\"titulo\": \"Generar etiquetas\", \"descripcion\": \"Ir a Inventario > Descargar etiquetas seleccionadas. Imprimir etiquetas de precio para todos los productos nuevos.\"}, {\"titulo\": \"Verificar en dashboard\", \"descripcion\": \"Confirmar que los productos aparecen correctamente en el inventario y que el valor del catálogo se actualizó.\"}]', 1, '2025-11-14 20:59:24.928105'),
(6, 'Análisis de Ventas y Reportes', 'Cómo generar y analizar reportes de ventas para tomar decisiones de negocio.', '[{\"titulo\": \"Consultar ventas del día\", \"descripcion\": \"Usar el asistente IA: \\\"¿Cuántas ventas se realizaron hoy?\\\" o ir al dashboard para ver estadísticas en tiempo real.\"}, {\"titulo\": \"Analizar productos más vendidos\", \"descripcion\": \"Preguntar al asistente: \\\"Muestra los productos más vendidos del mes\\\" para identificar tendencias.\"}, {\"titulo\": \"Revisar ingresos\", \"descripcion\": \"Consultar ingresos totales del mes y comparar con períodos anteriores para evaluar crecimiento.\"}, {\"titulo\": \"Identificar productos con bajo stock\", \"descripcion\": \"Usar el asistente o el dashboard para ver productos que necesitan reposición urgente.\"}, {\"titulo\": \"Tomar decisiones\", \"descripcion\": \"Basarse en los datos para decidir qué productos reponer, qué promociones hacer, o qué ajustar en precios.\"}]', 1, '2025-11-14 20:59:24.933286'),
(7, 'Gestión de Precios y Actualizaciones', 'Proceso para actualizar precios de productos existentes en el inventario.', '[{\"titulo\": \"Identificar productos a actualizar\", \"descripcion\": \"Usar el asistente: \\\"Muestra productos sin precio\\\" o revisar el inventario manualmente.\"}, {\"titulo\": \"Calcular nuevos precios\", \"descripcion\": \"Considerar costo, margen de ganancia deseado, competencia y política de precios de la empresa.\"}, {\"titulo\": \"Actualizar en el sistema\", \"descripcion\": \"Ir a Inventario > Editar producto o usar la edición rápida directamente desde el dashboard. Actualizar precios minorista y/o mayorista.\"}, {\"titulo\": \"Regenerar etiquetas\", \"descripcion\": \"Si los precios cambiaron, generar nuevas etiquetas para los productos afectados.\"}, {\"titulo\": \"Verificar cambios\", \"descripcion\": \"Confirmar que los precios se actualizaron correctamente y que aparecen bien en el POS y dashboard.\"}]', 1, '2025-11-14 20:59:24.939405');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistente_ia_assistantquickreply`
--

CREATE TABLE IF NOT EXISTS `asistente_ia_assistantquickreply` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(80) NOT NULL,
  `prompt` longtext NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `orden` int(10) UNSIGNED NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ;

--
-- RELACIONES PARA LA TABLA `asistente_ia_assistantquickreply`:
--

--
-- Volcado de datos para la tabla `asistente_ia_assistantquickreply`
--

INSERT INTO `asistente_ia_assistantquickreply` (`id`, `titulo`, `prompt`, `categoria`, `orden`, `activo`, `creado`, `actualizado`) VALUES
(1, 'Consultar stock de iPhone', '¿Qué modelos de iPhone tenemos en stock? Muestra stock, precios y SKU de cada uno.', 'inventario', 1, 1, '2025-11-14 20:48:04.362452', '2025-11-14 20:48:04.362452'),
(2, 'Productos con bajo stock', 'Muestra todos los productos que tienen stock por debajo del mínimo configurado.', 'inventario', 2, 1, '2025-11-14 20:48:04.367462', '2025-11-14 20:48:04.367462'),
(3, 'Ventas del día', '¿Cuántas ventas se realizaron hoy? Muestra el total y un resumen.', 'ventas', 1, 1, '2025-11-14 20:48:04.371861', '2025-11-14 20:48:04.371861'),
(4, 'Productos más vendidos', 'Muestra los 10 productos más vendidos en el último mes con sus cantidades.', 'ventas', 2, 1, '2025-11-14 20:48:04.376147', '2025-11-14 20:48:04.376147'),
(5, 'Precio de un producto', 'Necesito consultar el precio de un producto. ¿Cómo busco por SKU o nombre?', 'soporte', 1, 1, '2025-11-14 20:48:04.380229', '2025-11-14 20:48:04.380229'),
(6, 'Agregar nuevo producto', '¿Cuál es el proceso para agregar un nuevo producto al inventario?', 'soporte', 2, 1, '2025-11-14 20:48:04.386233', '2025-11-14 20:48:04.386233'),
(7, 'Reporte de ingresos', 'Genera un reporte de ingresos del mes actual con totales por día.', 'finanzas', 1, 1, '2025-11-14 20:48:04.390235', '2025-11-14 20:48:04.390235'),
(8, 'Productos sin precio', 'Muestra todos los productos que no tienen precio configurado.', 'inventario', 3, 1, '2025-11-14 20:48:04.395370', '2025-11-14 20:48:04.395370');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistente_ia_conversationmessage`
--

CREATE TABLE IF NOT EXISTS `asistente_ia_conversationmessage` (
  `id` bigint(20) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `contenido` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `thread_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `asistente_ia_conversationmessage`:
--   `thread_id`
--       `asistente_ia_conversationthread` -> `id`
--

--
-- Volcado de datos para la tabla `asistente_ia_conversationmessage`
--

INSERT INTO `asistente_ia_conversationmessage` (`id`, `rol`, `contenido`, `creado`, `thread_id`) VALUES
(1, 'user', 'hola', '2025-11-14 20:55:03.382059', 3),
(2, 'assistant', '¡Hola admin! ¿En qué te puedo ayudar hoy? Puedo consultarte stock, precios, generar reportes, o ayudarte con cualquier consulta del negocio.', '2025-11-14 20:55:07.706857', 3),
(3, 'user', 'que hora es', '2025-11-14 20:55:24.873315', 3),
(4, 'assistant', 'Admin, entiendo que querés saber la hora, pero como ISAC, mi función es asistirte con la gestión interna de ImportStore (stock, precios, ventas, reportes, etc.). No tengo acceso a la hora actual para brindártela. Podés consultarla en tu dispositivo o computadora.\n\n¿Hay algo más relacionado con el negocio en lo que pueda ayudarte en este momento?', '2025-11-14 20:55:36.333863', 3),
(5, 'user', 'reporte de ingresos', '2025-11-14 20:55:54.800073', 3),
(6, 'assistant', 'admin, entiendo que estás buscando un reporte de ingresos. Para poder generar uno o indicarte cómo acceder a él en el sistema, necesitaría que me especifiques un poco más qué tipo de reporte buscás.\n\nPor ejemplo, ¿necesitás un reporte de ingresos por un **período específico** (semanal, mensual, anual), por **línea de productos**, o de algún otro tipo de detalle?\n\nGeneralmente, podés encontrar la funcionalidad para generar estos reportes en la sección de **Finanzas** o **Reportes** de tu panel en el sistema de gestión de ImportStore. Si me das más detalles, con gusto te guío paso a paso.', '2025-11-14 20:56:10.049524', 3),
(7, 'user', 'aa', '2025-11-14 20:57:54.103956', 3),
(8, 'assistant', 'admin, con \"aa\" no me queda claro qué quisiste indicar. ¿Estás intentando especificar algo sobre el reporte de ingresos que me pediste, o tenés alguna otra consulta en la que pueda ayudarte en este momento?\n\nSi es por el reporte de ingresos, recordá que necesito saber el período (semanal, mensual, anual) o si es por línea de productos para poder orientarte mejor.', '2025-11-14 20:58:01.234729', 3),
(9, 'user', 'cuantos cargadores hay', '2025-11-14 20:58:43.174788', 4),
(10, 'assistant', 'admin, busqué en la base de datos pero no encontré resultados para \"cargadores\" con esa consulta. Parece que no hay stock registrado o no se encontraron coincidencias exactas.\n\n¿Querés que revise con otros criterios, como marcas o modelos específicos de cargadores, o te ayudo con alguna otra consulta?', '2025-11-14 20:58:52.876452', 4),
(11, 'user', '¿Cuántas ventas se realizaron hoy? Muestra el total y un resumen.', '2025-11-14 21:01:42.302895', 6),
(12, 'assistant', '¡Excelente!\n\nPara el día de hoy, se registraron un total de **3 ventas**.\n\nActualmente, solo tengo el conteo total. Si necesitás un resumen más detallado con información específica de cada venta (productos vendidos, montos, clientes, etc.), puedo generar un reporte de ventas completo.\n\n¿Te gustaría que prepare un reporte más exhaustivo o tenés alguna otra consulta sobre el análisis de ventas? Recordá que tenés el playbook de \"Análisis de Ventas y Reportes\" disponible para explorar más opciones.', '2025-11-14 21:02:06.099141', 6),
(13, 'user', 'si', '2025-11-14 21:02:18.924674', 6),
(14, 'assistant', '¡Entendido! Entonces, querés un reporte de ventas más exhaustivo.\n\nPara generarte el reporte que necesitás, ¿qué detalles te gustaría incluir? Por ejemplo, podemos mostrar:\n\n*   Productos específicos vendidos en cada transacción\n*   Montos de cada venta\n*   Clientes asociados\n*   Métodos de pago\n*   O un rango de fechas particular, si no es solo el día de hoy.\n\nRecordá que en el playbook de **Análisis de Ventas y Reportes** tenés distintas opciones para generar y personalizar estos informes.\n\n¿Querés que prepare un reporte estándar con los productos y montos de las 3 ventas de hoy, o tenés alguna preferencia?', '2025-11-14 21:02:26.104954', 6),
(15, 'user', 'que se vendio ayer', '2025-11-14 21:07:26.369384', 6),
(16, 'assistant', '¡Claro! Aquí te detallo las ventas registradas **ayer**:\n\nAyer se realizaron un total de **9 transacciones** (ventas) por un monto total de **$24.907.272,60 ARS**.\n\nEste es el detalle por cada venta:\n\n*   **Venta POS-BE12561B** - Total: **$10.000,00 ARS**\n    *   **Cargador 20w** x1 - $10.000,00 ARS\n\n*   **Venta POS-6251D818** - Total: **$10.000,00 ARS**\n    *   **Cargador 20w** x1 - $10.000,00 ARS\n\n*   **Venta POS-CB216F2A** - Total: **$10.000,00 ARS**\n    *   **Cargador 20w** x1 - $10.000,00 ARS\n\n*   **Venta POS-119A299D** - Total: **$10.000,00 ARS**\n    *   **Cargador 20w** x1 - $10.000,00 ARS\n\n*   **Venta POS-B627CAD1** - Total: **$12.121.212,00 ARS**\n    *   **iPhone 13 mini Sin especificar** x1 - $12.121.212,00 ARS\n\n*   **Venta POS-4B6258AE** - Total: **$10.000,00 ARS**\n    *   **Cargador 20w** x1 - $10.000,00 ARS\n\n*   **Venta POS-3BABAE79** - Total: **$12.121.212,00 ARS**\n    *   **iPhone 13 mini Sin especificar** x1 - $12.121.212,00 ARS\n\n*   **Venta POS-B0240418** - Total: **$8.800,00 ARS**\n    *   **Cargador 20w** x1 - $8.800,00 ARS\n\n*   **Venta POS-F5DB5517** - Total: **$616.048,60 ARS**\n    *   **Cargador 20w** x1 - $9.988,00 ARS\n    *   **iPhone 13 mini Sin especificar** x1 - $606.060,60 ARS\n\n¿Necesitás este reporte para alguna fecha específica o querés que desglosemos la información de alguna otra manera? Recordá que en el playbook de \"Análisis de Ventas y Reportes\" tenés más opciones para personalizar los informes.', '2025-11-14 21:07:48.894595', 6),
(17, 'user', 'cuantos cargadores hay', '2025-11-14 21:08:22.312191', 6),
(18, 'assistant', '¡Entendido! Acabo de consultar el inventario.\n\nEn este momento, tenemos un total de **11 unidades de cargadores** disponibles en stock.\n\nSi necesitás saber la cantidad de un tipo específico de cargador (por ejemplo, el \"Cargador 20w\" o algún otro modelo), avisame y busco ese detalle. También podés consultar el artículo \"Cómo Buscar Productos en el Sistema\" si querés explorar el stock por SKU o nombre de producto.', '2025-11-14 21:08:29.885699', 6),
(19, 'user', 'hola', '2025-11-14 21:22:47.706835', 6),
(20, 'assistant', '¡Hola! 👋\n\n¿En qué te puedo ayudar hoy? Puedo consultar stock, precios, generar reportes, o ayudarte con cualquier otra consulta del negocio.\n\nRecordá que siempre podés consultar los Playbooks o Artículos de conocimiento para procesos específicos.', '2025-11-14 21:22:50.415767', 6),
(21, 'user', 'que podes hacer', '2025-11-14 21:23:06.588345', 6),
(22, 'assistant', '¡Excelente pregunta! Estoy acá para asistirlos en la gestión diaria de ImportStore.\n\nEn resumen, puedo ayudarte con lo siguiente:\n\n*   **Consultas de inventario:** Chequear el stock actual de cualquier producto, como iPhones, cargadores, accesorios, etc.\n*   **Análisis de ventas:** Generar reportes de ventas por día, semana, mes, o un período específico, desglosando por producto, monto, etc. (como el reporte que te pasé hace un rato). Para esto, tenés disponible el playbook de \"Análisis de Ventas y Reportes\".\n*   **Gestión de productos y precios:** Ayudar con consultas sobre precios, actualizaciones, o procesos para cargar nuevo inventario. Podés consultar el playbook de \"Carga de Nuevo Inventario\" o \"Gestión de Precios y Actualizaciones\".\n*   **Soporte operativo:**\n    *   **Atención de reclamos:** Guiarte a través del \"Playbook de Atención de Reclamo\".\n    *   **Proceso de venta:** Orientarte con el \"Proceso de Venta Completa\".\n    *   **Políticas y procedimientos:** Resolver dudas sobre nuestra \"Política de Garantías\" o el \"Proceso de Plan Canje\", entre otros artículos de conocimiento.\n*   **Búsqueda de información:** En general, puedo buscar cualquier dato relevante que tengamos en el sistema para optimizar tu trabajo.\n\nSi tenés alguna consulta específica en mente o necesitás ayuda con algún proceso, no dudes en preguntarme. Estoy para hacer tu trabajo más fácil.', '2025-11-14 21:23:12.074137', 6),
(23, 'user', 'HO', '2025-11-14 21:24:37.507163', 7),
(24, 'assistant', 'Hola! ¿En qué te puedo ayudar hoy? Puedo consultarte stock, precios, generar reportes, o ayudarte con cualquier consulta del negocio.', '2025-11-14 21:24:42.604942', 7),
(25, 'user', 'cuantos iphone hay', '2025-11-14 21:27:33.863258', 6),
(26, 'assistant', '¡Hola! Acabo de revisar el inventario y, en este momento, **no tenemos iPhones disponibles en stock.** El sistema me indica 0 unidades.\n\n¿Hay algún modelo específico de iPhone que estabas buscando? A veces, si no hay stock global, puede haber una entrada pendiente o un movimiento que no se reflejó.\n\nTambién puedo ayudarte a buscar otros productos o con cualquier otra consulta que tengas.', '2025-11-14 21:27:45.517415', 6),
(27, 'user', 'Genera un reporte de ingresos del mes actual con totales por día.', '2025-11-14 21:28:24.933235', 8),
(28, 'assistant', '¡Hola! Acá te presento el reporte de ingresos del mes actual, con los totales por día, considerando solo las ventas completadas:\n\n---\n\n**Reporte de Ingresos - Noviembre 2025 (Ventas Completadas)**\n\n*   **14/11/2025:** $0.00 ARS (No hay ventas completadas registradas para este día)\n*   **13/11/2025:** $13,733,234.76 ARS\n*   **12/11/2025:** $32,326,285.40 ARS\n\n---\n\n**Total de Ingresos del Mes (hasta el 14/11/2025): $46,059,520.16 ARS**\n\nTené en cuenta que las ventas con estado \"Pendiente de pago\" o \"Cancelado\" no se incluyeron en este cálculo de ingresos.\n\nSi necesitás algún otro tipo de reporte o análisis de ventas, recordá que podés consultar el Playbook de **Análisis de Ventas y Reportes** en el panel lateral del sistema. ¡Decime si necesitás algo más!', '2025-11-14 21:28:58.330993', 8),
(29, 'user', '¿Cuál es el proceso para agregar un nuevo producto al inventario?', '2025-11-14 21:29:21.202414', 8),
(30, 'assistant', '¡Excelente pregunta! Para agregar un nuevo producto al inventario y asegurarte de seguir todos los pasos correctamente, te recomiendo consultar el Playbook de **Carga de Nuevo Inventario**.\n\nEn ese Playbook vas a encontrar la guía detallada con todo el proceso, los campos a completar y las consideraciones importantes para que el producto se cargue de forma exitosa en nuestro sistema. Lo podés encontrar en el panel lateral.\n\n¿Necesitás alguna otra ayuda o tenés otra consulta operativa?', '2025-11-14 21:29:25.565539', 8),
(31, 'user', 'Detalles del pedido\nProducto	Total\nPack Rollo Papel Termico X5 Color Blanco Para Mini Impresora Térmica × 3	$1,35\nAdaptador OTG 3 en 1 × 1	$0,50\nCuchillo De Cocina Con Mango De Plástico 3.5\'\' × 3	$1,50\nSet 5 Bowls De Acero Inoxidable Con Tapa Recipiente Metalico × 4	$22,00\nKit Mochila Antirrobo Urbana Para Notebook Morral Estuche 3 en 1 × 5	$35,00\nFrasco Decant para perfume Vidrio 5ml unidad × 40	$20,00\nFrasco Decant para perfume Vidrio 10ml unidad × 40	$24,00\nTV BOX Caja Verde 4k Ultra HD 512gb + 64gb ram × 2	$32,00\nGorra Bros Varios Colores × 4	$9,20\nAdaptador Cargado Auto a Tipo C Simil Iphone 13 Pro Max 20w-charger × 10	$17,00\nTripode Para Camaras Y Celulares Tf 3110 Extensible A 1,2m × 2	$7,00\nReloj Smart S30 Promax Series 10 7 en 1 Mallas × 1	$10,90\nAdaptador Usb 2.0 Wifi 802.11n Wireless 300mbps × 1	$1,30\nSmartwatch T-Wear Ultra 2 Super AMOLED Display × 1	$6,50\nSoporte Para Celular Plegable LB-0108/JS-67 Metalico 360 Lambo Tech × 10	$19,00\nMemoria 128gb Kingston Común × 1	$6,00\nToma 12v Para Moto Cargador Puerto Usb Con Encendedor AJ-S02 × 1	$4,50\nCABLE KLGO AUXILIAR 3.5 a 3.5 EN L COLORES 1MT × 10	$8,00\nCable Samsung Usb-a A Usb-c Carga Rapida 1 Metro × 10	$9,00\nCable Samsung 2A Tipo C Carga Rápida Bolsa Azul x 50 OFERTA × 2	$35,00\nCABLE USB T-C A T-C SAMSUNG CAJA × 20	$16,00\nRiñonera Wanlifu Mochila Cruzada De Pecho Bandolera Morral × 1	$3,60\nReloj Smartwatch S20 Ultra Con 4 Mallas Intercambiables × 1	$7,90\nEstantes de ángulo ranurado 100cm x 50cm x 198cm 4 Pisos × 1	$95,00\nAuricular Gamer Gm-06 PC PS4 Headphones × 3	$6,00\nSubtotal:	$398,25\nDescuento:	-$19,91\nEnvío:	Envío a transporte\nTotal:	$378,34', '2025-11-14 21:32:15.921281', 12),
(32, 'assistant', '¡Hola! Veo que me estás compartiendo los detalles de un pedido. Es una lista bastante completa de productos con sus cantidades, los precios individuales, el subtotal de $398,25, un descuento de -$19,91, y el total final de $378,34, con envío a transporte.\n\nPara poder ayudarte de la mejor manera, ¿qué acción específica te gustaría realizar con esta información? Por ejemplo, ¿necesitás que revise el stock de alguno de estos artículos, que genere un comprobante de venta, que consulte algo sobre el envío, o hay algún otro proceso que necesites gestionar sobre este pedido?', '2025-11-14 21:32:31.607360', 12),
(33, 'user', 'agregar al stock', '2025-11-14 21:33:33.083527', 12),
(34, 'assistant', 'Ah, entiendo. Con esta lista de productos que me compartiste, lo que necesitás es realizar la **recepción de mercadería** para que se sumen a nuestro inventario, ¿verdad?\n\nPara llevar a cabo este proceso y actualizar el stock con todos estos artículos, te sugiero que consultes el **Playbook de Recepción de Mercadería**. Ahí vas a encontrar los pasos detallados para registrar correctamente la entrada de estos productos en el sistema, asegurando que el inventario esté siempre al día.\n\nLo podés encontrar en el panel lateral de la plataforma, junto con los otros recursos disponibles. Si tenés alguna duda específica mientras lo hacés, avisame y te asisto.', '2025-11-14 21:33:40.732167', 12),
(35, 'user', 'agrega al stock', '2025-11-14 21:40:13.167202', 12),
(36, 'assistant', 'Entiendo tu consulta. Querías que yo, como ISAC, agregara directamente esos productos al stock, ¿verdad?\n\nComo asistente de IA, yo no tengo la capacidad de modificar el inventario de forma directa en el sistema. Mi función es guiarte y proporcionarte la información o los recursos para que vos, como empleado, puedas realizar estas operaciones de gestión.\n\nPara poder cargar todos estos productos al stock y que se reflejen en nuestro inventario, es fundamental que sigas el procedimiento de **Recepción de Mercadería**. Como te mencioné, el **Playbook de Recepción de Mercadería** es la herramienta que te indica el paso a paso detallado para registrar correctamente la entrada de esta mercadería en el sistema.\n\nSi necesitás ayuda para entender algún punto del Playbook o tenés alguna dificultad al momento de cargar los artículos, avisame y te asisto con eso, pero la acción de carga la tenés que realizar vos a través del sistema siguiendo esos pasos.', '2025-11-14 21:40:22.873578', 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistente_ia_conversationthread`
--

CREATE TABLE IF NOT EXISTS `asistente_ia_conversationthread` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `asistente_ia_conversationthread`:
--   `usuario_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `asistente_ia_conversationthread`
--

INSERT INTO `asistente_ia_conversationthread` (`id`, `titulo`, `creado`, `actualizado`, `activo`, `usuario_id`) VALUES
(1, 'Nueva conversación', '2025-11-14 20:51:22.467137', '2025-11-14 20:51:42.475171', 0, 2),
(2, '¿Qué modelos de iPhone tenemos en stock? Muestra s...', '2025-11-14 20:51:54.573370', '2025-11-14 20:57:45.120540', 0, 2),
(3, 'hola', '2025-11-14 20:54:58.768211', '2025-11-14 21:01:34.144420', 0, 2),
(4, 'cuantos cargadores hay', '2025-11-14 20:58:32.950284', '2025-11-14 21:22:44.269153', 0, 2),
(5, 'Nueva conversación', '2025-11-14 20:58:35.213982', '2025-11-14 21:01:38.059616', 0, 2),
(6, '¿Cuántas ventas se realizaron hoy? Muestra el tota...', '2025-11-14 21:01:42.284728', '2025-11-14 21:02:06.109431', 1, 2),
(7, 'HO', '2025-11-14 21:24:31.372322', '2025-11-14 21:24:42.608945', 1, 2),
(8, 'Genera un reporte de ingresos del mes actual con t...', '2025-11-14 21:28:24.925233', '2025-11-14 21:28:58.335993', 1, 2),
(9, 'Nueva conversación', '2025-11-14 21:31:52.414962', '2025-11-14 21:32:09.444278', 0, 2),
(10, 'Nueva conversación', '2025-11-14 21:31:58.567214', '2025-11-14 21:32:11.880561', 0, 2),
(11, 'Nueva conversación', '2025-11-14 21:31:59.776134', '2025-11-14 21:32:04.844584', 0, 2),
(12, 'Detalles del pedido\nProducto	Total\nPack Rollo Pape...', '2025-11-14 21:32:13.667463', '2025-11-14 21:32:31.612359', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `auth_group`:
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `auth_group_permissions`:
--   `permission_id`
--       `auth_permission` -> `id`
--   `group_id`
--       `auth_group` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `auth_permission`:
--   `content_type_id`
--       `django_content_type` -> `id`
--

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Cliente', 7, 'add_cliente'),
(26, 'Can change Cliente', 7, 'change_cliente'),
(27, 'Can delete Cliente', 7, 'delete_cliente'),
(28, 'Can view Cliente', 7, 'view_cliente'),
(29, 'Can add Conversación', 8, 'add_conversacion'),
(30, 'Can change Conversación', 8, 'change_conversacion'),
(31, 'Can delete Conversación', 8, 'delete_conversacion'),
(32, 'Can view Conversación', 8, 'view_conversacion'),
(33, 'Can add Mensaje', 9, 'add_mensaje'),
(34, 'Can change Mensaje', 9, 'change_mensaje'),
(35, 'Can delete Mensaje', 9, 'delete_mensaje'),
(36, 'Can view Mensaje', 9, 'view_mensaje'),
(37, 'Can add Categoría', 10, 'add_categoria'),
(38, 'Can change Categoría', 10, 'change_categoria'),
(39, 'Can delete Categoría', 10, 'delete_categoria'),
(40, 'Can view Categoría', 10, 'view_categoria'),
(41, 'Can add Producto', 11, 'add_producto'),
(42, 'Can change Producto', 11, 'change_producto'),
(43, 'Can delete Producto', 11, 'delete_producto'),
(44, 'Can view Producto', 11, 'view_producto'),
(45, 'Can add Proveedor', 12, 'add_proveedor'),
(46, 'Can change Proveedor', 12, 'change_proveedor'),
(47, 'Can delete Proveedor', 12, 'delete_proveedor'),
(48, 'Can view Proveedor', 12, 'view_proveedor'),
(49, 'Can add Variante de Producto', 13, 'add_productovariante'),
(50, 'Can change Variante de Producto', 13, 'change_productovariante'),
(51, 'Can delete Variante de Producto', 13, 'delete_productovariante'),
(52, 'Can view Variante de Producto', 13, 'view_productovariante'),
(53, 'Can add Detalle de iPhone', 14, 'add_detalleiphone'),
(54, 'Can change Detalle de iPhone', 14, 'change_detalleiphone'),
(55, 'Can delete Detalle de iPhone', 14, 'delete_detalleiphone'),
(56, 'Can view Detalle de iPhone', 14, 'view_detalleiphone'),
(57, 'Can add Precio', 15, 'add_precio'),
(58, 'Can change Precio', 15, 'change_precio'),
(59, 'Can delete Precio', 15, 'delete_precio'),
(60, 'Can view Precio', 15, 'view_precio'),
(61, 'Can add Registro de Historial', 16, 'add_registrohistorial'),
(62, 'Can change Registro de Historial', 16, 'change_registrohistorial'),
(63, 'Can delete Registro de Historial', 16, 'delete_registrohistorial'),
(64, 'Can view Registro de Historial', 16, 'view_registrohistorial'),
(65, 'Can add Etiqueta', 17, 'add_etiqueta'),
(66, 'Can change Etiqueta', 17, 'change_etiqueta'),
(67, 'Can delete Etiqueta', 17, 'delete_etiqueta'),
(68, 'Can view Etiqueta', 17, 'view_etiqueta'),
(69, 'Can add venta', 18, 'add_venta'),
(70, 'Can change venta', 18, 'change_venta'),
(71, 'Can delete venta', 18, 'delete_venta'),
(72, 'Can view venta', 18, 'view_venta'),
(73, 'Can add Línea de venta', 19, 'add_lineaventa'),
(74, 'Can change Línea de venta', 19, 'change_lineaventa'),
(75, 'Can delete Línea de venta', 19, 'delete_lineaventa'),
(76, 'Can view Línea de venta', 19, 'view_lineaventa'),
(77, 'Can add Artículo de conocimiento', 20, 'add_assistantknowledgearticle'),
(78, 'Can change Artículo de conocimiento', 20, 'change_assistantknowledgearticle'),
(79, 'Can delete Artículo de conocimiento', 20, 'delete_assistantknowledgearticle'),
(80, 'Can view Artículo de conocimiento', 20, 'view_assistantknowledgearticle'),
(81, 'Can add Playbook del asistente', 21, 'add_assistantplaybook'),
(82, 'Can change Playbook del asistente', 21, 'change_assistantplaybook'),
(83, 'Can delete Playbook del asistente', 21, 'delete_assistantplaybook'),
(84, 'Can view Playbook del asistente', 21, 'view_assistantplaybook'),
(85, 'Can add Respuesta rápida', 22, 'add_assistantquickreply'),
(86, 'Can change Respuesta rápida', 22, 'change_assistantquickreply'),
(87, 'Can delete Respuesta rápida', 22, 'delete_assistantquickreply'),
(88, 'Can view Respuesta rápida', 22, 'view_assistantquickreply'),
(89, 'Can add Configuración del sistema', 23, 'add_configuracionsistema'),
(90, 'Can change Configuración del sistema', 23, 'change_configuracionsistema'),
(91, 'Can delete Configuración del sistema', 23, 'delete_configuracionsistema'),
(92, 'Can view Configuración del sistema', 23, 'view_configuracionsistema'),
(93, 'Can add preferencia usuario', 24, 'add_preferenciausuario'),
(94, 'Can change preferencia usuario', 24, 'change_preferenciausuario'),
(95, 'Can delete preferencia usuario', 24, 'delete_preferenciausuario'),
(96, 'Can view preferencia usuario', 24, 'view_preferenciausuario'),
(97, 'Can add Configuración de tienda', 25, 'add_configuraciontienda'),
(98, 'Can change Configuración de tienda', 25, 'change_configuraciontienda'),
(99, 'Can delete Configuración de tienda', 25, 'delete_configuraciontienda'),
(100, 'Can view Configuración de tienda', 25, 'view_configuraciontienda'),
(101, 'Can add Detalle de venta', 26, 'add_detalleventa'),
(102, 'Can change Detalle de venta', 26, 'change_detalleventa'),
(103, 'Can delete Detalle de venta', 26, 'delete_detalleventa'),
(104, 'Can view Detalle de venta', 26, 'view_detalleventa'),
(105, 'Can add local', 27, 'add_local'),
(106, 'Can change local', 27, 'change_local'),
(107, 'Can delete local', 27, 'delete_local'),
(108, 'Can view local', 27, 'view_local'),
(109, 'Can add Caja Diaria', 28, 'add_cajadiaria'),
(110, 'Can change Caja Diaria', 28, 'change_cajadiaria'),
(111, 'Can delete Caja Diaria', 28, 'delete_cajadiaria'),
(112, 'Can view Caja Diaria', 28, 'view_cajadiaria'),
(113, 'Can add Movimiento de Caja', 29, 'add_movimientocaja'),
(114, 'Can change Movimiento de Caja', 29, 'change_movimientocaja'),
(115, 'Can delete Movimiento de Caja', 29, 'delete_movimientocaja'),
(116, 'Can view Movimiento de Caja', 29, 'view_movimientocaja'),
(117, 'Can add Solicitud de Impresión', 30, 'add_solicitudimpresion'),
(118, 'Can change Solicitud de Impresión', 30, 'change_solicitudimpresion'),
(119, 'Can delete Solicitud de Impresión', 30, 'delete_solicitudimpresion'),
(120, 'Can view Solicitud de Impresión', 30, 'view_solicitudimpresion'),
(121, 'Can add Carrito Remoto', 31, 'add_carritoremoto'),
(122, 'Can change Carrito Remoto', 31, 'change_carritoremoto'),
(123, 'Can delete Carrito Remoto', 31, 'delete_carritoremoto'),
(124, 'Can view Carrito Remoto', 31, 'view_carritoremoto'),
(125, 'Can add Imagen de producto', 32, 'add_productoimagen'),
(126, 'Can change Imagen de producto', 32, 'change_productoimagen'),
(127, 'Can delete Imagen de producto', 32, 'delete_productoimagen'),
(128, 'Can view Imagen de producto', 32, 'view_productoimagen'),
(129, 'Can add Configuración Plan Canje', 33, 'add_plancanjeconfig'),
(130, 'Can change Configuración Plan Canje', 33, 'change_plancanjeconfig'),
(131, 'Can delete Configuración Plan Canje', 33, 'delete_plancanjeconfig'),
(132, 'Can view Configuración Plan Canje', 33, 'view_plancanjeconfig'),
(133, 'Can add Transacción Plan Canje', 34, 'add_plancanjetransaccion'),
(134, 'Can change Transacción Plan Canje', 34, 'change_plancanjetransaccion'),
(135, 'Can delete Transacción Plan Canje', 34, 'delete_plancanjetransaccion'),
(136, 'Can view Transacción Plan Canje', 34, 'view_plancanjetransaccion'),
(137, 'Can add Mensaje', 35, 'add_conversationmessage'),
(138, 'Can change Mensaje', 35, 'change_conversationmessage'),
(139, 'Can delete Mensaje', 35, 'delete_conversationmessage'),
(140, 'Can view Mensaje', 35, 'view_conversationmessage'),
(141, 'Can add Conversación', 36, 'add_conversationthread'),
(142, 'Can change Conversación', 36, 'change_conversationthread'),
(143, 'Can delete Conversación', 36, 'delete_conversationthread'),
(144, 'Can view Conversación', 36, 'view_conversationthread'),
(145, 'Can add Cotización', 37, 'add_cotizacion'),
(146, 'Can change Cotización', 37, 'change_cotizacion'),
(147, 'Can delete Cotización', 37, 'delete_cotizacion'),
(148, 'Can view Cotización', 37, 'view_cotizacion'),
(149, 'Can add Contexto del Cliente', 38, 'add_clientecontexto'),
(150, 'Can change Contexto del Cliente', 38, 'change_clientecontexto'),
(151, 'Can delete Contexto del Cliente', 38, 'delete_clientecontexto'),
(152, 'Can view Contexto del Cliente', 38, 'view_clientecontexto'),
(153, 'Can add Dirección de Envío', 39, 'add_direccionenvio'),
(154, 'Can change Dirección de Envío', 39, 'change_direccionenvio'),
(155, 'Can delete Dirección de Envío', 39, 'delete_direccionenvio'),
(156, 'Can view Dirección de Envío', 39, 'view_direccionenvio'),
(157, 'Can add Perfil de Usuario', 40, 'add_perfilusuario'),
(158, 'Can change Perfil de Usuario', 40, 'change_perfilusuario'),
(159, 'Can delete Perfil de Usuario', 40, 'delete_perfilusuario'),
(160, 'Can view Perfil de Usuario', 40, 'view_perfilusuario'),
(161, 'Can add Favorito', 41, 'add_favorito'),
(162, 'Can change Favorito', 41, 'change_favorito'),
(163, 'Can delete Favorito', 41, 'delete_favorito'),
(164, 'Can view Favorito', 41, 'view_favorito'),
(165, 'Can add Historial de Estado de Venta', 42, 'add_historialestadoventa'),
(166, 'Can change Historial de Estado de Venta', 42, 'change_historialestadoventa'),
(167, 'Can delete Historial de Estado de Venta', 42, 'delete_historialestadoventa'),
(168, 'Can view Historial de Estado de Venta', 42, 'view_historialestadoventa'),
(169, 'Can add Solicitud Mayorista', 43, 'add_solicitudmayorista'),
(170, 'Can change Solicitud Mayorista', 43, 'change_solicitudmayorista'),
(171, 'Can delete Solicitud Mayorista', 43, 'delete_solicitudmayorista'),
(172, 'Can view Solicitud Mayorista', 43, 'view_solicitudmayorista'),
(173, 'Can add Cupón', 44, 'add_cupon'),
(174, 'Can change Cupón', 44, 'change_cupon'),
(175, 'Can delete Cupón', 44, 'delete_cupon'),
(176, 'Can view Cupón', 44, 'view_cupon'),
(177, 'Can add Escala de Precio Mayorista', 45, 'add_escalapreciomayorista'),
(178, 'Can change Escala de Precio Mayorista', 45, 'change_escalapreciomayorista'),
(179, 'Can delete Escala de Precio Mayorista', 45, 'delete_escalapreciomayorista'),
(180, 'Can view Escala de Precio Mayorista', 45, 'view_escalapreciomayorista'),
(181, 'Can add Notificación Interna', 46, 'add_notificacioninterna'),
(182, 'Can change Notificación Interna', 46, 'change_notificacioninterna'),
(183, 'Can delete Notificación Interna', 46, 'delete_notificacioninterna'),
(184, 'Can view Notificación Interna', 46, 'view_notificacioninterna');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `auth_user`:
--

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$Aug4S1VCCpAva4vjvJtxir$B+dNpahdN40gH9WmT7VbSO3KytHeJvuRVW9P1vsmB+A=', '2025-11-03 01:06:37.277911', 1, 'esrsosa', '', '', 'emanuelsosa4436@gmail.com', 1, 1, '2025-11-03 01:05:46.221246'),
(2, 'pbkdf2_sha256$1000000$LnCcyS3JAbLnu8OcMupBTT$bc0lw8TgvI3UJyviyceBwtOBaI/EQFIacG2yRqLE9es=', '2025-11-21 15:10:39.763787', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2025-11-11 20:06:13.956375'),
(7, 'pbkdf2_sha256$1000000$FID6vRdkvDjlRH2T5b722a$hqFTiedlHnALvSe/RDJWuYq9L+SOqKsTjlAmm+ei0pw=', NULL, 0, 'sosaemanuel4436@gmail.com', 'Emanuel', 'Sosa', 'sosaemanuel4436@gmail.com', 0, 1, '2025-11-21 15:08:43.122496');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `auth_user_groups`:
--   `group_id`
--       `auth_group` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `auth_user_user_permissions`:
--   `permission_id`
--       `auth_permission` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caja_cajadiaria`
--

CREATE TABLE IF NOT EXISTS `caja_cajadiaria` (
  `id` bigint(20) NOT NULL,
  `fecha_apertura` datetime(6) NOT NULL,
  `monto_inicial_ars` decimal(12,2) NOT NULL,
  `fecha_cierre` datetime(6) DEFAULT NULL,
  `monto_cierre_real_ars` decimal(12,2) DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  `local_id` bigint(20) NOT NULL,
  `usuario_apertura_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `caja_cajadiaria`:
--   `local_id`
--       `locales_local` -> `id`
--   `usuario_apertura_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `caja_cajadiaria`
--

INSERT INTO `caja_cajadiaria` (`id`, `fecha_apertura`, `monto_inicial_ars`, `fecha_cierre`, `monto_cierre_real_ars`, `estado`, `local_id`, `usuario_apertura_id`) VALUES
(1, '2025-11-12 18:19:31.447156', 122.00, '2025-11-12 19:26:03.948536', 1.00, 'CERRADA', 1, 2),
(2, '2025-11-13 16:35:00.127376', 0.00, '2025-11-13 16:35:09.385217', 1500.00, 'CERRADA', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caja_movimientocaja`
--

CREATE TABLE IF NOT EXISTS `caja_movimientocaja` (
  `id` bigint(20) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `monto_ars` decimal(12,2) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `caja_diaria_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `venta_asociada_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `caja_movimientocaja`:
--   `caja_diaria_id`
--       `caja_cajadiaria` -> `id`
--   `usuario_id`
--       `auth_user` -> `id`
--   `venta_asociada_id`
--       `ventas_venta` -> `id`
--

--
-- Volcado de datos para la tabla `caja_movimientocaja`
--

INSERT INTO `caja_movimientocaja` (`id`, `tipo`, `metodo_pago`, `monto_ars`, `descripcion`, `fecha`, `caja_diaria_id`, `usuario_id`, `venta_asociada_id`) VALUES
(1, 'APERTURA', 'EFECTIVO_ARS', 122.00, 'Apertura de caja - Monto inicial', '2025-11-12 18:19:31.448157', 1, 2, NULL),
(2, 'VENTA', 'EFECTIVO_ARS', 12085.48, 'Venta POS-4B6258AE', '2025-11-12 18:41:40.164738', 1, 2, 'POS-4B6258AE'),
(3, 'VENTA', 'EFECTIVO_ARS', 7333333.26, 'Venta POS-3BABAE79', '2025-11-12 19:21:00.164626', 1, 2, 'POS-3BABAE79'),
(4, 'APERTURA', 'EFECTIVO_ARS', 0.00, 'Apertura de caja - Monto inicial', '2025-11-13 16:35:00.131623', 2, 2, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion_configuracionsistema`
--

CREATE TABLE IF NOT EXISTS `configuracion_configuracionsistema` (
  `id` bigint(20) NOT NULL,
  `nombre_comercial` varchar(120) NOT NULL,
  `lema` varchar(180) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `color_principal` varchar(7) NOT NULL,
  `modo_oscuro_predeterminado` tinyint(1) NOT NULL,
  `mostrar_alertas` tinyint(1) NOT NULL,
  `whatsapp_numero` varchar(30) NOT NULL,
  `acceso_admin_habilitado` tinyint(1) NOT NULL,
  `contacto_email` varchar(254) NOT NULL,
  `domicilio_comercial` varchar(200) NOT NULL,
  `notas_sistema` longtext NOT NULL,
  `dolar_blue_manual` decimal(10,2) DEFAULT NULL,
  `costo_envio_local` decimal(10,2) DEFAULT NULL,
  `costo_envio_nacional` decimal(10,2) DEFAULT NULL,
  `descuento_efectivo_porcentaje` decimal(5,2) NOT NULL,
  `envios_disponibles` tinyint(1) NOT NULL,
  `envios_locales` varchar(200) NOT NULL,
  `envios_nacionales` tinyint(1) NOT NULL,
  `facebook` varchar(200) NOT NULL,
  `instagram_empresa` varchar(100) NOT NULL,
  `instagram_secundario` varchar(100) NOT NULL,
  `nombre_local` varchar(200) NOT NULL,
  `pago_efectivo_local` tinyint(1) NOT NULL,
  `pago_efectivo_retiro` tinyint(1) NOT NULL,
  `pago_online` tinyint(1) NOT NULL,
  `pago_online_link` varchar(200) NOT NULL,
  `pago_tarjeta` tinyint(1) NOT NULL,
  `pago_transferencia` tinyint(1) NOT NULL,
  `tiktok` varchar(100) NOT NULL,
  `transferencia_alias` varchar(50) NOT NULL,
  `transferencia_cbu` varchar(22) NOT NULL,
  `ubicacion_mapa` varchar(255) NOT NULL,
  `whatsapp_alternativo` varchar(40) NOT NULL,
  `cantidad_minima_mayorista` int(11) NOT NULL,
  `horarios_apertura` varchar(100) NOT NULL,
  `instagram_personal` varchar(100) NOT NULL,
  `monto_minimo_mayorista` decimal(12,2) NOT NULL,
  `precios_escala_activos` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `configuracion_configuracionsistema`:
--

--
-- Volcado de datos para la tabla `configuracion_configuracionsistema`
--

INSERT INTO `configuracion_configuracionsistema` (`id`, `nombre_comercial`, `lema`, `logo`, `color_principal`, `modo_oscuro_predeterminado`, `mostrar_alertas`, `whatsapp_numero`, `acceso_admin_habilitado`, `contacto_email`, `domicilio_comercial`, `notas_sistema`, `dolar_blue_manual`, `costo_envio_local`, `costo_envio_nacional`, `descuento_efectivo_porcentaje`, `envios_disponibles`, `envios_locales`, `envios_nacionales`, `facebook`, `instagram_empresa`, `instagram_secundario`, `nombre_local`, `pago_efectivo_local`, `pago_efectivo_retiro`, `pago_online`, `pago_online_link`, `pago_tarjeta`, `pago_transferencia`, `tiktok`, `transferencia_alias`, `transferencia_cbu`, `ubicacion_mapa`, `whatsapp_alternativo`, `cantidad_minima_mayorista`, `horarios_apertura`, `instagram_personal`, `monto_minimo_mayorista`, `precios_escala_activos`) VALUES
(1, 'ImportSt', 'Distribuidora de tecnología', 'branding/Belgrano_47_San_Luis..png', '#ffffff', 0, 1, '2665032890', 1, 'importstore.sanluis@gmail.com', 'Belgrano 47 local 1', '', NULL, NULL, NULL, 0.00, 1, '', 0, '', '', '', '', 1, 1, 0, '', 1, 1, '', '', '', '', '', 1, '', '', 3000.00, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion_configuraciontienda`
--

CREATE TABLE IF NOT EXISTS `configuracion_configuraciontienda` (
  `id` bigint(20) NOT NULL,
  `nombre_tienda` varchar(150) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `cuit` varchar(20) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `email_contacto` varchar(254) NOT NULL,
  `telefono_contacto` varchar(40) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `garantia_dias_general` int(10) UNSIGNED NOT NULL
) ;

--
-- RELACIONES PARA LA TABLA `configuracion_configuraciontienda`:
--

--
-- Volcado de datos para la tabla `configuracion_configuraciontienda`
--

INSERT INTO `configuracion_configuraciontienda` (`id`, `nombre_tienda`, `logo`, `cuit`, `direccion`, `email_contacto`, `telefono_contacto`, `actualizado`, `garantia_dias_general`) VALUES
(1, 'ImportStore', '', '20443604031', 'Belgrano 47, San Luis capital', 'importstore.sanluis@gmail.com', '+542665031180', '2025-11-12 22:04:19.861668', 50);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion_escalapreciomayorista`
--

CREATE TABLE IF NOT EXISTS `configuracion_escalapreciomayorista` (
  `id` bigint(20) NOT NULL,
  `cantidad_minima` int(11) NOT NULL,
  `cantidad_maxima` int(11) DEFAULT NULL,
  `porcentaje_descuento` decimal(5,2) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `orden` int(11) NOT NULL DEFAULT 0,
  `configuracion_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `configuracion_escalapreciomayorista`:
--   `configuracion_id`
--       `configuracion_configuracionsistema` -> `id`
--

--
-- Volcado de datos para la tabla `configuracion_escalapreciomayorista`
--

INSERT INTO `configuracion_escalapreciomayorista` (`id`, `cantidad_minima`, `cantidad_maxima`, `porcentaje_descuento`, `activo`, `orden`, `configuracion_id`) VALUES
(4, 5, 10, 5.00, 1, 0, 1),
(5, 10, 20, 10.00, 1, 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion_escalapreciomayorista_categorias`
--

CREATE TABLE IF NOT EXISTS `configuracion_escalapreciomayorista_categorias` (
  `id` bigint(20) NOT NULL,
  `escalapreciomayorista_id` bigint(20) NOT NULL,
  `categoria_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `configuracion_escalapreciomayorista_categorias`:
--   `categoria_id`
--       `inventario_categoria` -> `id`
--   `escalapreciomayorista_id`
--       `configuracion_escalapreciomayorista` -> `id`
--

--
-- Volcado de datos para la tabla `configuracion_escalapreciomayorista_categorias`
--

INSERT INTO `configuracion_escalapreciomayorista_categorias` (`id`, `escalapreciomayorista_id`, `categoria_id`) VALUES
(1, 4, 1),
(2, 5, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion_preferenciausuario`
--

CREATE TABLE IF NOT EXISTS `configuracion_preferenciausuario` (
  `id` bigint(20) NOT NULL,
  `usa_modo_oscuro` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `configuracion_preferenciausuario`:
--   `usuario_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `configuracion_preferenciausuario`
--

INSERT INTO `configuracion_preferenciausuario` (`id`, `usa_modo_oscuro`, `actualizado`, `usuario_id`) VALUES
(1, 0, '2025-11-21 20:31:51.701491', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_direccionenvio`
--

CREATE TABLE IF NOT EXISTS `core_direccionenvio` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` longtext NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `codigo_postal` varchar(20) DEFAULT NULL,
  `provincia` varchar(100) DEFAULT NULL,
  `pais` varchar(100) NOT NULL,
  `es_principal` tinyint(1) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `core_direccionenvio`:
--   `usuario_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_favorito`
--

CREATE TABLE IF NOT EXISTS `core_favorito` (
  `id` bigint(20) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `variante_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `core_favorito`:
--   `usuario_id`
--       `auth_user` -> `id`
--   `variante_id`
--       `inventario_productovariante` -> `id`
--

--
-- Volcado de datos para la tabla `core_favorito`
--

INSERT INTO `core_favorito` (`id`, `creado`, `usuario_id`, `variante_id`) VALUES
(1, '2025-11-21 15:34:05.555235', 7, 387),
(2, '2025-11-21 15:34:06.812218', 7, 219),
(3, '2025-11-21 15:34:08.122735', 7, 199),
(4, '2025-11-21 17:27:04.566191', 7, 438);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_notificacioninterna`
--

CREATE TABLE IF NOT EXISTS `core_notificacioninterna` (
  `id` bigint(20) NOT NULL,
  `tipo` varchar(30) NOT NULL,
  `prioridad` varchar(20) NOT NULL DEFAULT 'MEDIA',
  `titulo` varchar(200) NOT NULL,
  `mensaje` text NOT NULL,
  `url_relacionada` varchar(500) DEFAULT NULL,
  `leida` tinyint(1) NOT NULL DEFAULT 0,
  `creada` datetime(6) NOT NULL DEFAULT current_timestamp(6),
  `leida_por_id` int(11) DEFAULT NULL,
  `fecha_lectura` datetime(6) DEFAULT NULL,
  `datos_adicionales` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_adicionales`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `core_notificacioninterna`:
--   `leida_por_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `core_notificacioninterna`
--

INSERT INTO `core_notificacioninterna` (`id`, `tipo`, `prioridad`, `titulo`, `mensaje`, `url_relacionada`, `leida`, `creada`, `leida_por_id`, `fecha_lectura`, `datos_adicionales`) VALUES
(1, 'OTRO', 'MEDIA', 'Test', 'Test', NULL, 0, '2025-11-21 16:00:30.734740', NULL, NULL, '{}'),
(2, 'VENTA_WEB', 'ALTA', 'Nueva Venta Web: WEB-251121160421-137', 'Se recibió una nueva venta web de Emanuel Sosa por $6,240,009.00', '/ventas/listado/?q=WEB-251121160421-137', 0, '2025-11-21 16:04:21.647373', NULL, NULL, '{\"venta_id\": \"WEB-251121160421-137\", \"cliente_nombre\": \"Emanuel Sosa\", \"total\": 6240009.0}'),
(3, 'VENTA_WEB', 'ALTA', 'Nueva Venta Web: WEB-251121164708-985', 'Se recibió una nueva venta web de Emanuel Sosa por $351,250.00', '/ventas/listado/?q=WEB-251121164708-985', 0, '2025-11-21 16:47:08.709468', NULL, NULL, '{\"venta_id\": \"WEB-251121164708-985\", \"cliente_nombre\": \"Emanuel Sosa\", \"total\": 351250.0}'),
(4, 'VENTA_WEB', 'ALTA', 'Nueva Venta Web: WEB-251121164842-385', 'Se recibió una nueva venta web de Emanuel Sosa por $351,250.00', '/ventas/listado/?q=WEB-251121164842-385', 0, '2025-11-21 16:48:42.492262', NULL, NULL, '{\"venta_id\": \"WEB-251121164842-385\", \"cliente_nombre\": \"Emanuel Sosa\", \"total\": 351250.0}'),
(5, 'VENTA_WEB', 'ALTA', 'Nueva Venta Web: WEB-251121170232-788', 'Se recibió una nueva venta web de Emanuel Sosa por $351,250.00', '/ventas/listado/?q=WEB-251121170232-788', 0, '2025-11-21 17:02:32.273154', NULL, NULL, '{\"venta_id\": \"WEB-251121170232-788\", \"cliente_nombre\": \"Emanuel Sosa\", \"total\": 351250.0}'),
(6, 'VENTA_WEB', 'ALTA', 'Nueva Venta Web: WEB-251121170742-675', 'Se recibió una nueva venta web de Emanuel Sosa por $6,240,000.00', '/ventas/listado/?q=WEB-251121170742-675', 0, '2025-11-21 17:07:43.014431', NULL, NULL, '{\"venta_id\": \"WEB-251121170742-675\", \"cliente_nombre\": \"Emanuel Sosa\", \"total\": 6240000.0}'),
(7, 'VENTA_WEB', 'ALTA', 'Nueva Venta Web: WEB-251121200341-751', 'Se recibió una nueva venta web de Emanuel Sosa por $1,560,001.00', '/ventas/listado/?q=WEB-251121200341-751', 0, '2025-11-21 20:03:41.994538', NULL, NULL, '{\"venta_id\": \"WEB-251121200341-751\", \"cliente_nombre\": \"Emanuel Sosa\", \"total\": 1560001.0}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_perfilusuario`
--

CREATE TABLE IF NOT EXISTS `core_perfilusuario` (
  `id` bigint(20) NOT NULL,
  `tipo_usuario` varchar(20) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` longtext DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(20) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `documento` varchar(20) DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `core_perfilusuario`:
--   `usuario_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `core_perfilusuario`
--

INSERT INTO `core_perfilusuario` (`id`, `tipo_usuario`, `telefono`, `direccion`, `ciudad`, `codigo_postal`, `fecha_nacimiento`, `documento`, `creado`, `actualizado`, `usuario_id`) VALUES
(1, 'MINORISTA', '2665032890', NULL, NULL, NULL, NULL, '44360403', '2025-11-21 15:08:43.352994', '2025-11-21 15:08:43.353002', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_solicitudmayorista`
--

CREATE TABLE IF NOT EXISTS `core_solicitudmayorista` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `nombre_comercio` varchar(200) NOT NULL,
  `rubro` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `mensaje` longtext DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `fecha_revision` datetime(6) DEFAULT NULL,
  `notas` longtext DEFAULT NULL,
  `revisado_por_id` int(11) DEFAULT NULL,
  `cuit_cuil` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `core_solicitudmayorista`:
--   `revisado_por_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_cliente`
--

CREATE TABLE IF NOT EXISTS `crm_cliente` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `tipo_cliente` varchar(20) NOT NULL,
  `instagram_handle` varchar(100) DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL,
  `documento` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `crm_cliente`:
--

--
-- Volcado de datos para la tabla `crm_cliente`
--

INSERT INTO `crm_cliente` (`id`, `nombre`, `telefono`, `email`, `tipo_cliente`, `instagram_handle`, `fecha_creacion`, `ultima_actualizacion`, `documento`) VALUES
(1, 'Sosa Raul emanuel', '2665032890', NULL, 'Potencial', NULL, '2025-11-12 17:18:10.837266', '2025-11-12 17:18:10.837266', NULL),
(2, 's', 's', NULL, 'Minorista', NULL, '2025-11-13 04:02:07.468363', '2025-11-13 04:02:07.468363', NULL),
(3, 'caca', 'caca', NULL, 'Minorista', NULL, '2025-11-13 23:05:30.894709', '2025-11-13 23:05:30.894709', NULL),
(4, 'Facundo Bastias', 'Facundo Bastias', NULL, 'Minorista', NULL, '2025-11-14 16:37:09.311891', '2025-11-14 16:37:09.311891', NULL),
(5, 'Emanuel', '5492665032890', NULL, 'Potencial', NULL, '2025-11-15 00:33:10.512087', '2025-11-15 14:58:05.013602', NULL),
(6, 'Cliente 1181', '16315551181', NULL, 'Potencial', NULL, '2025-11-15 00:51:02.402397', '2025-11-15 00:51:02.403399', NULL),
(7, 'Emanuel Sosa', '', 'sosaemanuel4436@gmail.com', 'Potencial', NULL, '2025-11-21 15:38:37.598088', '2025-11-21 15:38:37.598117', '44360403');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_clientecontexto`
--

CREATE TABLE IF NOT EXISTS `crm_clientecontexto` (
  `id` bigint(20) NOT NULL,
  `productos_interes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`productos_interes`)),
  `categorias_preferidas` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`categorias_preferidas`)),
  `tipo_consulta_comun` varchar(50) NOT NULL,
  `ultima_interaccion` datetime(6) NOT NULL,
  `total_interacciones` int(11) NOT NULL,
  `promedio_respuesta_segundos` double DEFAULT NULL,
  `notas_internas` longtext NOT NULL,
  `tags_comportamiento` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`tags_comportamiento`)),
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`metadata`)),
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `cliente_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `crm_clientecontexto`:
--   `cliente_id`
--       `crm_cliente` -> `id`
--

--
-- Volcado de datos para la tabla `crm_clientecontexto`
--

INSERT INTO `crm_clientecontexto` (`id`, `productos_interes`, `categorias_preferidas`, `tipo_consulta_comun`, `ultima_interaccion`, `total_interacciones`, `promedio_respuesta_segundos`, `notas_internas`, `tags_comportamiento`, `metadata`, `creado`, `actualizado`, `cliente_id`) VALUES
(3, '[]', '[]', 'saludo', '2025-11-15 16:06:25.886904', 1, NULL, '', '[]', '{\"intenciones\": {\"saludo\": 1}}', '2025-11-15 16:06:25.882535', '2025-11-15 16:06:25.886904', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_conversacion`
--

CREATE TABLE IF NOT EXISTS `crm_conversacion` (
  `id` bigint(20) NOT NULL,
  `fuente` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `resumen` longtext NOT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL,
  `asesor_asignado_id` int(11) DEFAULT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `prioridad` varchar(10) NOT NULL,
  `sla_vencimiento` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `crm_conversacion`:
--   `asesor_asignado_id`
--       `auth_user` -> `id`
--   `cliente_id`
--       `crm_cliente` -> `id`
--

--
-- Volcado de datos para la tabla `crm_conversacion`
--

INSERT INTO `crm_conversacion` (`id`, `fuente`, `estado`, `resumen`, `fecha_inicio`, `ultima_actualizacion`, `asesor_asignado_id`, `cliente_id`, `prioridad`, `sla_vencimiento`) VALUES
(1, 'WhatsApp', 'Abierta', '', '2025-11-15 00:33:10.512087', '2025-11-15 15:58:54.077671', NULL, 5, 'medium', NULL),
(2, 'WhatsApp', 'Abierta', '', '2025-11-15 00:51:02.757658', '2025-11-15 00:51:02.757658', NULL, 6, 'medium', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_conversacion_etiquetas`
--

CREATE TABLE IF NOT EXISTS `crm_conversacion_etiquetas` (
  `id` bigint(20) NOT NULL,
  `conversacion_id` bigint(20) NOT NULL,
  `etiqueta_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `crm_conversacion_etiquetas`:
--   `conversacion_id`
--       `crm_conversacion` -> `id`
--   `etiqueta_id`
--       `crm_etiqueta` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_cotizacion`
--

CREATE TABLE IF NOT EXISTS `crm_cotizacion` (
  `id` bigint(20) NOT NULL,
  `productos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`productos`)),
  `total` decimal(12,2) NOT NULL,
  `valido_hasta` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `notas` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `cliente_id` bigint(20) NOT NULL,
  `conversacion_id` bigint(20) NOT NULL,
  `venta_relacionada_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `crm_cotizacion`:
--   `cliente_id`
--       `crm_cliente` -> `id`
--   `conversacion_id`
--       `crm_conversacion` -> `id`
--   `venta_relacionada_id`
--       `ventas_venta` -> `id`
--

--
-- Volcado de datos para la tabla `crm_cotizacion`
--

INSERT INTO `crm_cotizacion` (`id`, `productos`, `total`, `valido_hasta`, `estado`, `notas`, `creado`, `actualizado`, `cliente_id`, `conversacion_id`, `venta_relacionada_id`) VALUES
(1, '[{\"sku\": \"ADAPTADOR-5W-USB-IPHONE-CARGADORCABLE\", \"nombre\": \"Adaptador 5w USB IPhone Cargador+Cable\", \"precio\": 1.0, \"cantidad\": 1, \"subtotal\": 1.0}]', 1.00, '2025-11-22 13:41:04.759570', 'Pendiente', '', '2025-11-15 13:41:04.759570', '2025-11-15 13:41:04.759570', 5, 1, NULL),
(2, '[{\"sku\": \"ADAPTADOR-20W-TIPO-C-OOGAN\", \"nombre\": \"Adaptador 20W Tipo C Oogan\", \"precio\": 1560000.0, \"cantidad\": 1, \"subtotal\": 1560000.0}]', 1560000.00, '2025-11-22 14:39:14.741696', 'Pendiente', '', '2025-11-15 14:39:14.741696', '2025-11-15 14:39:14.741696', 5, 1, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_etiqueta`
--

CREATE TABLE IF NOT EXISTS `crm_etiqueta` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `color` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `crm_etiqueta`:
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crm_mensaje`
--

CREATE TABLE IF NOT EXISTS `crm_mensaje` (
  `id` bigint(20) NOT NULL,
  `emisor` varchar(10) NOT NULL,
  `contenido` longtext NOT NULL,
  `fecha_envio` datetime(6) NOT NULL,
  `enviado_por_ia` tinyint(1) NOT NULL,
  `conversacion_id` bigint(20) NOT NULL,
  `archivo` varchar(100) DEFAULT NULL,
  `tipo_mensaje` varchar(20) NOT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`metadata`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `crm_mensaje`:
--   `conversacion_id`
--       `crm_conversacion` -> `id`
--

--
-- Volcado de datos para la tabla `crm_mensaje`
--

INSERT INTO `crm_mensaje` (`id`, `emisor`, `contenido`, `fecha_envio`, `enviado_por_ia`, `conversacion_id`, `archivo`, `tipo_mensaje`, `metadata`) VALUES
(6, 'Cliente', 'this is a text message', '2025-11-15 00:51:02.874499', 0, 2, '', 'texto', NULL),
(130, 'Sistema', 'hola', '2025-11-15 14:22:28.371889', 0, 2, '', 'texto', NULL),
(189, 'Cliente', 'Hola', '2025-11-15 16:06:18.859594', 0, 1, '', 'texto', '{\"whatsapp_id\": \"wamid.HBgNNTQ5MjY2NTAzMjg5MBUCABIYFDNBNUZFNTkwN0ZGNTc4RkZCOUYyAA==\"}'),
(190, 'Sistema', '¡Hola Emanuel! ¿Cómo estás? Soy ISAC, tu asistente virtual de ImportSt.\n\n¡Un placer saludarte! ¿En qué te puedo ayudar hoy? 😉', '2025-11-15 16:06:26.899700', 1, 1, '', 'texto', '{\"contexto_usado\": {\"tiene_historial\": true, \"productos_interes\": false}, \"productos_info\": [], \"requiere_asesor\": false, \"intencion_detectada\": \"saludo\", \"productos_mencionados\": []}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ;

--
-- RELACIONES PARA LA TABLA `django_admin_log`:
--   `content_type_id`
--       `django_content_type` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-11-03 01:20:14.137223', '1', 'CARGADORES', 1, '[{\"added\": {}}]', 10, 1),
(2, '2025-11-03 01:21:35.112729', '1', 'VARIOS', 1, '[{\"added\": {}}]', 12, 1),
(3, '2025-11-11 20:09:10.904678', '1', 'None — MINORISTA 10000 ARS', 2, '[{\"changed\": {\"fields\": [\"Precio\"]}}]', 15, 2),
(4, '2025-11-11 20:11:44.398695', '2', 'iPhone 13 mini [None]', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2),
(5, '2025-11-11 20:12:01.335820', '2', 'None — MINORISTA 12121212 USD', 2, '[{\"changed\": {\"fields\": [\"Precio\"]}}]', 15, 2),
(6, '2025-11-12 16:58:15.306384', '2', 'CArgador', 2, '[{\"changed\": {\"name\": \"Variante de Producto\", \"object\": \"CArgador [SKU-000001]\", \"fields\": [\"Stock actual\"]}}]', 11, 2),
(7, '2025-11-12 18:31:08.111219', '1', 'CArgador [SKU-000001]', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2),
(8, '2025-11-12 18:31:08.115219', '2', 'iPhone 13 mini [SKU-000002]', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2),
(9, '2025-11-12 20:21:30.965771', '1', 'CArgador [SKU-000001]', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2),
(10, '2025-11-12 20:21:49.821696', '2', 'SKU-000002 — MINORISTA 350 USD', 2, '[{\"changed\": {\"fields\": [\"Precio\"]}}]', 15, 2),
(11, '2025-11-12 21:38:33.388452', '1', 'CArgador [SKU-000001]', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2),
(12, '2025-11-12 21:38:33.392453', '2', 'iPhone 13 mini [IPHONE-13-MINI-64GB-TITANIO-NATURAL] — 64GB / Titanio Natural', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2),
(13, '2025-11-12 21:57:02.086596', '3', 'iPhone 13 mini', 2, '[{\"changed\": {\"name\": \"Variante de Producto\", \"object\": \"iPhone 13 mini [IPHONE-13-MINI-64GB-TITANIO-NATURAL] \\u2014 64GB / Titanio Natural\", \"fields\": [\"Stock actual\"]}}]', 11, 2),
(14, '2025-11-12 21:57:09.264094', '1', 'Cargador 20w', 2, '[]', 11, 2),
(15, '2025-11-12 22:13:21.552177', '2', 'iPhone 13 mini [IPHONE-13-MINI-64GB-TITANIO-NATURAL] — 64GB / Titanio Natural', 2, '[{\"changed\": {\"fields\": [\"Stock actual\"]}}]', 13, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `django_content_type`:
--

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(20, 'asistente_ia', 'assistantknowledgearticle'),
(21, 'asistente_ia', 'assistantplaybook'),
(22, 'asistente_ia', 'assistantquickreply'),
(35, 'asistente_ia', 'conversationmessage'),
(36, 'asistente_ia', 'conversationthread'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(28, 'caja', 'cajadiaria'),
(29, 'caja', 'movimientocaja'),
(23, 'configuracion', 'configuracionsistema'),
(25, 'configuracion', 'configuraciontienda'),
(45, 'configuracion', 'escalapreciomayorista'),
(24, 'configuracion', 'preferenciausuario'),
(5, 'contenttypes', 'contenttype'),
(39, 'core', 'direccionenvio'),
(41, 'core', 'favorito'),
(46, 'core', 'notificacioninterna'),
(40, 'core', 'perfilusuario'),
(43, 'core', 'solicitudmayorista'),
(7, 'crm', 'cliente'),
(38, 'crm', 'clientecontexto'),
(8, 'crm', 'conversacion'),
(37, 'crm', 'cotizacion'),
(17, 'crm', 'etiqueta'),
(9, 'crm', 'mensaje'),
(16, 'historial', 'registrohistorial'),
(10, 'inventario', 'categoria'),
(14, 'inventario', 'detalleiphone'),
(33, 'inventario', 'plancanjeconfig'),
(34, 'inventario', 'plancanjetransaccion'),
(15, 'inventario', 'precio'),
(11, 'inventario', 'producto'),
(32, 'inventario', 'productoimagen'),
(13, 'inventario', 'productovariante'),
(12, 'inventario', 'proveedor'),
(27, 'locales', 'local'),
(6, 'sessions', 'session'),
(31, 'ventas', 'carritoremoto'),
(44, 'ventas', 'cupon'),
(26, 'ventas', 'detalleventa'),
(42, 'ventas', 'historialestadoventa'),
(19, 'ventas', 'lineaventa'),
(30, 'ventas', 'solicitudimpresion'),
(18, 'ventas', 'venta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `django_migrations`:
--

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-03 00:56:19.084429'),
(2, 'auth', '0001_initial', '2025-11-03 00:56:19.801554'),
(3, 'admin', '0001_initial', '2025-11-03 00:56:19.910881'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-03 00:56:19.922251'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-03 00:56:19.933946'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-03 00:56:19.999487'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-03 00:56:20.047793'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-03 00:56:20.061729'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-03 00:56:20.070397'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-03 00:56:20.122030'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-03 00:56:20.125292'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-03 00:56:20.138697'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-03 00:56:20.164944'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-03 00:56:20.178717'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-03 00:56:20.195549'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-03 00:56:20.205569'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-03 00:56:20.219872'),
(18, 'crm', '0001_initial', '2025-11-03 00:56:20.559669'),
(19, 'crm', '0002_alter_mensaje_emisor', '2025-11-03 00:56:20.568544'),
(20, 'crm', '0003_mensaje_archivo_mensaje_tipo_mensaje', '2025-11-03 00:56:20.597203'),
(21, 'historial', '0001_initial', '2025-11-03 00:56:20.668071'),
(22, 'inventario', '0001_initial', '2025-11-03 00:56:21.179171'),
(23, 'inventario', '0002_producto_imagen', '2025-11-03 00:56:21.191854'),
(27, 'sessions', '0001_initial', '2025-11-03 00:56:21.382981'),
(28, 'inventario', '0006_remove_producto_activo_remove_producto_codigo_barras_and_more', '2025-11-06 22:42:14.514069'),
(29, 'inventario', '0003_producto_activo', '2025-11-07 00:55:16.871087'),
(30, 'inventario', '0004_precio_moneda', '2025-11-07 01:02:00.695145'),
(31, 'inventario', '0005_remove_detalleiphone_fecha_compra_and_more', '2025-11-07 01:04:32.262483'),
(32, 'inventario', '0007_reconcile_state_only', '2025-11-07 21:53:11.002944'),
(33, 'asistente_ia', '0001_initial', '2025-11-08 16:45:58.104175'),
(34, 'crm', '0004_conversacion_enhancements', '2025-11-08 16:45:58.407536'),
(35, 'configuracion', '0001_initial', '2025-11-11 19:58:03.876085'),
(36, 'inventario', '0006_remove_detalleiphone_variante_and_more', '2025-11-11 19:58:04.163139'),
(37, 'inventario', '0008_detalleiphone_rebuild', '2025-11-11 19:58:04.310929'),
(38, 'inventario', '0009_detalleiphone_variante_bridge', '2025-11-11 19:58:04.540853'),
(39, 'inventario', '0010_sync_schema_new', '2025-11-11 19:58:04.886335'),
(40, 'ventas', '0001_initial', '2025-11-11 19:58:05.108096'),
(41, 'ventas', '0002_venta_extensiones', '2025-11-11 19:58:05.373184'),
(42, 'inventario', '0007_squash_fix_state_only', '2025-11-11 19:58:05.373184'),
(43, 'configuracion', '0002_configuraciontienda', '2025-11-12 15:48:31.722855'),
(44, 'ventas', '0003_remove_venta_descuento_general_and_more', '2025-11-12 15:48:40.219144'),
(45, 'locales', '0001_initial', '2025-11-12 16:18:49.343203'),
(47, 'inventario', '0011_rename_ultima_actualizacion_and_fix_sku', '2025-11-12 16:34:56.674638'),
(48, 'caja', '0001_initial', '2025-11-12 17:11:36.815757'),
(49, 'ventas', '0004_detalleventa_precio_unitario_usd_original_and_more', '2025-11-12 18:25:13.132866'),
(50, 'inventario', '0012_productovariante_codigo_barras_and_more', '2025-11-12 18:34:19.336053'),
(51, 'inventario', '0013_add_estado_field_to_producto', '2025-11-12 20:29:48.946276'),
(52, 'inventario', '0014_add_nombre_variante_field', '2025-11-12 20:40:04.035902'),
(53, 'ventas', '0005_make_variante_nullable', '2025-11-12 20:50:36.603011'),
(54, 'configuracion', '0003_configuraciontienda_garantia_dias_general', '2025-11-12 21:25:37.079696'),
(55, 'inventario', '0015_categoria_garantia_dias', '2025-11-12 21:25:43.163793'),
(56, 'ventas', '0006_venta_es_pago_mixto_venta_metodo_pago_2_and_more', '2025-11-12 23:39:54.501857'),
(57, 'ventas', '0007_alter_detalleventa_variante_carritoremoto', '2025-11-13 07:09:45.647591'),
(58, 'ventas', '0008_solicitudimpresion', '2025-11-13 07:09:45.869855'),
(59, 'ventas', '0009_venta_descuento_metodo_pago_ars', '2025-11-13 14:04:20.681549'),
(60, 'inventario', '0016_productoimagen', '2025-11-13 15:08:25.952422'),
(61, 'inventario', '0017_add_categoria_parent', '2025-11-13 17:35:07.708945'),
(62, 'inventario', '0018_plan_canje_models', '2025-11-14 16:54:45.570677'),
(63, 'inventario', '0019_add_plan_canje_new_fields', '2025-11-14 17:17:27.579056'),
(64, 'asistente_ia', '0002_conversationthread_conversationmessage', '2025-11-14 20:34:41.078806'),
(65, 'crm', '0005_clientecontexto', '2025-11-14 22:54:49.324933'),
(66, 'crm', '0006_cotizacion', '2025-11-14 22:54:49.583077'),
(67, 'configuracion', '0004_agregar_campos_crm_ia', '2025-11-15 14:25:50.574293'),
(68, 'core', '0001_initial', '2025-11-19 20:13:53.000000'),
(69, 'ventas', '0010_agregar_estados_y_origen', '2025-11-21 15:27:48.387319'),
(70, 'ventas', '0011_agregar_estados_pago_entrega', '2025-11-21 15:27:59.131766'),
(71, 'core', '0002_agregar_solicitud_mayorista', '2025-11-21 15:29:07.740474'),
(72, 'core', '0003_alter_perfilusuario_documento', '2025-11-21 15:29:31.324982'),
(73, 'ventas', '0012_alter_venta_metodo_pago_alter_venta_metodo_pago_2_and_more', '2025-11-21 15:29:45.256663'),
(74, 'core', '0004_agregar_cuit_cuil_solicitud', '2025-11-21 15:34:59.340805'),
(75, 'crm', '0007_agregar_documento_cliente', '2025-11-21 15:37:53.650707'),
(76, 'ventas', '0013_agregar_cupones', '2025-11-21 15:40:43.945322'),
(77, 'ventas', '0014_agregar_default_actualizado_cupon', '2025-11-21 15:44:20.655563'),
(78, 'ventas', '0015_agregar_default_actualizado_carrito', '2025-11-21 15:47:31.389400'),
(79, 'configuracion', '0005_agregar_precios_escala_mayorista', '2025-11-21 15:54:01.679802'),
(80, 'core', '0005_agregar_default_actualizado_todas_tablas', '2025-11-21 15:55:30.026974'),
(81, 'core', '0007_agregar_notificaciones_internas', '2025-11-21 15:59:14.941377'),
(82, 'configuracion', '0006_remove_configuracionsistema_correo_contacto_and_more', '2025-11-21 22:31:31.093245');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `django_session`:
--

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0g723v6avmnn7mo60kmrc6shqrpydpt9', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJRk0:-McLfyZm59oB5E_S5oUMaehU9WefhNlxQi7WrAuVk9Q', '2025-11-27 07:27:36.135705'),
('0t94cgbavdbqnagpsxowbt760gca9qs3', '.eJxVjDsOwjAQBe_iGllZxz9S0nMChKyN10vCJ5Ycp0LcnURKAe2befMWAZc6hGVOJYwkOqHE4XfrMT7StAG643TLMuaplrGXmyJ3OstzpvQ87e5fYMB5WN_GW-6t8wxGgSVQpiWwhhsC3yjQrHmNJU2uQWKkyC17YKWNs2iObo1GLGWsOZT0yjWL7nL9fAF5WT8g:1vJPhH:aUGHs25Odlj4G_7ytfm0prW2ChCd1EP9UW872fFiqNE', '2025-11-27 05:16:39.447376'),
('0xitxulmr1fw3skvj1ugcsa08533vu96', '.eJxVjcsOgjAURP-la0Jo6QPZ4c4FMVE3rprC7ZX6aAmFRGP8dyFhods5M2feRJtp7PQU7aAdkJIwkvxmjWlv1i8ArsZfQtoGPw6uSZdKutKY1gHsfbt2_wSdid28FoXERqoCqWBUAmUiByoFZkCLjFGOHGeZ5aAyA2igxRwLiowLJY3YqEUabYwueG2fvRtepMwS8ggQdD_Y1oX5pK7O-8PueKrI5wtS4EdJ:1vMZgR:zaACISA44xy6Bg7rbTGAnVkPlub8wl6D-rSrjGE4FB0', '2025-12-05 22:32:51.343600'),
('14p8zklmi8hcptj00vzo5jflyfpwdexa', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJRk8:-YKZvkrHxq8xvOMOUzbsFd2s09sLbv9pz8FuDeeUQwY', '2025-11-27 07:27:44.387442'),
('2iewxhy0h2pcf86udkiv9j14g4qjgd0g', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJwYv:K_IMiv6RjuWwZ6N77wi6hFDs_pJMfImqxdQ_sTFw95o', '2025-11-28 16:22:13.601519'),
('53fwpbzzq8cd4erer6vb8ufgcgnq94um', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vMI71:Nw91EAHCVww68Vi2Zqrc6zXJwFQRzvtSXBCWl0ylqtE', '2025-12-05 03:47:07.127392'),
('5lryevowz1wjg7yy2u5isjjyqexwhppj', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJgLW:7ILSkYu7KIE4HeTo7hREN10zlHtKWuJ0_lFQBGAwlDQ', '2025-11-27 23:03:18.430166'),
('6a2nxz8gwj04dc27fgiu8pfsz0ufe3sw', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJx6n:2NdhNSMnpoKA8ap2fqJXgzJSPmIQb8ybOc80zlbimas', '2025-11-28 16:57:13.787648'),
('6opg11dpyj3jf5rmvaxoigq20chcv8j2', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vMSdk:8rB-JkyypQOhx1NVyCceuJpL2a8LlrpFcmtMeASahvw', '2025-12-05 15:01:36.846870'),
('70z6f8gggb58vnd2v689x39m3odiys6w', '.eJxVjcsOgjAURP-la0Jo6QPZ6Y4Fmqj7pnB7pT5aQiHRGP9dSFjods7MmTfRZho7PUU7aAekJIwkv1lj2pv1C4Cr8ZeQtsGPg2vSpZKuNKZ1AHvfrd0_QWdiN69FIbGRqkAqGJVAmciBSoEZ0CJjlCPHWWY5qMwAGmgxx4Ii40JJIzZqkUYbowte22fvhhcps4Q8AgTdD7Z1YT6pq_3hWJ3OW_L5AlLNR0Y:1vJwXw:YEHoEG60BtEDpEbl-T4IloOK4UY63GTbIXikZe8Stds', '2025-11-28 16:21:12.613905'),
('8kmsg3gdglo4u8kwhx9037n70fpsg7cn', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vK4Ym:C7dmWNO6QDtO_mFoxNFt-OKy1AvmxxHpTpOKO1KrMMA', '2025-11-29 00:54:36.928253'),
('8wqugj5agb9y5sy0gj7jk0s2io8is6pt', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZLk:fM3ivcDgx48Bc0WJTKAvHM6QgxtpTWC41O33ia_dTe8', '2025-11-27 15:35:04.744420'),
('979n20vlc3xf1n9wcjyybfkabgo8f81c', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJcD1:K-mnl51Gbjka-mZlSIZit2HLYAQb1e5Q1OqYHg-hGC8', '2025-11-27 18:38:15.620926'),
('aucedjbk59jktb21ux43qxlirnxej9fo', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJS0x:Xlyy9PYIro4uqMLfZPS1vCnh0vRvK7xPtjbjq9tVtgc', '2025-11-27 07:45:07.432670'),
('axfmt132087b8z8oh3gf943czt1n88c5', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJY3u:HG_xF0yH5NXICfa0BGk8GiDF4sTP0Vu3JWe8XClV-tQ', '2025-11-27 14:12:34.475382'),
('cab9s6dhf0ipes9bzw5n5trnu1t1snur', '.eJxVjMsOgjAQRf-la9O0pS9YuvcbmoHpSNW0hEKiMf67kLDQ7T3nnjcLsC5jWGucQ0LWMcVOv1sPwz3mHeAN8rXwoeRlTj3fFX7Qyi8F4-N8uH-BEeq4vY231FvnSRolLUplGpTWkEDphZKaNG2xqNEJQAIcqCEvSWnjLJjW7dEaa00lh_ic0vxinTKtEkJ8vvc5QEQ:1vK0cV:gbJYIIhjffYURZIhuo1-Zuef9JM2lyEU53jkGDmFpDw', '2025-12-14 20:42:11.957192'),
('cdkrgx38xp1w3fq8npqcijcm1fht51ig', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vIurZ:S0Cc11OUsFmWeFc9tPJhZxf4PUGVy7e-0CKcLD0ClY0', '2025-11-25 20:21:13.921514'),
('cispeeq6ei2zzn9ab0h8m76pk0i56xoi', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJcot:H-Qt7yPmGKh7eAfLc6C0db1ETGFjPPf7dLCpRWRlr5s', '2025-11-27 19:17:23.522586'),
('cushkle9c9lo4v95s6m6owbwhmq4c8n2', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vLqta:leN6NKx-Bj7dFKHb6wINssJO37HEcneugsInlLLapwM', '2025-12-03 22:43:26.570815'),
('dm7dx4zdh2kcj0eeydrxjanw5sj8jgnz', '.eJxVjrtuwzAMRX8l0GwYluNXs7WdO3UsCoHWI2Zii4Ykdwny72UcI0053se5vAgFSxrUEm1QaMRBlCJ71nrQZ-tvhjmBP1KuyaeAfX6L5Jsb8w8ydnzbsv8AA8SB23XXuL5pOyfrUjZGlvXeyKZ2hZFdUcrKVY5htjJtAcaB0W7vOunKqm4bqF9ahmoIAROpYCdKJA5fF_EDAcEnu74uMxHPC29x8AiGAnc8TX2wrL2_PjRjow44ayT_ZOw-0e9snK1Gh0xYB31CA4wuMzEHdkgtHhOPkoIQebLgy4s_NxpFAY_oYRQHv4xjJmxUOA_k-QsHY7SropeYaHoo9zoDL2JCz4SY4L4gtolCXK_f1180TZE-:1vJQR7:vxO6nisHIWCFvWmSuefHWUOCtzOWRtMflus6h7cR510', '2025-11-27 06:04:01.812474'),
('e5rob8jh27puw0nf1ccbyztu6ys1ysvz', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZtQ:jHfYrBva2nzUcnY-N7pnlNmpi4jKlr9n3XdUGF1QW00', '2025-11-27 16:09:52.581416'),
('eauhvksq324c3hvsg23jn2w0572p76ow', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJxSQ:M9JABjtttUaGse_y1KMvOB3nxuaMM7eOUdY_0JMcUXA', '2025-11-28 17:19:34.309418'),
('eb9hqtxujmieyopwj0e4x4hl36qrms0c', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZ99:36fEGzIg3a1V0j7woQ8fiwZeW3zmlFeCAlEXc55KHQU', '2025-11-27 15:22:03.818907'),
('fuicmdeqn043tfov8p3av3364asr9ydy', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJPQc:cJm9I2DSTYbi2HZAUxskdQFr5CqYzzvmpnK7e-Sr740', '2025-11-27 04:59:26.469841'),
('i7jn3aoer07rbtn1amkrotzcl1xex5ot', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJhHo:mNLRWf7RbH6q8TDOhuY8HPOm8aDjUnlHnilCco9cqRU', '2025-11-28 00:03:32.113997'),
('iyjfnmaj00qao2zk2j9y41j4mi2phcwy', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJY3t:Uk-irswfBzQbJr03629X7nM8-om6y1dt3PFJj4VmJs8', '2025-11-27 14:12:33.208342'),
('jcfgg787423e2am28clxd7vxmj8k469t', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJdI7:rKhR_r-BH4pKSu6lqLbP8MBVp4eq03IkSvNPffq-zVw', '2025-11-27 19:47:35.427878'),
('lfioiqrtkocaz735iuajv2k3j1ai80wo', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJZ0q:eWXTGSRc010jXkoV5E4L0aauF6NGGoK3g4YhinG-R1o', '2025-11-27 15:13:28.836164'),
('lje3nnnfuxg90p8memo5opxs9mun8fze', '.eJxVjcsOgjAURP-la0Jo6QPZ4c4FMVE3rprC7ZX6aAmFRGP8dyFhods5M2feRJtp7PQU7aAdkJIwkvxmjWlv1i8ArsZfQtoGPw6uSZdKutKY1gHsfbt2_wSdid28FoXERqoCqWBUAmUiByoFZkCLjFGOHGeZ5aAyA2igxRwLiowLJY3YqEUabYwueG2fvRtepMwS8ggQdD_Y1oX5pK7O-8PueKrI5wtS4EdJ:1vMGRe:5AS8JP5PY-neNs9a2EksZnXhESTUFIRCLwHv2CFhg-Q', '2025-12-05 02:00:18.654693'),
('lodg84vdk4077oh2udceky68h8a7z7w1', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJacp:62xwQzSgcyQxghQw3Zr0KeMJiqLAvtYXL0eypQtJJtU', '2025-11-27 16:56:47.561253'),
('mhirscrf8ylm4v8o1qabjy5yykp8uvog', '.eJxVjrtuwzAMRX8l0GwYluNXs7WdO3UsCoHWI2Zii4Ykdwny72UcI0053se5vAgFSxrUEm1QaMRBlCJ71nrQZ-tvhjmBP1KuyaeAfX6L5Jsb8w8ydnzbsv8AA8SB23XXuL5pOyfrUjZGlvXeyKZ2hZFdUcrKVY5htjJtAcaB0W7vOunKqm4bqF9ahmoIAROpYCdKJA5fF_EDAcEnu74uMxHPC29x8AiGAnc8TX2wrL2_PjRjow44ayT_ZOw-0e9snK1Gh0xYB31CA4yu2kzMgS1Si8fEq6QgRN4s-PLiz41GUcAjehjFwS_jmAkbFc4DeX7DwRjtquglJpoeyr3OwIuY0DMhJrgviG2iENfr9_UXtQWRdw:1vJPWH:T76niIhumzDp7hi6NHzCXkT37N7TVL_yf00_5AuTAI0', '2025-11-27 05:05:17.460091'),
('msa2ueqt76z5z271ggymv3ql7b8s0q51', '.eJxVjEEOwiAQRe_C2pDCgIBL9z0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kbgIJU6_W8L84LYDumO7zTLPbV2mJHdFHrTLcSZ-Xg_376Bir9_a55wVKxcCWHUenCFtTOFExnhndQAoAwAob5HAabaOCoA1CJY9BC3eH7yaNpA:1vFj1p:4rA4LdnEsEzjiX3swuXSXLPV6J6aGdCpLvGVo6o29Yo', '2025-11-17 01:06:37.279905'),
('mtrc6d2a4zzmk3fuq4bzsqq7trgb75kb', '.eJy9VMtuGzkQ_JXOnDaGIGtkPWxfgmRtYBeLPOBkD4tVIPSQPRLtGbbChxAlyL9vkyPJFqxNjBxy0ohsFqurqvm1mGMMy3n05OZGF5fFsOg9XKtQ3ZFNG_oW7YL7im1wpuqnkv521_dfs6bm1bb2AGCJfimnx-eTuppMz-tyPCwnuhyOz3Q5GdcDXZ4PhuWoHtUCRiM9HaCuUav6rD4v6-FoPJ3g-GIqoC1rnq8cKcMC-PrlP29v_nz_4aXsoPfGB7RhvpRfdpvi8t-vheOGpDCxkJrEm2yQhbfN2mgEaiCvfQ4MG_lsyX6ZxcGASogWwUZaI3jyJi3WZ7ZffOvtQfc3HiCnSiyv019tNPfgusVncIUte1ixg9pYbMwX1JxuD9QiCAQ5I3s7Crn4OIGZndlr6W8DTWoTVugEYBM1ukCpGWgYPkUCS0qOBfJ9SGer-trKem7uAlaR5P7uTLqnRcuw5M0LeJd3BMfHJuR9uUXdgSZYOdZRBfY96ByQjwVZcugAm0VmiBYcSZtyjndMcrH00HENEYLDCm-5I4bllWy39OyhtI_8SjjrpGhSRog-1Yd35GoSzp0NSbwbWhu_lUEMcLSQw45Tg4IrFqypo72MFWdxTk7k5oAnJ7tilOQkK2cF6tbYWQEIDXooJ5dnUwFqoBydluXpcDAcZ8N-T7YgGFuza1HtzARUIWIDon1LgCKPeJYM9AISsGlEM_IrUpmuro3KO83eiU4S8es3y23lqAfv__q7B0q0kHRrsaAz6nnqjjwCr8QtdRCmLhxvurR02fe5_yr69BPvHdXZgyCdtrvCjmcKczY3KZjVc53CHjxWlOMhcbepKBgVG0mMZyGcSWXMXfJM9i8lSinS6WiueSSdN0kzI-2re9JbW-1hM2ko9oS7MB6d56OhY6vxqWH7g8XkPO4f5JmCyqSOObXS3d57OLOPxvTejKdN6g0pdnr7WuU5Oz66R6Z1a6gXrw6eDiVp_BSNqM6S8j1UzpylBQvK9xVDf4u3_sd6vWF5-RIvVnFFPk_n_wgQ6F6Dn1TglzxeH7_9B9dkhVM:1vK0ZT:vz_-P6iqvY7-lLFTH__r0v9j5nvGPkuAciM3ymIKoTE', '2025-11-28 20:39:03.075682'),
('n14xf74ufx4zyfqgi8a40i2d51ad2stf', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJeN4:b6mBaIzmj96bwm-z0MTsfZz3RYR0ltWzIl_e76sVCeI', '2025-11-27 20:56:46.702226'),
('nb01o5oilyl8vw8stncrmzbuy1arcupw', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJYzV:ft5AtRNVxfLCyolYQ-GxgL_TG_X4f-HSFaa4SYaK0gs', '2025-11-27 15:12:05.379683'),
('ng8imfjbdx9wp1s58cb3bgeo1a4truta', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJbRB:dqab4L9vwPF5UZyKYAcxLfcMAq-ePFwqGK4NZtHlQ1Q', '2025-11-27 17:48:49.127033'),
('p7ezngmyjeq4lmiwqq2v6m2zek99jys6', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vMSXm:-ulMzuziwXdjUKX5RN6VnfK9NcHd73yyYi7k3zr9-YU', '2025-12-05 14:55:26.653109'),
('px26c45tdy9au338butruirhjn9yvivw', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJS0p:jr6Ly2d694GmAWSaMCxx5bPpbK7fwj7Dyn8ILJcNGtM', '2025-11-27 07:44:59.039390'),
('q3ixqctaadr3vjylutzsyt54s1537h7v', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vIudI:_OLMxaz1wtiFqVFgGG-CaUWRwK0W1gKAU2My_S_49ME', '2025-11-25 20:06:28.196085'),
('tw9flkkzxiu40od5nlfm4mbu7gmp4d87', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJPdD:z5qqP36MWRxD9J2I2IXYvUZ-pzC3L02HQ-tqtaG3bzU', '2025-11-27 05:12:27.840176'),
('tyiuvm69kmy4bczlzs2ld23urzmhszvw', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJXt7:Y2nj3nw-9mmkP3mS3xQsoPVDqX1KAXzI1xwGkQlUOfI', '2025-11-27 14:01:25.750910'),
('ub0c0jtm0cj5zfv1whlsw1eo5lydx17c', '.eJxVjDsOwjAQBe_iGllexz8o6TmDtfZ6cQA5UpxUiLuTSCmgfTNv3iLiutS49jLHkcRFaHH63RLmZ2k7oAe2-yTz1JZ5THJX5EG7vE1UXtfD_QtU7HV72-A4OR8YrAZHoO1A4CwrgqA0GDa8xYohr5AYKfPAAVgb6x3asxefL9MvN9U:1vJRj3:mdnzDz67e-oFfJT4p0AT6NoQ5Mtas9j5LiksMVzjAVE', '2025-11-27 07:26:37.048013'),
('vhlkts06efuo2dcsty34d029x8na0hpk', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJeK8:rMaCs_16MXsWCAUSsU6KWx8LjVvLGYWJ2qowHE1q98s', '2025-11-27 20:53:44.316295'),
('vsp75dfjro7odzfllrsgddtw6ffxg0lt', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vMGUj:e3D20QJ6wjCm8JaX2Sc140mOixY91E7JkI8yM2Mw4JQ', '2025-12-05 02:03:29.328960'),
('wl5jbtjmfca22jig8a3vsxhs09i1grs6', '.eJxVjMsOwiAQRf-FtSFAedmle7-BTDuMRQ0YaBON8d9tky50e8-5580CLPMUlhZrSMh6ptjhdxtgvMW8AbxCvhQ-ljzXNPBN4Ttt_Fww3k-7-xeYoE3r23hLg3WepFHSolSmQ2kNCZReKKlJ0xqLGp0AJMCROvKSlDbOgjm6Ldpia6nkEJ-PVF-sF58veik_Eg:1vJgZt:z0hT4CNXsqfKSs_VP3NRAVfY7bDLlGbDYSdFRgjYT08', '2025-11-27 23:18:09.224910'),
('y4da69m4vkpya3xe0w4a54waivpuzc7o', '.eJxVjcsOgjAURP-la0Jo6QPZ4c4FMVE3rprC7ZX6aAmFRGP8dyFhods5M2feRJtp7PQU7aAdkJIwkvxmjWlv1i8ArsZfQtoGPw6uSZdKutKY1gHsfbt2_wSdid28FoXERqoCqWBUAmUiByoFZkCLjFGOHGeZ5aAyA2igxRwLiowLJY3YqEUabYwueG2fvRtepMwS8ggQdD_Y1oX5pK7O-8PueKrI5wtS4EdJ:1vJbXg:bGHjgT0aKObNYX58fbKlr4TKwDvlxkKK_PgIfFINWZ8', '2025-11-27 17:55:32.635894');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_registrohistorial`
--

CREATE TABLE IF NOT EXISTS `historial_registrohistorial` (
  `id` bigint(20) NOT NULL,
  `tipo_accion` varchar(20) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `historial_registrohistorial`:
--   `usuario_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `historial_registrohistorial`
--

INSERT INTO `historial_registrohistorial` (`id`, `tipo_accion`, `descripcion`, `fecha`, `usuario_id`) VALUES
(1, 'CREACION', 'Se agregó el nuevo iPhone: iPhone 13 mini - 1TB / Azul.', '2025-11-06 22:14:53.368133', 1),
(2, 'VENTA', 'Venta POS-0686AF2B por 9000.00 (efectivo).', '2025-11-11 20:09:48.099498', NULL),
(3, 'VENTA', 'Venta POS-7C627328 por 12906666.54 (efectivo).', '2025-11-11 20:13:01.224965', 2),
(4, 'VENTA', 'Venta POS-6A89ADAE por 10000.00 (efectivo).', '2025-11-11 20:22:27.192347', 2),
(5, 'VENTA', 'Venta POS-88CA0C8B por 12121212.00 (efectivo).', '2025-11-11 20:44:58.359410', 2),
(6, 'VENTA', 'Venta POS-CF4E18B1 por 10000.00 (efectivo).', '2025-11-12 15:22:13.782224', 2),
(7, 'VENTA', 'Venta POS-BE12561B por $10000.00 (EFECTIVO_ARS).', '2025-11-12 16:58:29.682890', 2),
(9, 'ESTADO', 'Estado inactivo → iPhone 13 mini', '2025-11-12 17:16:12.065615', 2),
(10, 'ESTADO', 'Estado activo → iPhone 13 mini', '2025-11-12 17:16:17.210622', 2),
(11, 'VENTA', 'Venta POS-6251D818 por $12085.48 (EFECTIVO_ARS).', '2025-11-12 17:58:54.803385', 2),
(12, 'VENTA', 'Venta POS-CB216F2A por $10648.00 (EFECTIVO_ARS).', '2025-11-12 18:04:34.609291', 2),
(13, 'VENTA', 'Venta POS-119A299D por $12085.48 (EFECTIVO_USD).', '2025-11-12 18:07:21.151394', 2),
(15, 'VENTA', 'Venta POS-B627CAD1 por $12121212.00 (EFECTIVO_ARS).', '2025-11-12 18:14:47.970821', 2),
(16, 'VENTA', 'Venta POS-4B6258AE por $12085.48 (EFECTIVO_ARS).', '2025-11-12 18:41:40.047282', 2),
(17, 'VENTA', 'Venta POS-3BABAE79 por $7333333.26 (EFECTIVO_ARS).', '2025-11-12 19:21:00.029567', 2),
(18, 'VENTA', 'Venta POS-B0240418 por $10648.00 (EFECTIVO_ARS).', '2025-11-12 20:00:17.935555', 2),
(19, 'VENTA', 'Venta POS-F5DB5517 por $616048.60 (EFECTIVO_ARS).', '2025-11-12 20:10:17.632548', 2),
(20, 'VENTA', 'Venta POS-5D3E5CE4 por $381.15 (TARJETA).', '2025-11-12 20:25:57.543526', 2),
(21, 'ESTADO', 'Estado inactivo → iPhone 13 mini', '2025-11-12 20:32:45.683187', 2),
(22, 'ESTADO', 'Estado activo → iPhone 13 mini', '2025-11-12 20:32:48.144542', 2),
(23, 'VENTA', 'Venta POS-553AE394 por $10648.00 (EFECTIVO_ARS).', '2025-11-12 20:34:26.182190', 2),
(24, 'VENTA', 'Venta POS-298C6FD3 por $10621.38 (TRANSFERENCIA).', '2025-11-12 20:41:38.961576', 2),
(25, 'VENTA', 'Venta POS-5BEC9024 por $1488.00 (EFECTIVO_ARS).', '2025-11-12 20:52:37.059502', 2),
(26, 'VENTA', 'Venta POS-796712CB por $1999.00 (EFECTIVO_ARS).', '2025-11-12 20:53:08.470798', 2),
(28, 'MODIFICACION', 'Actualización iPhone iPhone 13 mini (64GB / Titanio Natural)', '2025-11-12 21:28:43.520548', 2),
(29, 'VENTA', 'Venta POS-90825F5D por $10000.00 (EFECTIVO_ARS).', '2025-11-12 21:36:40.290284', 2),
(30, 'VENTA', 'Venta POS-65B108DF por $11949.19 (EFECTIVO_ARS).', '2025-11-12 21:38:39.256947', 2),
(31, 'VENTA', 'Venta POS-DF47FA7E por $1729130.00 (EFECTIVO_ARS).', '2025-11-12 21:53:35.433867', 2),
(32, 'VENTA', 'Venta POS-C21BAE7C por $2092247.30 (EFECTIVO_ARS).', '2025-11-12 21:58:46.699782', 2),
(33, 'VENTA', 'Venta POS-A4518974 por $20000.00 (EFECTIVO_ARS).', '2025-11-12 22:01:07.478957', 2),
(34, 'VENTA', 'Venta POS-39941E37 por $1729130.00 (TRANSFERENCIA).', '2025-11-12 22:07:47.683654', 2),
(35, 'VENTA', 'Venta POS-9EB7FA22 por $1729130.00 (EFECTIVO_ARS).', '2025-11-12 22:13:24.942162', 2),
(36, 'VENTA', 'Venta POS-00EA9703 por $50000.00 (EFECTIVO_ARS).', '2025-11-12 22:17:54.190908', 2),
(37, 'VENTA', 'Venta POS-B80FE78F por $14666666.52 (EFECTIVO_ARS).', '2025-11-12 22:21:27.664003', 2),
(38, 'VENTA', 'Venta POS-FE370894 por $1288.00 (EFECTIVO_ARS).', '2025-11-12 23:06:06.558582', 2),
(39, 'VENTA', 'Venta POS-92C3F826 por $21212.00 (EFECTIVO_ARS).', '2025-11-12 23:09:49.890483', 2),
(40, 'VENTA', 'Venta POS-ECB1CCF8 por $13552.00 (EFECTIVO_ARS).', '2025-11-12 23:15:39.300115', 2),
(41, 'VENTA', 'Venta POS-130AD6CE por $121.00 (EFECTIVO_ARS).', '2025-11-12 23:23:04.337819', 2),
(42, 'VENTA', 'Venta POS-D990084C por $10000.00 (TRANSFERENCIA).', '2025-11-12 23:41:57.760327', 2),
(43, 'VENTA', 'Venta POS-ABFC278E por $1729130.00 (EFECTIVO_ARS).', '2025-11-12 23:43:15.684592', 2),
(44, 'VENTA', 'Venta POS-F74FFB14 por $1212.00 (EFECTIVO_ARS).', '2025-11-12 23:44:59.189877', 2),
(45, 'VENTA', 'Venta POS-248DDA43 por $10000.00 (EFECTIVO_ARS).', '2025-11-12 23:47:12.400974', 2),
(46, 'VENTA', 'Venta POS-3650B009 por $10000.00 (EFECTIVO_ARS).', '2025-11-12 23:54:24.252033', 2),
(47, 'VENTA', 'Venta POS-0E5CFD36 por $12222.00 (EFECTIVO_ARS).', '2025-11-13 00:00:21.109901', 2),
(48, 'CREACION', 'Alta iPhone iPhone 16 (128GB / Titanio Negro)', '2025-11-13 03:44:06.003076', 2),
(49, 'VENTA', 'Venta POS-1E7960FF por $2092247.30 (EFECTIVO_ARS).', '2025-11-13 03:44:33.898798', 2),
(50, 'MODIFICACION', 'Actualización iPhone iPhone 16 (128GB / Titanio Negro)', '2025-11-13 03:45:37.842376', 2),
(51, 'ELIMINACION', 'Baja iPhone iPhone 13 mini (64GB / Titanio Natural)', '2025-11-13 03:47:46.646351', 2),
(52, 'VENTA', 'Venta POS-040397B8 por $10513.33 (EFECTIVO_ARS).', '2025-11-13 04:02:07.501802', 2),
(53, 'VENTA', 'Venta POS-8D0BAA4A por $11.00 (EFECTIVO_ARS).', '2025-11-13 04:02:47.967546', 2),
(54, 'ESTADO', 'Estado de venta POS-D990084C cambiado de Completado a Pendiente de pago', '2025-11-13 04:38:54.319609', 2),
(55, 'VENTA', 'Venta POS-41E8B8C7 por $6685.25 (EFECTIVO_ARS).', '2025-11-13 05:27:20.995995', 2),
(56, 'ELIMINACION', 'Venta POS-41E8B8C7 anulada. Stock devuelto. ', '2025-11-13 05:28:25.231134', 2),
(57, 'VENTA', 'Venta POS-A074FD78 por $60197.50 (EFECTIVO_ARS).', '2025-11-13 05:33:48.488027', 2),
(58, 'VENTA', 'Venta POS-A518A580 por $9990.00 (EFECTIVO_ARS).', '2025-11-13 06:18:20.890565', 2),
(59, 'VENTA', 'Venta POS-5773F459 por $8075.00 (EFECTIVO_ARS).', '2025-11-13 06:50:19.676838', 2),
(60, 'ELIMINACION', 'Venta POS-5773F459 anulada. Stock devuelto. ', '2025-11-13 07:01:33.558014', 2),
(61, 'VENTA', 'Venta POS-049D4502 por $1477835.50 (EFECTIVO_ARS).', '2025-11-13 07:17:04.326943', 2),
(62, 'VENTA', 'Venta POS-20F0E7F3 por $9500.00 (EFECTIVO_ARS).', '2025-11-13 07:23:37.283467', 2),
(63, 'VENTA', 'Venta POS-D4BF06D2 por $5759.60 (EFECTIVO_ARS).', '2025-11-13 07:42:42.522376', 2),
(64, 'VENTA', 'Venta POS-CDE476D4 por $9770.75 (EFECTIVO_ARS).', '2025-11-13 14:15:02.732651', 2),
(65, 'CREACION', 'Alta iPhone iPhone 15 Pro (64GB / Titanio Natural)', '2025-11-13 15:28:11.070914', 2),
(66, 'ESTADO', 'Estado inactivo → iPhone 13 mini', '2025-11-13 15:30:11.219692', 2),
(67, 'MODIFICACION', 'Actualización iPhone iPhone 16 (128GB / Titanio Negro)', '2025-11-13 16:21:56.588624', 2),
(68, 'VENTA', 'Venta POS-31A9A44D por $41465.45 (EFECTIVO_ARS).', '2025-11-13 18:23:20.243818', 2),
(69, 'VENTA', 'Venta POS-6B100E8F por $1799181.74 (EFECTIVO_ARS).', '2025-11-13 18:27:06.727856', 2),
(70, 'VENTA', 'Venta POS-B00486BF por $17916.59 (EFECTIVO_ARS).', '2025-11-13 18:39:43.758812', 2),
(71, 'VENTA', 'Venta POS-CA846B38 por $1804125.00 (EFECTIVO_ARS).', '2025-11-13 18:50:39.151152', 2),
(72, 'MODIFICACION', 'Actualización iPhone iPhone 15 Pro (64GB / Titanio Natural)', '2025-11-13 18:59:41.118995', 2),
(73, 'VENTA', 'Venta POS-762454C2 por $4990.00 (EFECTIVO_ARS).', '2025-11-13 19:44:22.136123', 2),
(74, 'VENTA', 'Venta POS-98BB15AC por $284956.45 (EFECTIVO_ARS).', '2025-11-13 19:52:34.429805', 2),
(75, 'ELIMINACION', 'Venta POS-98BB15AC anulada. Stock devuelto. ', '2025-11-13 20:11:27.175787', 2),
(76, 'VENTA', 'Venta POS-D485FC80 por $2122500.00 (EFECTIVO_ARS).', '2025-11-13 22:51:38.734006', 2),
(77, 'VENTA', 'Venta POS-90E0619E por $8.00 (EFECTIVO_ARS).', '2025-11-13 23:05:30.926493', 2),
(78, 'VENTA', 'Venta POS-611E669B por $1.00 (EFECTIVO_ARS).', '2025-11-13 23:12:47.315360', 2),
(79, 'VENTA', 'Venta POS-56C4E11D por $2122501.00 (EFECTIVO_ARS).', '2025-11-13 23:13:09.162028', 2),
(80, 'ELIMINACION', 'Baja iPhone iPhone 13 mini (64GB / Titanio Natural)', '2025-11-13 23:36:08.369365', 2),
(81, 'VENTA', 'Venta POS-1AF59883 por $2122500.00 (EFECTIVO_ARS).', '2025-11-13 23:46:13.182002', 2),
(82, 'CREACION', 'Alta iPhone iPhone 11 (64GB / Morado)', '2025-11-14 00:07:07.862305', 2),
(83, 'VENTA', 'Venta POS-3EEECD18 por $201860.00 (EFECTIVO_ARS).', '2025-11-14 16:37:09.327194', 2),
(84, 'ESTADO', 'Estado inactivo → Adaptador 5w USB IPhone Cargador+Cable ()', '2025-11-14 17:49:35.534559', 2),
(85, 'ESTADO', 'Estado activo → Adaptador 5w USB IPhone Cargador+Cable ()', '2025-11-14 17:49:40.302269', 2),
(86, 'MODIFICACION', 'Stock actualizado: Adaptador Apple 20w Tipo C (ORIGINAL APPLE) (ADAPTADOR-APPLE-20W-TIPO-C-ORIGINAL-APPLE) - 0 → 2', '2025-11-14 17:54:17.418081', 2),
(87, 'MODIFICACION', 'Stock actualizado: Adaptador Apple 20w Tipo C (ORIGINAL APPLE) (ADAPTADOR-APPLE-20W-TIPO-C-ORIGINAL-APPLE) - 0 → 2', '2025-11-14 17:54:17.427883', 2),
(88, 'ESTADO', 'Estado inactivo → Adaptador 20W Tipo C Oogan ()', '2025-11-14 17:54:47.735980', 2),
(89, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - MINORISTA ARS - 1.00 → 1560000', '2025-11-14 17:58:11.451711', 2),
(90, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - MINORISTA ARS - 1560000.00 → 1560000', '2025-11-14 17:58:11.466784', 2),
(91, 'MODIFICACION', 'Precio creado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - MAYORISTA ARS - 1212.00 → 1212', '2025-11-14 18:48:54.529884', 2),
(92, 'ESTADO', 'Estado activo → Adaptador 20W Tipo C Oogan ()', '2025-11-14 18:49:12.518192', 2),
(93, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - 0 → 2', '2025-11-15 00:35:46.613252', 2),
(94, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - 0 → 2', '2025-11-15 00:35:46.621291', 2),
(95, 'VENTA', 'Venta POS-6B0D8096 por $2559150.00 (EFECTIVO_ARS).', '2025-11-15 00:57:54.268622', 2),
(96, 'ESTADO', 'Estado de venta WEB-20251121150919 cambiado de Pendiente de pago a Pendiente de armado', '2025-11-21 15:30:32.635338', 2),
(97, 'ELIMINACION', 'Venta WEB-20251121150919 anulada. Stock devuelto. Motivo: por gil', '2025-11-21 15:30:43.251473', 2),
(98, 'ESTADO', 'Estado de venta WEB-251121160421-137 cambiado de Pendiente de pago a Listo para retirar', '2025-11-21 16:05:00.922442', 2),
(99, 'MODIFICACION', 'Actualización iPhone iPhone 11 (64GB / Morado)', '2025-11-21 16:16:14.355024', 2),
(100, 'ESTADO', 'Estado de venta WEB-251121170232-788 cambiado de Pendiente de pago a Completado', '2025-11-21 17:05:33.729459', 2),
(102, 'VENTA', 'Venta POS-BD33A466 por $3120004.00 (efectivo).', '2025-11-21 17:17:37.153510', 2),
(103, 'VENTA', 'Venta POS-3CD519E6 por $1.00 (efectivo).', '2025-11-21 17:20:01.793661', 2),
(104, 'ESTADO', 'Estado de venta WEB-251121170742-675 cambiado de Pendiente de pago a Devuelto', '2025-11-21 18:09:41.888222', 2),
(105, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - 0 → 11', '2025-11-21 18:24:08.609898', 2),
(106, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - 0 → 0', '2025-11-21 18:24:08.615375', 2),
(107, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - 0 → 11', '2025-11-21 18:24:17.343316', 2),
(108, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN) - 0 → 0', '2025-11-21 18:24:17.346473', 2),
(109, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - 11 → 10', '2025-11-21 18:28:33.895534', 2),
(110, 'MODIFICACION', 'Stock actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - 10 → 21', '2025-11-21 18:28:45.663759', 2),
(111, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - MAYORISTA ARS - 1212.00 → 1500', '2025-11-21 18:29:39.844008', 2),
(112, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - MAYORISTA ARS - 1212.00 → 0', '2025-11-21 18:29:39.847144', 2),
(113, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - MAYORISTA ARS - 0.00 → 0', '2025-11-21 18:29:45.440431', 2),
(114, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - MAYORISTA ARS - 0.00 → 1500', '2025-11-21 18:29:49.783736', 2),
(115, 'MODIFICACION', 'Precio actualizado: Adaptador 20W Tipo C Oogan (ADAPTADOR-20W-TIPO-C-OOGAN-1) - MAYORISTA ARS - 0.00 → 0', '2025-11-21 18:29:49.785559', 2),
(116, 'ESTADO', 'Estado de venta WEB-251121200341-751 cambiado de Pendiente de pago a Pendiente de armado', '2025-11-21 20:04:42.744852', 2),
(117, 'MODIFICACION', 'Actualización iPhone iPhone 11 (64GB / Morado)', '2025-11-21 20:12:25.022684', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_categoria`
--

CREATE TABLE IF NOT EXISTS `inventario_categoria` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `descripcion` longtext NOT NULL,
  `garantia_dias` int(10) UNSIGNED DEFAULT NULL,
  `parent_id` bigint(20) DEFAULT NULL
) ;

--
-- RELACIONES PARA LA TABLA `inventario_categoria`:
--   `parent_id`
--       `inventario_categoria` -> `id`
--

--
-- Volcado de datos para la tabla `inventario_categoria`
--

INSERT INTO `inventario_categoria` (`id`, `nombre`, `descripcion`, `garantia_dias`, `parent_id`) VALUES
(1, 'CARGADORES', '', 30, NULL),
(2, 'Celulares', '', 60, NULL),
(3, 'Fundas', '', 1, NULL),
(4, 'Iphone', '', NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_detalleiphone`
--

CREATE TABLE IF NOT EXISTS `inventario_detalleiphone` (
  `id` bigint(20) NOT NULL,
  `imei` varchar(15) DEFAULT NULL,
  `salud_bateria` int(10) UNSIGNED DEFAULT NULL,
  `fallas_detectadas` longtext NOT NULL,
  `es_plan_canje` tinyint(1) NOT NULL,
  `costo_usd` decimal(10,2) DEFAULT NULL,
  `precio_venta_usd` decimal(10,2) NOT NULL,
  `precio_oferta_usd` decimal(10,2) DEFAULT NULL,
  `notas` longtext NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `variante_id` bigint(20) DEFAULT NULL
) ;

--
-- RELACIONES PARA LA TABLA `inventario_detalleiphone`:
--   `variante_id`
--       `inventario_productovariante` -> `id`
--

--
-- Volcado de datos para la tabla `inventario_detalleiphone`
--

INSERT INTO `inventario_detalleiphone` (`id`, `imei`, `salud_bateria`, `fallas_detectadas`, `es_plan_canje`, `costo_usd`, `precio_venta_usd`, `precio_oferta_usd`, `notas`, `foto`, `creado`, `actualizado`, `variante_id`) VALUES
(2, '123456789012340', 12, '', 1, 1222.00, 1222.00, NULL, '', '', '2025-11-13 03:44:06.001074', '2025-11-13 16:21:56.588624', 4),
(3, NULL, 100, '', 1, 1000.00, 1500.00, NULL, '', '', '2025-11-13 15:28:11.070914', '2025-11-13 18:59:41.116985', 9),
(7, NULL, 100, '', 1, 200.00, 250.00, NULL, '', '', '2025-11-14 00:07:07.862305', '2025-11-21 20:12:25.021083', 454);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_plancanjeconfig`
--

CREATE TABLE IF NOT EXISTS `inventario_plancanjeconfig` (
  `id` bigint(20) NOT NULL,
  `modelo_iphone` varchar(100) NOT NULL,
  `capacidad` varchar(20) NOT NULL,
  `valor_base_canje_usd` decimal(10,2) NOT NULL,
  `descuentos_bateria` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`descuentos_bateria`)),
  `descuentos_estado` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`descuentos_estado`)),
  `descuentos_accesorios` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`descuentos_accesorios`)),
  `guia_estado_excelente` longtext NOT NULL,
  `guia_estado_bueno` longtext NOT NULL,
  `guia_estado_regular` longtext NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `descuentos_botones` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `inventario_plancanjeconfig`:
--

--
-- Volcado de datos para la tabla `inventario_plancanjeconfig`
--

INSERT INTO `inventario_plancanjeconfig` (`id`, `modelo_iphone`, `capacidad`, `valor_base_canje_usd`, `descuentos_bateria`, `descuentos_estado`, `descuentos_accesorios`, `guia_estado_excelente`, `guia_estado_bueno`, `guia_estado_regular`, `activo`, `creado`, `actualizado`, `descuentos_botones`, `descuentos_camara`, `descuentos_marco`, `descuentos_pantalla`) VALUES
(2, 'iPhone 11', '64GB', 200.00, '{\"<80\": 0.2, \">90\": 0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.307988', '2025-11-14 17:26:12.285173', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(3, 'iPhone 11', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.311988', '2025-11-14 17:21:32.380080', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(4, 'iPhone 11', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.316920', '2025-11-14 17:21:32.382099', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(5, 'iPhone 11 Pro', '64GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.321887', '2025-11-14 17:21:32.386125', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(6, 'iPhone 11 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.321887', '2025-11-14 17:21:32.388141', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(7, 'iPhone 11 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.321887', '2025-11-14 17:21:32.388141', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(8, 'iPhone 11 Pro Max', '64GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.334364', '2025-11-14 17:21:32.394526', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(9, 'iPhone 11 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.335877', '2025-11-14 17:21:32.394526', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(10, 'iPhone 11 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.335877', '2025-11-14 17:21:32.394526', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(11, 'iPhone 12', '64GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.335877', '2025-11-14 17:21:32.408283', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(12, 'iPhone 12', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.350047', '2025-11-14 17:21:32.410300', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(13, 'iPhone 12', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.352405', '2025-11-14 17:21:32.410300', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(14, 'iPhone 12 mini', '64GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.352405', '2025-11-14 17:21:32.410300', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(15, 'iPhone 12 mini', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.352405', '2025-11-14 17:21:32.421913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(16, 'iPhone 12 mini', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.367549', '2025-11-14 17:21:32.421913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(17, 'iPhone 12 Pro', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.368448', '2025-11-14 17:21:32.432100', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(18, 'iPhone 12 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.368448', '2025-11-14 17:21:32.432100', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(19, 'iPhone 12 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.368448', '2025-11-14 17:21:32.438237', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(20, 'iPhone 12 Pro Max', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.381828', '2025-11-14 17:21:32.438746', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(21, 'iPhone 12 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.387382', '2025-11-14 17:21:32.438746', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(22, 'iPhone 12 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.387382', '2025-11-14 17:21:32.438746', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(23, 'iPhone 13', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.387382', '2025-11-14 17:21:32.438746', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(24, 'iPhone 13', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.387382', '2025-11-14 17:21:32.438746', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(25, 'iPhone 13', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.404611', '2025-11-14 17:21:32.456146', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(26, 'iPhone 13 mini', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.404611', '2025-11-14 17:21:32.456146', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(27, 'iPhone 13 mini', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.404611', '2025-11-14 17:21:32.456146', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(28, 'iPhone 13 mini', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.404611', '2025-11-14 17:21:32.456146', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(29, 'iPhone 13 Pro', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.423621', '2025-11-14 17:21:32.466332', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(30, 'iPhone 13 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.425581', '2025-11-14 17:21:32.466332', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(31, 'iPhone 13 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.425581', '2025-11-14 17:21:32.466332', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(32, 'iPhone 13 Pro', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.425581', '2025-11-14 17:21:32.481786', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(33, 'iPhone 13 Pro Max', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.434225', '2025-11-14 17:21:32.482584', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(34, 'iPhone 13 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.439113', '2025-11-14 17:21:32.482584', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(35, 'iPhone 13 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.439113', '2025-11-14 17:21:32.482584', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(36, 'iPhone 13 Pro Max', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.439113', '2025-11-14 17:21:32.482584', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(37, 'iPhone 14', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.439113', '2025-11-14 17:21:32.497913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(38, 'iPhone 14', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.451901', '2025-11-14 17:21:32.497913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(39, 'iPhone 14', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.453894', '2025-11-14 17:21:32.497913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(40, 'iPhone 14 Plus', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.453894', '2025-11-14 17:21:32.497913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(41, 'iPhone 14 Plus', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.453894', '2025-11-14 17:21:32.497913', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(42, 'iPhone 14 Plus', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.453894', '2025-11-14 17:21:32.513909', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(43, 'iPhone 14 Pro', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.453894', '2025-11-14 17:21:32.513909', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(44, 'iPhone 14 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.468866', '2025-11-14 17:21:32.513909', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(45, 'iPhone 14 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.471862', '2025-11-14 17:21:32.523423', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(46, 'iPhone 14 Pro', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.473858', '2025-11-14 17:21:32.526430', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(47, 'iPhone 14 Pro Max', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.476858', '2025-11-14 17:21:32.530814', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(48, 'iPhone 14 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.478858', '2025-11-14 17:21:32.533326', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(49, 'iPhone 14 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.481858', '2025-11-14 17:21:32.535324', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(50, 'iPhone 14 Pro Max', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.484378', '2025-11-14 17:21:32.537324', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}');
INSERT INTO `inventario_plancanjeconfig` (`id`, `modelo_iphone`, `capacidad`, `valor_base_canje_usd`, `descuentos_bateria`, `descuentos_estado`, `descuentos_accesorios`, `guia_estado_excelente`, `guia_estado_bueno`, `guia_estado_regular`, `activo`, `creado`, `actualizado`, `descuentos_botones`, `descuentos_camara`, `descuentos_marco`, `descuentos_pantalla`) VALUES
(51, 'iPhone 15', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.488394', '2025-11-14 17:21:32.539324', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(52, 'iPhone 15', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.490391', '2025-11-14 17:21:32.541324', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(53, 'iPhone 15', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.493390', '2025-11-14 17:21:32.545047', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(54, 'iPhone 15 Plus', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.495391', '2025-11-14 17:21:32.545047', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(55, 'iPhone 15 Plus', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.498391', '2025-11-14 17:21:32.545047', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(56, 'iPhone 15 Plus', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.500816', '2025-11-14 17:21:32.545047', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(57, 'iPhone 15 Pro', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.502827', '2025-11-14 17:21:32.545047', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(58, 'iPhone 15 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.502827', '2025-11-14 17:21:32.545047', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(59, 'iPhone 15 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.502827', '2025-11-14 17:21:32.560030', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(60, 'iPhone 15 Pro', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.502827', '2025-11-14 17:21:32.564822', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(61, 'iPhone 15 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.502827', '2025-11-14 17:21:32.564822', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(62, 'iPhone 15 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.516313', '2025-11-14 17:21:32.564822', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(63, 'iPhone 15 Pro Max', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.518786', '2025-11-14 17:21:32.564822', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(64, 'iPhone 16', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.521691', '2025-11-14 17:21:32.575843', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(65, 'iPhone 16', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.523482', '2025-11-14 17:21:32.575843', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(66, 'iPhone 16', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.523482', '2025-11-14 17:21:32.581819', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(67, 'iPhone 16 Plus', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.523482', '2025-11-14 17:21:32.581819', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(68, 'iPhone 16 Plus', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.532714', '2025-11-14 17:21:32.581819', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(69, 'iPhone 16 Plus', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.536704', '2025-11-14 17:21:32.592486', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(70, 'iPhone 16 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.538703', '2025-11-14 17:21:32.592486', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(71, 'iPhone 16 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.541700', '2025-11-14 17:21:32.592486', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(72, 'iPhone 16 Pro', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.543700', '2025-11-14 17:21:32.592486', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(73, 'iPhone 16 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.545700', '2025-11-14 17:21:32.592486', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(74, 'iPhone 16 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.548700', '2025-11-14 17:21:32.609632', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(75, 'iPhone 16 Pro Max', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.551279', '2025-11-14 17:21:32.615660', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(76, 'iPhone 17', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.554352', '2025-11-14 17:21:32.617668', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(77, 'iPhone 17', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.556352', '2025-11-14 17:21:32.617668', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(78, 'iPhone 17', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.558352', '2025-11-14 17:21:32.623668', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(79, 'iPhone 17 Plus', '128GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.561353', '2025-11-14 17:21:32.631844', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(80, 'iPhone 17 Plus', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.563351', '2025-11-14 17:21:32.631844', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(81, 'iPhone 17 Plus', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.566352', '2025-11-14 17:21:32.639644', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(82, 'iPhone 17 Pro', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.567359', '2025-11-14 17:21:32.640272', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(83, 'iPhone 17 Pro', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.567359', '2025-11-14 17:21:32.640272', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(84, 'iPhone 17 Pro', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.567359', '2025-11-14 17:21:32.640272', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(85, 'iPhone 17 Pro Max', '256GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.567359', '2025-11-14 17:21:32.655753', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(86, 'iPhone 17 Pro Max', '512GB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.567359', '2025-11-14 17:21:32.662593', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}'),
(87, 'iPhone 17 Pro Max', '1TB', 0.00, '{\"<80\": 0.15, \">90\": 0.0, \"80-90\": 0.1}', '{\"bueno\": 0.05, \"regular\": 0.15, \"excelente\": 0.0}', '{\"sin_caja\": 0.02}', 'Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños', '1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan', 'Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles', 1, '2025-11-14 17:18:02.567359', '2025-11-14 17:21:32.662593', '{\"todos_funcionan\": 0.0, \"alguno_no_funciona\": 0.05, \"varios_no_funcionan\": 0.1}', '{\"rota\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.02, \"rayas_visibles\": 0.05}', '{\"golpes\": 0.05, \"perfecto\": 0.0, \"arañazos\": 0.02, \"deformado\": 0.1}', '{\"grieta\": 0.15, \"perfecta\": 0.0, \"rayas_menores\": 0.03, \"rayas_visibles\": 0.08}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_plancanjetransaccion`
--

CREATE TABLE IF NOT EXISTS `inventario_plancanjetransaccion` (
  `id` bigint(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `cliente_nombre` varchar(200) NOT NULL,
  `cliente_documento` varchar(40) NOT NULL,
  `iphone_recibido_modelo` varchar(100) NOT NULL,
  `iphone_recibido_capacidad` varchar(20) NOT NULL,
  `iphone_recibido_color` varchar(50) NOT NULL,
  `iphone_recibido_imei` varchar(15) NOT NULL,
  `iphone_recibido_bateria` int(10) UNSIGNED NOT NULL,
  `iphone_recibido_estado` varchar(20) NOT NULL,
  `iphone_recibido_accesorios` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`iphone_recibido_accesorios`)),
  `iphone_recibido_observaciones` longtext NOT NULL,
  `valor_base_usd` decimal(10,2) NOT NULL,
  `descuento_bateria_porcentaje` decimal(5,2) NOT NULL,
  `descuento_estado_porcentaje` decimal(5,2) NOT NULL,
  `descuento_accesorios_porcentaje` decimal(5,2) NOT NULL,
  `valor_calculado_usd` decimal(10,2) NOT NULL,
  `valor_calculado_ars` decimal(12,2) NOT NULL,
  `ajuste_manual_ars` decimal(12,2) NOT NULL,
  `valor_iphone_entregado_ars` decimal(12,2) NOT NULL,
  `diferencia_ars` decimal(12,2) NOT NULL,
  `notas` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `cliente_id` bigint(20) DEFAULT NULL,
  `detalle_iphone_recibido_id` bigint(20) DEFAULT NULL,
  `iphone_entregado_id` bigint(20) DEFAULT NULL,
  `vendedor_id` int(11) DEFAULT NULL,
  `venta_asociada_id` varchar(20) DEFAULT NULL,
  `descuento_botones_porcentaje` decimal(5,2) NOT NULL,
  `descuento_camara_porcentaje` decimal(5,2) NOT NULL,
  `descuento_marco_porcentaje` decimal(5,2) NOT NULL,
  `descuento_pantalla_porcentaje` decimal(5,2) NOT NULL,
  `iphone_recibido_estado_botones` varchar(50) NOT NULL,
  `iphone_recibido_estado_camara` varchar(50) NOT NULL,
  `iphone_recibido_estado_marco` varchar(50) NOT NULL,
  `iphone_recibido_estado_pantalla` varchar(50) NOT NULL
) ;

--
-- RELACIONES PARA LA TABLA `inventario_plancanjetransaccion`:
--   `cliente_id`
--       `crm_cliente` -> `id`
--   `detalle_iphone_recibido_id`
--       `inventario_detalleiphone` -> `id`
--   `iphone_entregado_id`
--       `inventario_productovariante` -> `id`
--   `vendedor_id`
--       `auth_user` -> `id`
--   `venta_asociada_id`
--       `ventas_venta` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_precio`
--

CREATE TABLE IF NOT EXISTS `inventario_precio` (
  `id` bigint(20) NOT NULL,
  `tipo_precio` varchar(20) NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `precio_venta_normal` decimal(10,2) NOT NULL,
  `precio_venta_minimo` decimal(10,2) NOT NULL,
  `precio_venta_descuento` decimal(10,2) DEFAULT NULL,
  `variante_id` bigint(20) NOT NULL,
  `moneda` varchar(10) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `creado` datetime(6) NOT NULL,
  `precio` decimal(12,2) NOT NULL,
  `tipo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `inventario_precio`:
--   `variante_id`
--       `inventario_productovariante` -> `id`
--

--
-- Volcado de datos para la tabla `inventario_precio`
--

INSERT INTO `inventario_precio` (`id`, `tipo_precio`, `costo`, `precio_venta_normal`, `precio_venta_minimo`, `precio_venta_descuento`, `variante_id`, `moneda`, `activo`, `actualizado`, `creado`, `precio`, `tipo`) VALUES
(1, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 1, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-07 16:08:45.661848', 1.00, 'MINORISTA'),
(4, 'MINORISTA', 0.00, 1222.00, 1222.00, NULL, 4, 'USD', 1, '2025-11-13 16:21:56.582362', '2025-11-13 00:44:05.000000', 1222.00, 'MINORISTA'),
(5, 'MAYORISTA', 0.00, 1222.00, 1222.00, NULL, 4, 'USD', 1, '2025-11-13 16:21:56.588624', '2025-11-13 00:44:05.000000', 1222.00, 'MAYORISTA'),
(6, 'MINORISTA', 0.00, 1500.00, 1500.00, NULL, 9, 'USD', 1, '2025-11-13 12:28:11.000000', '2025-11-13 12:28:11.000000', 1500.00, 'MINORISTA'),
(7, 'MAYORISTA', 0.00, 1500.00, 1500.00, NULL, 9, 'USD', 1, '2025-11-13 12:28:11.000000', '2025-11-13 12:28:11.000000', 1500.00, 'MAYORISTA'),
(8, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 13, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 13:51:03.000000', 1.00, 'MINORISTA'),
(9, 'MAYORISTA', 0.00, 233.00, 1212.00, NULL, 13, 'ARS', 1, '2025-11-13 13:51:19.000000', '2025-11-13 13:51:03.000000', 233.00, 'MAYORISTA'),
(184, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 191, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:02.000000', 1.00, 'MINORISTA'),
(185, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 192, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:02.000000', 1.00, 'MINORISTA'),
(186, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 193, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(187, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 194, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(188, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 195, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(189, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 196, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(190, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 197, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(191, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 198, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(192, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 199, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(193, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 200, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(194, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 201, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(195, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 202, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(196, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 203, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(197, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 204, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(198, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 205, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(199, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 206, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(200, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 207, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(201, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 208, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(202, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 209, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(203, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 210, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(204, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 211, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(205, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 212, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(206, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 213, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(207, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 214, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(208, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 215, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(209, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 216, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(210, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 217, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(211, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 218, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(212, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 219, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(213, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 220, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(214, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 221, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(215, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 222, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(216, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 223, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(217, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 224, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(218, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 225, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(219, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 226, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(220, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 227, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(221, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 228, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(222, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 229, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(223, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 230, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(224, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 231, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(225, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 232, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(226, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 233, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(227, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 234, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(228, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 235, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(229, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 236, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(230, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 237, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(231, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 238, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(232, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 239, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(233, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 240, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(234, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 241, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(235, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 242, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(236, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 243, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(237, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 244, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(238, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 245, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(239, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 246, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(240, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 247, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(241, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 248, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(242, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 249, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(243, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 250, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(244, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 251, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(245, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 252, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(246, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 253, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(247, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 254, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(248, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 255, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(249, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 256, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(250, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 257, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(251, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 258, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(252, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 259, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:03.000000', 1.00, 'MINORISTA'),
(253, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 260, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(254, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 261, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(255, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 262, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(256, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 263, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(257, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 264, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(258, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 265, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(259, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 266, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(260, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 267, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(261, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 268, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(262, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 269, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(263, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 270, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(264, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 271, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(265, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 272, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(266, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 273, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(267, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 274, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(268, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 275, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(269, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 276, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(270, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 277, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(271, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 278, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(272, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 279, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(273, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 280, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(274, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 281, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(275, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 282, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(276, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 283, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(277, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 284, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(278, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 285, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(279, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 286, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(280, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 287, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(281, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 288, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(282, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 289, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(283, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 290, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(284, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 291, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(285, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 292, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(286, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 293, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(287, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 294, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(288, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 295, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(289, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 296, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(290, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 297, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(291, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 298, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(292, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 299, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(293, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 300, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(294, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 301, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(295, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 302, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(296, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 303, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(297, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 304, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(298, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 305, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(299, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 306, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(300, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 307, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(301, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 308, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(302, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 309, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(303, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 310, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(304, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 311, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(305, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 312, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(306, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 313, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(307, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 314, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(308, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 315, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(309, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 316, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(310, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 317, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(311, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 318, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(312, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 319, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(313, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 320, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(314, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 321, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(315, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 322, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(316, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 323, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(317, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 324, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(318, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 325, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(319, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 326, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(320, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 327, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(321, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 328, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(322, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 329, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(323, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 330, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(324, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 331, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(325, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 332, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(326, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 333, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(327, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 334, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(328, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 335, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(329, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 336, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(330, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 337, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(331, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 338, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:04.000000', 1.00, 'MINORISTA'),
(332, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 339, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(333, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 340, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(334, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 341, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(335, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 342, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(336, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 343, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(337, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 344, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(338, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 345, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(339, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 346, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(340, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 347, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(341, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 348, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(342, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 349, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(343, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 350, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(344, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 351, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(345, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 352, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(346, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 353, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(347, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 354, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(348, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 355, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(349, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 356, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(350, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 357, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(351, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 358, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(352, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 359, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(353, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 360, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(354, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 361, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(355, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 362, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(356, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 363, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(357, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 364, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(358, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 365, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(359, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 366, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(360, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 367, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(361, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 368, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(362, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 369, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(363, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 370, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(364, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 371, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(365, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 372, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(366, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 373, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(367, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 374, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(368, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 375, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(369, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 376, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(370, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 377, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(371, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 378, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(372, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 379, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(373, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 380, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(374, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 381, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(375, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 382, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(376, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 383, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(377, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 384, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(378, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 385, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(379, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 386, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(380, 'MINORISTA', 0.00, 1560000.00, 1560000.00, NULL, 387, 'ARS', 1, '2025-11-21 15:31:22.000000', '2025-11-13 14:13:05.000000', 1560000.00, 'MINORISTA'),
(381, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 388, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(382, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 389, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(383, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 390, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(384, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 391, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(385, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 392, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(386, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 393, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(387, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 394, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(388, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 395, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(389, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 396, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(390, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 397, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(391, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 398, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(392, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 399, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(393, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 400, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(394, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 401, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(395, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 402, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(396, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 403, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(397, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 404, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(398, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 405, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(399, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 406, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(400, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 407, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(401, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 408, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(402, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 409, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(403, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 410, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(404, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 411, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(405, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 412, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(406, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 413, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(407, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 414, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(408, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 415, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(409, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 416, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(410, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 417, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(411, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 418, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(412, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 419, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:05.000000', 1.00, 'MINORISTA'),
(413, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 420, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(414, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 421, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(415, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 422, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(416, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 423, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(417, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 424, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(418, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 425, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(419, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 426, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(420, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 427, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(421, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 428, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(422, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 429, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(423, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 430, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(424, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 431, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(425, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 432, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(426, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 433, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(427, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 434, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(428, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 435, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(429, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 436, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(430, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 437, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(431, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 438, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(432, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 439, 'ARS', 1, '2025-11-13 17:23:39.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(433, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 440, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(434, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 441, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(435, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 442, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(436, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 443, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(437, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 444, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(438, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 445, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(439, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 446, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(440, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 447, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(441, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 448, 'ARS', 1, '2025-11-13 17:23:37.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(442, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 449, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(443, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 450, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(444, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 451, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 14:13:06.000000', 1.00, 'MINORISTA'),
(445, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 453, 'ARS', 1, '2025-11-13 17:23:36.000000', '2025-11-13 17:14:45.000000', 1.00, 'MINORISTA'),
(446, 'MAYORISTA', 1222.00, 1212.00, 1212.00, NULL, 453, 'ARS', 1, '2025-11-13 17:14:45.000000', '2025-11-13 17:14:45.000000', 1212.00, 'MAYORISTA'),
(447, 'MINORISTA', 1.00, 1.00, 1.00, NULL, 452, 'ARS', 1, '2025-11-13 17:23:38.000000', '2025-11-13 17:23:38.000000', 1.00, 'MINORISTA'),
(448, 'MAYORISTA', 0.00, 1500.00, 1560000.00, NULL, 387, 'ARS', 1, '2025-11-21 15:31:22.000000', '2025-11-14 15:48:54.000000', 1500.00, 'MAYORISTA'),
(450, 'MINORISTA', 0.00, 250.00, 250.00, NULL, 454, 'USD', 1, '2025-11-21 20:12:25.016889', '2025-11-21 13:46:35.000000', 250.00, 'MINORISTA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_producto`
--

CREATE TABLE IF NOT EXISTS `inventario_producto` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `actualizado` datetime(6) DEFAULT NULL,
  `categoria_id` bigint(20) DEFAULT NULL,
  `proveedor_id` bigint(20) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `seo_descripcion` varchar(160) DEFAULT NULL,
  `seo_titulo` varchar(70) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `codigo_barras` varchar(64) DEFAULT NULL,
  `imagen_codigo_barras` varchar(255) DEFAULT NULL,
  `creado` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `inventario_producto`:
--   `categoria_id`
--       `inventario_categoria` -> `id`
--   `proveedor_id`
--       `inventario_proveedor` -> `id`
--

--
-- Volcado de datos para la tabla `inventario_producto`
--

INSERT INTO `inventario_producto` (`id`, `nombre`, `descripcion`, `actualizado`, `categoria_id`, `proveedor_id`, `estado`, `seo_descripcion`, `seo_titulo`, `activo`, `codigo_barras`, `imagen_codigo_barras`, `creado`) VALUES
(1, 'Cargador 20w', '', '2025-11-12 21:57:09.263095', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023'),
(2, 'Cargador 20w', 'Caragdor 292', '2025-11-13 20:23:37.302696', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-07 16:08:45.733023'),
(11, 'iPhone 16', '', '2025-11-13 16:21:56.571924', 2, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 03:44:05.946364'),
(21, 'iPhone 15 Pro', '', '2025-11-13 18:59:41.081513', 2, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 15:28:11.007026'),
(25, 'FUNDAS', '', '2025-11-13 20:23:37.615629', 3, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 16:51:03.126271'),
(168, 'Cargador 20w Tipo C', '', '2025-11-13 20:23:37.325051', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:02.955582'),
(169, 'Proyector HY300', '', '2025-11-13 20:23:38.843707', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:02.999258'),
(170, 'Cargador 5w USB IPhone', '', '2025-11-13 20:23:37.350511', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.012367'),
(171, 'Cable Usb a Lightning 1mt', '', '2025-11-13 20:23:37.163354', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.025149'),
(172, 'Auriculares F9-5', '', '2025-11-13 20:23:36.655656', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.041147'),
(173, 'Auriculares vincha P9', '', '2025-11-13 20:23:36.922854', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.056354'),
(174, 'Adaptador 5w USB IPhone Cargador+Cable', '', '2025-11-13 20:23:36.105547', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.090124'),
(175, 'Cargador MagSafe IPhone', '', '2025-11-13 20:23:37.371026', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.104308'),
(176, 'OFERTA REFLECTOR Luminaria alumbrado público 150w (reflector)', '', '2025-11-13 20:23:38.573216', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.119599'),
(177, 'Cable USB C a C', '', '2025-11-13 20:23:37.202081', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.135609'),
(178, 'MacBook Air M2', '', '2025-11-13 20:23:38.356788', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.150589'),
(179, 'MagSafe Battery Pack', '', '2025-11-13 20:23:38.369796', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.164259'),
(180, 'AirPods 2 Pro AAA', '', '2025-11-13 20:23:36.327861', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.178806'),
(181, 'TV BOX PRO 5G 4K', '', '2025-11-13 20:23:39.455312', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.191952'),
(182, 'AURICULARES ULTRAPODS MAX', '', '2025-11-13 20:23:36.888636', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.204952'),
(183, 'Vaso Termico Stanley con Manija 1.4 Litros', '', '2025-11-13 20:23:39.517090', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:03.279169'),
(184, 'Cable USB a IPhone', '', '2025-11-13 20:23:37.147839', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.292380'),
(185, 'Cable USB a Micro-Usb Motorola', '', '2025-11-13 20:23:37.191471', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.307386'),
(186, 'Cargador Tipo C 3.1A Samsung', '', '2025-11-13 20:23:37.391702', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.322322'),
(187, 'Adaptador Auricular a IPhone', '', '2025-11-13 20:23:36.138264', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.337478'),
(188, 'Caloventor para Auto', '', '2025-11-13 20:23:37.279233', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.352505'),
(189, 'Luz Led Con Panel Solar (Con Forma de Copos)', '', '2025-11-13 20:23:38.342071', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.366195'),
(190, 'Casco Rebatible', '', '2025-11-13 20:23:37.404312', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.379914'),
(191, 'Adaptador Apple 20w Tipo C (ORIGINAL APPLE)', '', '2025-11-13 20:23:36.113552', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.394114'),
(192, 'Smartwatch + Accesorios', '', '2025-11-13 20:23:39.132907', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.408989'),
(193, 'Smartwatch 7 Mallas + Auriculares', '', '2025-11-13 20:23:39.158925', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.425330'),
(194, 'Termo 500ml Starry Sky', '', '2025-11-13 20:23:39.351001', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.439326'),
(195, 'Cable Usb Tipo C a Lightning 1mt', '', '2025-11-13 20:23:37.224903', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.487895'),
(196, 'Auriculares M10', '', '2025-11-13 20:23:36.800273', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.503066'),
(197, 'Cabezal Masuya Tipo C 64w', '', '2025-11-13 20:23:36.969102', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.517520'),
(198, 'Cable Usb Tipo C a C IPhone', '', '2025-11-13 20:23:37.211592', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.530323'),
(199, 'Funda Silicone Case IPhone (Consultar modelos)', '', '2025-11-13 20:23:37.586509', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.542249'),
(200, 'Funda Transparente Magsafe', '', '2025-11-13 20:23:37.601818', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:03.557261'),
(201, 'Earpods Lightning', '', '2025-11-13 20:23:37.466522', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.570487'),
(202, 'Adaptador Samsung 25W', '', '2025-11-13 20:23:36.249949', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.585997'),
(203, 'Cargador Carga Rapida Ditron 3.1A con cable', '', '2025-11-13 20:23:37.360020', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.599183'),
(204, 'Cable USB a C Samsung', '', '2025-11-13 20:23:37.136987', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.612889'),
(205, 'Cable C a C Motorola', '', '2025-11-13 20:23:37.001228', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.626829'),
(206, 'Funda rigida Transparente', '', '2025-11-13 20:23:37.563292', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.641196'),
(207, 'CABLE AUX A 2RCA', '', '2025-11-13 20:23:36.978106', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.653846'),
(208, 'Funda AirPods Pro 2 Lisa', '', '2025-11-13 20:23:37.532642', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.667530'),
(209, 'Cable Lightning A Usb IPhone 2Mt', '', '2025-11-13 20:23:37.074673', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.681015'),
(210, 'Auriculares Gamer para Xbox 360', '', '2025-11-13 20:23:36.683237', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.694173'),
(211, 'Parlante Portable Speaker Hf-323 Bluetooth', '', '2025-11-13 20:23:38.661704', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:03.707181'),
(212, 'Parlante Portable speaker Bluetooth', '', '2025-11-13 20:23:38.653192', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:03.720439'),
(213, 'Cable USB a Lightning 2mt Belkin', '', '2025-11-13 20:23:37.178661', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.734622'),
(214, 'Cable USB a C 2mt Belkin', '', '2025-11-13 20:23:37.111961', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.749629'),
(215, 'Adaptador Mosquito De Pared', '', '2025-11-13 20:23:36.216353', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.762339'),
(216, 'Adaptador Motorola + Cable Tipo C', '', '2025-11-13 20:23:36.233603', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.776907'),
(217, 'Soporte Adhesivo para Pared', '', '2025-11-13 20:23:39.261349', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.789901'),
(218, 'Auriculares AKG Samsung', '', '2025-11-13 20:23:36.605399', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.802081'),
(219, 'Adaptador Jack a USB C Samsung', '', '2025-11-13 20:23:36.163019', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.831840'),
(220, 'Adaptador Lightning Splitter', '', '2025-11-13 20:23:36.198335', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:03.846690'),
(221, 'Cargador 35w apple 2 entradas USB-C', '', '2025-11-13 20:23:37.338217', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.857693'),
(222, 'IPhone Wallet AAA', '', '2025-11-13 20:23:37.901383', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.870426'),
(223, 'Soporte celular con sopapa para vidrios y espejo', '', '2025-11-13 20:23:39.273611', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.883258'),
(224, 'Fundas varias', '', '2025-11-13 20:23:37.845928', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:03.896443'),
(225, 'Mini Proyector Astronauta', '', '2025-11-13 20:23:38.489293', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.015714'),
(226, 'Dispenser De Agua Electrico', '', '2025-11-13 20:23:37.440460', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.027457'),
(227, 'Tira Led RGB Bluetooth 5mt', '', '2025-11-13 20:23:39.406612', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.040795'),
(228, 'Maquina Mini-Donas', '', '2025-11-13 20:23:38.405513', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.054726'),
(229, 'Mochilas', '', '2025-11-13 20:23:38.526960', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.066451'),
(230, 'Lampara de Cristal Led', '', '2025-11-13 20:23:38.075006', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.081923'),
(231, 'Auriculares Y-09', '', '2025-11-13 20:23:36.947976', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.096066'),
(232, 'Mini Linterna Led Con Encendedor M8', '', '2025-11-13 20:23:38.453113', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.110018'),
(233, 'Mini Llavero Linterna Led', '', '2025-11-13 20:23:38.464630', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.123182'),
(234, 'Lava Copas', '', '2025-11-13 20:23:38.294720', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.137350'),
(235, 'Neblinero Led', '', '2025-11-13 20:23:38.560979', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.152339'),
(236, 'Lampara de Tubo Led USB', '', '2025-11-13 20:23:38.101984', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.167124'),
(237, 'Pinza Soporte para Auto', '', '2025-11-13 20:23:38.770859', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.181016'),
(238, 'Tripode 2.1mt', '', '2025-11-13 20:23:39.432974', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.194192'),
(239, 'Camara de vigilancia IP inteligente 2', '', '2025-11-13 20:23:37.290948', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.211606'),
(240, 'Repetidor Amplificador Wifi Señal 300 Mbp', '', '2025-11-13 20:23:39.060020', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.227364'),
(241, 'Joystick Inalambrico PS4', '', '2025-11-13 20:23:37.926004', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.238363'),
(242, 'Mini Plug a RCA', '', '2025-11-13 20:23:38.476630', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.253275'),
(243, 'Joystick PS3 Negro', '', '2025-11-13 20:23:37.939743', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.266468'),
(244, 'mini teclado smart', '', '2025-11-13 20:23:38.502294', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.280028'),
(245, 'auriculares royalcell', '', '2025-11-13 20:23:36.810781', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.292182'),
(246, 'Cable C a C Apple mallado 1mt', '', '2025-11-13 20:23:36.989788', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.306182'),
(247, 'Auriculares Bluetooth M90 Max', '', '2025-11-13 20:23:36.640311', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.322295'),
(248, 'lampara de mesa con cargador inalámbrico de celular', '', '2025-11-13 20:23:38.088222', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.334452'),
(249, 'Joystick Ps4 Edición Inter Miami Messi', '', '2025-11-13 20:23:37.977949', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.349272'),
(250, 'earpods 3.5mm', '', '2025-11-13 20:23:37.454203', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.395705'),
(251, 'Pendrive 64GB SanDisk', '', '2025-11-13 20:23:38.735821', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.404709'),
(252, 'Mouse Inalámbrico a Pilas', '', '2025-11-13 20:23:38.551472', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.415384'),
(253, 'Reflector LED RGB', '', '2025-11-13 20:23:38.874491', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.424394'),
(254, 'Xiaomi A3X 64GB / 3GB RAM', '', '2025-11-13 20:23:39.539844', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.435543'),
(255, 'Samsung Galaxy A05 64gb', '', '2025-11-13 20:23:39.072020', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.446587'),
(256, 'AURICULAR BT MUSIC LIFE', '', '2025-11-13 20:23:36.388721', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.456587'),
(257, 'AURICULAR SPORT BT QX15', '', '2025-11-13 20:23:36.569162', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.466355'),
(258, 'AURICULAR M19', '', '2025-11-13 20:23:36.551979', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.475435'),
(259, 'Mini-impresora Portatil', '', '2025-11-13 20:23:38.515249', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.486241'),
(260, 'Fundas Magsafe Electro', '', '2025-11-13 20:23:37.733434', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.495380'),
(261, 'Funda Magsafe Flex IPhone 13 Pro', '', '2025-11-13 20:23:37.544148', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.549534'),
(262, 'Funda Magsafe Soft IPhone 12 / 12 Pro', '', '2025-11-13 20:23:37.559297', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.559692'),
(263, 'Fundas con disipación de calor IPhone 12', '', '2025-11-13 20:23:37.660663', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.569342'),
(264, 'Cable USB a C Motorola', '', '2025-11-13 20:23:37.125304', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.605680'),
(265, 'Auriculares InPods 12', '', '2025-11-13 20:23:36.783354', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.617597'),
(266, 'Kit Mouse y Teclado Ultra Fit', '', '2025-11-13 20:23:38.059749', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.731147'),
(267, 'Receptor Bluetooth Auxiliar Para Auto', '', '2025-11-13 20:23:38.856969', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.782369'),
(268, 'Pava Electrica Para Auto 500ml', '', '2025-11-13 20:23:38.709849', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.793296'),
(269, 'Calculadora Cientifica Colores', '', '2025-11-13 20:23:37.256666', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.801299'),
(270, 'Moto E14', '', '2025-11-13 20:23:38.539471', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.827107'),
(271, 'LATTAFA Ajwad 60ml (Femenino)', '', '2025-11-13 20:23:38.153420', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.836109'),
(272, 'Reloj Curren Modelo 8346', '', '2025-11-13 20:23:38.925154', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.850404'),
(273, 'Vaso Starbucks', '', '2025-11-13 20:23:39.491949', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.861597'),
(274, 'Mini Lector De Memoria SD', '', '2025-11-13 20:23:38.440928', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.871108'),
(275, 'Lampara Led USB Bajo Mesada', '', '2025-11-13 20:23:38.126293', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.882280'),
(276, 'Holder Para Auto Soft Tube', '', '2025-11-13 20:23:37.865880', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.890279'),
(277, 'TERMO VACUUM STANLEY 1L', '', '2025-11-13 20:23:39.390792', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.900453'),
(278, 'Adaptador Samsung 45W', '', '2025-11-13 20:23:36.263961', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.934055'),
(279, 'Protector De Cable Espiral De Silicona Flexible', '', '2025-11-13 20:23:38.782884', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.945630'),
(280, 'Calculadora Científica Kenko', '', '2025-11-13 20:23:37.270232', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.954635'),
(281, 'Adaptador 20w + Cable C a Lightning', '', '2025-11-13 20:23:36.046686', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:04.964296'),
(282, 'Vaso Termico Stanley Bi-Color', '', '2025-11-13 20:23:39.505361', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.974302'),
(283, 'Smartwatch Con Parlante y Accesorios', '', '2025-11-13 20:23:39.174454', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.985459'),
(284, 'Esfera de Luz Grande', '', '2025-11-13 20:23:37.491276', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:04.995596'),
(285, 'Parlante Bluetooth Con Micrófono Karaoke', '', '2025-11-13 20:23:38.608309', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.018148'),
(286, 'ZTE Blade A35 64 GB 6 GB', '', '2025-11-13 20:23:39.586704', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.028936'),
(287, 'Auriculares Tipo JBL Vincha Bluetooth', '', '2025-11-13 20:23:36.824118', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.038936'),
(288, 'Auriculares ANC ENC PURE BASS B.T Zero Cables(color negro)', '', '2025-11-13 20:23:36.624164', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.049965'),
(289, 'AirPods 4(+AAA)', '', '2025-11-13 20:23:36.341515', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.060107'),
(290, 'Air Pods con pantalla', '', '2025-11-13 20:23:36.317857', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.070616'),
(291, 'Luces Neon Led 5 MT', '', '2025-11-13 20:23:38.328558', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.081166'),
(292, 'Luces Led Flexiblkes 1 mt RGB', '', '2025-11-13 20:23:38.306719', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.104333'),
(293, 'Soporte Video Making Led Microphone', '', '2025-11-13 20:23:39.310807', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.116698'),
(294, 'Smartwacht T9 con caja', '', '2025-11-13 20:23:39.119898', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.127021'),
(295, 'Smartwach A100 + 7 mallas', '', '2025-11-13 20:23:39.107371', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.137021'),
(296, 'Smartwatch S300 Max (7 Mallas + Auriculares bluetooth)', '', '2025-11-13 20:23:39.200961', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.147642'),
(297, 'Smartwatch + Auriculares Vincha P9 y 7 mallas', '', '2025-11-13 20:23:39.144413', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.156643'),
(298, 'Kit de herramientas', '', '2025-11-13 20:23:37.992812', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.167709'),
(299, 'Proyector Astronauta Con Parlante', '', '2025-11-13 20:23:38.794391', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.177017'),
(300, 'Proyector astronauta chico(caja azul)', '', '2025-11-13 20:23:38.819900', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.186015'),
(301, 'Proyector con Consola de Videojuegos', '', '2025-11-13 20:23:38.831356', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.195257'),
(302, 'Foco parlante para Fiesta', '', '2025-11-13 20:23:37.506075', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.204261'),
(303, 'Parlante Bluetooth hf3223', '', '2025-11-13 20:23:38.620313', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.215685'),
(304, 'Consola Gamepad con pantalla', '', '2025-11-13 20:23:37.416201', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.225862'),
(305, 'Soporte para Tablet', '', '2025-11-13 20:23:39.299302', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.234859'),
(306, 'Mallas varias_x000D__x000D__x000D__x000D__x000D__x000D__x000D__x000D__x000D__x000D__x000D_', '', '2025-11-13 20:23:38.392513', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.244819'),
(307, 'smartwatch t9 (outlet)', '', '2025-11-13 20:23:39.211466', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.253826'),
(308, 'Parlante Lampara Portable', '', '2025-11-13 20:23:38.640071', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.264501'),
(309, 'Humidificador Difusor Aromatizador Ultrasonico Llama', '', '2025-11-13 20:23:37.889043', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.274380'),
(310, 'Lattafa Fakhar Black 100ml', '', '2025-11-13 20:23:38.220646', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.285964'),
(311, 'Maison Alhambra Pink Velvet 80 ML EDP', '', '2025-11-13 20:23:38.380800', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.295117'),
(312, 'Reloj Duantai Modelo 1173', '', '2025-11-13 20:23:38.992981', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.304121'),
(313, 'Reloj Duantai Modelo 1187', '', '2025-11-13 20:23:39.010492', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.314502'),
(314, 'Reloj Duantai Modelo 8190', '', '2025-11-13 20:23:39.027454', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.324008'),
(315, 'Reloj Kadibin (Richard Mille)', '', '2025-11-13 20:23:39.044967', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.334157'),
(316, 'Reloj Curren Modelo 8149', '', '2025-11-13 20:23:38.892242', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.345354'),
(317, 'Reloj Curren Modelo 8362', '', '2025-11-13 20:23:38.941665', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.355354'),
(318, 'Reloj Curren Modelo 8443', '', '2025-11-13 20:23:38.959449', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.366107'),
(319, 'Reloj Curren Modelo 8229', '', '2025-11-13 20:23:38.910416', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.376911'),
(320, 'Reloj Deportivo Banami Modelo 1815G', '', '2025-11-13 20:23:38.977454', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.393593'),
(321, 'Auriculares Gamer Microfono Pc Noga Stormer St Hex Headset', '', '2025-11-13 20:23:36.668836', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.407948'),
(322, 'Adaptador XIAOMI 120W USB', '', '2025-11-13 20:23:36.292289', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.425453'),
(323, 'Adaptador XIAOMI 67W USB', '', '2025-11-13 20:23:36.306077', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.439961'),
(324, 'Pilas AAA Oryx', '', '2025-11-13 20:23:38.758859', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.454335'),
(325, 'Pilas AA Hytoshy', '', '2025-11-13 20:23:38.749344', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.467672'),
(326, 'Auriculares Vincha Plegables con Cable Desmontable', '', '2025-11-13 20:23:36.936163', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.482698'),
(327, 'Auricular Earpod simil Tipo C', '', '2025-11-13 20:23:36.423466', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.497370'),
(328, 'SmartWatch TK Ultra 2', '', '2025-11-13 20:23:39.223960', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.511736'),
(329, 'Tira Neon 1mt Con control', '', '2025-11-13 20:23:39.419754', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.522745'),
(330, 'Adaptador 20W Tipo C Oogan', '', '2025-11-21 18:31:22.089808', 1, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 17:13:05.538404'),
(331, 'Adaptador 20W Tipo C Con Cable Tipo C a C Oogan', '', '2025-11-13 20:23:36.070525', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.553494'),
(332, 'Lámpara Filamento Led Imán Recargable Velador Decorativo tl49', '', '2025-11-13 20:23:38.115292', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.567211'),
(333, 'Samsung Galaxy a06 64GB 4RAM', '', '2025-11-13 20:23:39.084357', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.582159'),
(334, 'Vidrios Templados', '', '2025-11-13 20:23:39.528092', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.596831'),
(335, 'Cable C a Lightning 2mt', '', '2025-11-13 20:23:37.011739', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.611352'),
(336, 'Cable Universal Tipo C - USB - Lightning', '', '2025-11-13 20:23:37.102451', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.625522'),
(337, 'Parlante JBL Clip5', '', '2025-11-13 20:23:38.629317', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.638025'),
(338, 'Cargador Para Auto Mixor 12v', '', '2025-11-13 20:23:37.382194', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.652100'),
(339, 'TV Stick Watch', '', '2025-11-13 20:23:39.479901', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.665760'),
(340, 'Smartwatch GT1', '', '2025-11-13 20:23:39.189773', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.677703'),
(341, 'Memoria Micro-SD 128GB Speed Flash', '', '2025-11-13 20:23:38.418411', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.689708'),
(342, 'Smartwatch Y20 + 7 Mallas', '', '2025-11-13 20:23:39.248832', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.702743'),
(343, 'Auriculares TWS-123 Con Pantalla', '', '2025-11-13 20:23:36.836586', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.717244'),
(344, 'Proyector Astronauta Sin Parlante', '', '2025-11-13 20:23:38.806391', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.730437'),
(345, 'Cable HDMI Mallado', '', '2025-11-13 20:23:37.052685', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.743705'),
(346, 'Parlante Tipo JBL GO4 Pro', '', '2025-11-13 20:23:38.700341', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.790538'),
(347, 'Parlante Tipo JBL GO3', '', '2025-11-13 20:23:38.686828', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.802697'),
(348, 'Parlante Tipo JBL Alexa', '', '2025-11-13 20:23:38.672704', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.815499'),
(349, 'AirPods Pro Max', '', '2025-11-13 20:23:36.354517', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.828645'),
(350, 'Smartwatch Ultra 9 - 7 Mallas intercambiables', '', '2025-11-13 20:23:39.237176', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.843690'),
(351, 'Armas de Hidrogel', '', '2025-11-13 20:23:36.365692', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.856693'),
(352, 'LATTAFA Ajwad Pink To 60ml', '', '2025-11-13 20:23:38.168931', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.871355'),
(353, 'LATTAFA Asad Bourbon 100ml', '', '2025-11-13 20:23:38.184980', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.886450'),
(354, 'LATTAFA Badee Noble Blush 100ml', '', '2025-11-13 20:23:38.196137', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.900615'),
(355, 'LATTAFA Eclaire Femenino 100ml', '', '2025-11-13 20:23:38.208647', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.916419'),
(356, 'LATTAFA Yara Candy 100ml', '', '2025-11-13 20:23:38.283202', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.929085'),
(357, 'ZIMAYA Only You 100ml', '', '2025-11-13 20:23:39.574316', 1, NULL, 'ACTIVO', NULL, NULL, 0, '', NULL, '2025-11-13 17:13:05.944491'),
(358, 'ORIENTICA Royal Amber (Unisex)', '', '2025-11-13 20:23:38.585294', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.958933'),
(359, 'Bolso Jordan Air Festival (ORIGINAL)', '', '2025-11-13 20:23:36.958480', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.971441'),
(360, 'Lattafa Habik Women 100ml', '', '2025-11-13 20:23:38.243386', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.984711'),
(361, 'LATTAFA Shahd Eau de Parfum 100ml', '', '2025-11-13 20:23:38.256897', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:05.997894'),
(362, 'LATTAFA Fhakar Gold 100ml', '', '2025-11-13 20:23:38.232876', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.011679'),
(363, 'Zimaya Hayam Eau de Parfum 100ml', '', '2025-11-13 20:23:39.559785', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.024901'),
(364, 'Zimaya Fatima Pink 100ml', '', '2025-11-13 20:23:39.551275', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.037410'),
(365, 'Lattafa The Kingdom Man 100ml', '', '2025-11-13 20:23:38.269898', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.050806'),
(366, 'Adaptador Tipo C a Audio/Charging', '', '2025-11-13 20:23:36.278508', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.064434'),
(367, 'HUB Tipo C', '', '2025-11-13 20:23:37.875882', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.080208'),
(368, 'Microfono Lu-b24', '', '2025-11-13 20:23:38.427415', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.094863'),
(369, 'FREIDORA DE AIRE 10L', '', '2025-11-13 20:23:37.519351', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.105867'),
(370, 'Lampara Sunset Light Con Tripode', '', '2025-11-13 20:23:38.139115', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.120261'),
(371, 'PAD ESCRITORIO 600X300X2MM', '', '2025-11-13 20:23:38.595805', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.133917'),
(372, 'AURICULAR CABLE S8', '', '2025-11-13 20:23:36.400968', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.149594'),
(373, 'AURICULARES VINCHA BT', '', '2025-11-13 20:23:36.901213', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.164273'),
(374, 'TV STICK 8G 4K', '', '2025-11-13 20:23:39.468563', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.178665'),
(375, 'CORTA PELO DE COLORES DIGITAL MELECH', '', '2025-11-13 20:23:37.427713', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.190665'),
(376, 'Set 5 Bowls De Acero Inoxidable Con Tapa Recipiente Metalico', '', '2025-11-13 20:23:39.093867', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.202818'),
(377, 'Kit Mochila Antirrobo Urbana Para Notebook Morral Estuche 3 en 1', '', '2025-11-13 20:23:38.006609', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.215817'),
(378, 'TV BOX Caja Verde 4k Ultra HD 512gb + 64gb ram', '', '2025-11-13 20:23:39.443483', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.229581'),
(379, 'Adaptador Cargado Auto a Tipo C', '', '2025-11-13 20:23:36.151080', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.244597'),
(380, 'Soporte Para Celular Plegable Metalico', '', '2025-11-13 20:23:39.287143', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.257608'),
(381, 'CABLE KLGO AUXILIAR 3.5 a 3.5 EN L COLORES 1MT', '', '2025-11-13 20:23:37.064696', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.270338'),
(382, 'Cable Samsung 2A Tipo C Carga Rápida Bolsa Azul', '', '2025-11-13 20:23:37.090163', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.283704'),
(383, 'CABLE USB Tipo C A Tipo C SAMSUNG CAJA', '', '2025-11-13 20:23:37.235385', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.296869'),
(384, 'Auricular Gamer Gm-06 PC PS4 Headphones', '', '2025-11-13 20:23:36.498688', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.308179'),
(385, 'AURICULAR GAMING CON CABLE', '', '2025-11-13 20:23:36.516032', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.320301'),
(386, 'AURICULAR EARPODS LIGHTNING', '', '2025-11-13 20:23:36.448284', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.332970'),
(387, 'AURICULAR EARPODS AUX', '', '2025-11-13 20:23:36.435713', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.345850'),
(388, 'AURICULAR EARPODS TIPO C', '', '2025-11-13 20:23:36.465666', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.358037'),
(389, 'JACK APPLE TIPO C A 3.5', '', '2025-11-13 20:23:37.910893', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.370540'),
(390, 'AURICULAR GALAXY BUDS 3', '', '2025-11-13 20:23:36.481056', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.382906'),
(391, 'AURICULAR CAJA BLANCA TIPO C', '', '2025-11-13 20:23:36.409966', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.395081'),
(392, 'AURICULAR LIGHTNING CAJA TRANSPARENTE', '', '2025-11-13 20:23:36.533140', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.406090'),
(393, 'PEGATINA SOPAPA PARA CELULAR CON ANILLO', '', '2025-11-13 20:23:38.723658', 1, NULL, 'ACTIVO', NULL, NULL, 1, '', NULL, '2025-11-13 17:13:06.419319'),
(394, 'ascasc', '', '2025-11-13 20:23:36.375690', 1, 1, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-13 20:14:45.409094'),
(395, 'iPhone 11', '', '2025-11-21 20:12:24.970167', 2, NULL, 'ACTIVO', NULL, NULL, 1, NULL, NULL, '2025-11-14 00:07:07.823241');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_productoimagen`
--

CREATE TABLE IF NOT EXISTS `inventario_productoimagen` (
  `id` bigint(20) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `orden` int(10) UNSIGNED NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `inventario_productoimagen`:
--   `producto_id`
--       `inventario_producto` -> `id`
--

--
-- Volcado de datos para la tabla `inventario_productoimagen`
--

INSERT INTO `inventario_productoimagen` (`id`, `imagen`, `orden`, `creado`, `actualizado`, `producto_id`) VALUES
(441, 'productos/330/6483aa6cc6c64c0c85bbb54a3595282b.png', 0, '2025-11-21 17:53:51.415513', '2025-11-21 17:53:51.416781', 330),
(442, 'productos/191/5637bd0999b845f59386b52a479a4bb5.png', 0, '2025-11-21 17:53:56.770875', '2025-11-21 17:53:56.772908', 191),
(443, 'productos/187/96e61f6dd13c4906813dbc13e8953545.webp', 0, '2025-11-21 17:53:58.040746', '2025-11-21 17:53:58.042074', 187),
(444, 'productos/379/2be10396422b47579f578662050cb393.png', 0, '2025-11-21 17:53:59.321563', '2025-11-21 17:53:59.324323', 379),
(445, 'productos/216/a20e100203874d8f8506f157962ab138.png', 0, '2025-11-21 17:54:08.596707', '2025-11-21 17:54:08.601429', 216),
(446, 'productos/366/3dd5e8c99c4d42cfa1925e4763327f2c.png', 0, '2025-11-21 17:54:14.292743', '2025-11-21 17:54:14.296379', 366),
(447, 'productos/290/5404c5084206404ab2041c0388d60e9a.webp', 0, '2025-11-21 17:54:23.532547', '2025-11-21 17:54:23.534544', 290),
(448, 'productos/256/1d5de51ef3e541de81b1581167a98523.webp', 0, '2025-11-21 17:54:45.773015', '2025-11-21 17:54:45.777019', 256),
(449, 'productos/372/2b92b8fbe2714857a26d28a16e12d9aa.webp', 0, '2025-11-21 17:54:47.009211', '2025-11-21 17:54:47.010524', 372),
(450, 'productos/391/b7a3a083312742b6a0b9bb9592e9ec32.png', 0, '2025-11-21 17:54:48.306930', '2025-11-21 17:54:48.308738', 391),
(451, 'productos/387/33ebb562563f4fcebb7678bbcc6eb94c.webp', 0, '2025-11-21 17:54:49.483456', '2025-11-21 17:54:49.485500', 387),
(452, 'productos/386/a8f9f1a4785d463ab41f8067c12e66ab.webp', 0, '2025-11-21 17:54:51.066815', '2025-11-21 17:54:51.067899', 386),
(453, 'productos/388/fe6f9dbc934747a79b21427b1c24584b.png', 0, '2025-11-21 17:54:52.361237', '2025-11-21 17:54:52.362560', 388),
(454, 'productos/390/160dce23c4344ba7bf9a77897bd239b9.webp', 0, '2025-11-21 17:54:53.540927', '2025-11-21 17:54:53.542342', 390),
(455, 'productos/384/760debd43c7749629c5906966b86fff8.webp', 0, '2025-11-21 17:54:54.721092', '2025-11-21 17:54:54.722413', 384),
(456, 'productos/385/ac18ef0e39c7471d8d2be08726ca52cf.webp', 0, '2025-11-21 17:54:56.455596', '2025-11-21 17:54:56.457720', 385),
(457, 'productos/392/01d78075c94342daa1c050f239a27dfd.webp', 0, '2025-11-21 17:54:57.843684', '2025-11-21 17:54:57.848719', 392),
(458, 'productos/258/68402730721649cb8e1fc23873c0cd04.webp', 0, '2025-11-21 17:54:59.037212', '2025-11-21 17:54:59.038418', 258),
(459, 'productos/257/1c3c35681af94bcf9aa566ac37256c89.webp', 0, '2025-11-21 17:55:00.225679', '2025-11-21 17:55:00.228124', 257),
(460, 'productos/288/ed117b4a82b5470f932bf5f62486a317.png', 0, '2025-11-21 17:55:05.709324', '2025-11-21 17:55:05.711635', 288),
(461, 'productos/210/2ce7e540c3514839aac3d5d970a5a775.webp', 0, '2025-11-21 17:55:19.725583', '2025-11-21 17:55:19.729064', 210),
(462, 'productos/287/32792164626f4150b6e157e3851cd09a.png', 0, '2025-11-21 17:55:34.003678', '2025-11-21 17:55:34.005676', 287),
(463, 'productos/343/886fc44d916f4e09b5900998e0056122.webp', 0, '2025-11-21 17:55:35.199676', '2025-11-21 17:55:35.201266', 343),
(464, 'productos/197/d425d1cde8d74bbe97f24ec0dfe296ec.png', 0, '2025-11-21 17:55:57.069836', '2025-11-21 17:55:57.072507', 197),
(465, 'productos/209/5715e9fc73134bc7869850824ecc65b0.webp', 0, '2025-11-21 17:56:18.625921', '2025-11-21 17:56:18.628088', 209),
(466, 'productos/382/b9d404e1e33e4472833bbf0e881aca81.png', 0, '2025-11-21 17:56:19.915658', '2025-11-21 17:56:19.916798', 382),
(467, 'productos/171/f383cb1327344da29447f171070fec71.webp', 0, '2025-11-21 17:56:37.452684', '2025-11-21 17:56:37.455139', 171),
(468, 'productos/213/2b4de9e1897d4e7b97a83d0abbbf8937.webp', 0, '2025-11-21 17:56:38.643606', '2025-11-21 17:56:38.645097', 213),
(469, 'productos/198/43329391c99848978acc90765d0dd60c.png', 0, '2025-11-21 17:56:49.069930', '2025-11-21 17:56:49.071168', 198),
(470, 'productos/195/d61198ef19204470b656496fae40246c.webp', 0, '2025-11-21 17:56:50.256997', '2025-11-21 17:56:50.257980', 195),
(471, 'productos/383/adc482cafbf349a3bd53856de4d5f650.png', 0, '2025-11-21 17:56:51.548341', '2025-11-21 17:56:51.549497', 383),
(472, 'productos/188/ea8516466b384d5386fb6348e1d8bf9d.webp', 0, '2025-11-21 17:57:01.237717', '2025-11-21 17:57:01.240197', 188),
(473, 'productos/168/107f89f473774b11b7c87b6fb08905d8.png', 0, '2025-11-21 17:57:15.691098', '2025-11-21 17:57:15.698290', 168),
(474, 'productos/203/955a9249ec3b4c2790d4eb2f81f5896a.webp', 0, '2025-11-21 17:57:27.453655', '2025-11-21 17:57:27.466300', 203),
(475, 'productos/186/1c71c03e02d54d03ba42507edb6e7531.png', 0, '2025-11-21 17:57:33.659444', '2025-11-21 17:57:33.663011', 186),
(476, 'productos/304/d5278b68312247eb9ba18b2ee398fbf5.webp', 0, '2025-11-21 17:57:39.175316', '2025-11-21 17:57:39.179051', 304),
(477, 'productos/201/184f65cde16141b6998df1838fe79087.webp', 0, '2025-11-21 17:57:53.114899', '2025-11-21 17:57:53.116938', 201),
(478, 'productos/302/7d21360f85334103885c8c27f30fa456.webp', 0, '2025-11-21 17:57:58.230307', '2025-11-21 17:57:58.231554', 302),
(479, 'productos/206/99ab15d62ba74a82ad0a4a8638aa0293.webp', 0, '2025-11-21 17:58:16.097434', '2025-11-21 17:58:16.100370', 206),
(480, 'productos/263/45b96abb21ba482fa578ebdf45c869f3.webp', 0, '2025-11-21 17:58:25.753427', '2025-11-21 17:58:25.755388', 263),
(481, 'productos/276/feba0245dd9848e086967ba89a2a9505.webp', 0, '2025-11-21 17:58:34.802892', '2025-11-21 17:58:34.841822', 276),
(482, 'productos/367/b563552b069d488a88d97158b9a775d0.png', 0, '2025-11-21 17:58:36.252861', '2025-11-21 17:58:36.253778', 367),
(483, 'productos/389/8d5d0134c5e44771bec87f4da37472e5.png', 0, '2025-11-21 17:58:57.791166', '2025-11-21 17:58:57.794090', 389),
(484, 'productos/377/cf225a1fd5594f1185c2252188977e94.webp', 0, '2025-11-21 17:59:14.969824', '2025-11-21 17:59:14.975120', 377),
(485, 'productos/248/a13e76688b734c8a8a38ea63111301ae.webp', 0, '2025-11-21 17:59:24.721787', '2025-11-21 17:59:24.723594', 248),
(486, 'productos/370/a8be24b70bdc439bad7659d5400c7de5.webp', 0, '2025-11-21 17:59:34.007046', '2025-11-21 17:59:34.008770', 370),
(487, 'productos/189/94957b9c916041fd8bfe9fc43ce3d22f.webp', 0, '2025-11-21 18:00:31.867669', '2025-11-21 18:00:31.878190', 189),
(488, 'productos/232/689766b7301f411c8a58646bdcd85fd3.webp', 0, '2025-11-21 18:00:57.954893', '2025-11-21 18:00:57.964392', 232),
(489, 'productos/348/5ddf4198dc314c5fb4171b3c89ce25ee.png', 0, '2025-11-21 18:01:54.684607', '2025-11-21 18:01:54.693752', 348),
(490, 'productos/346/0b15fa3f6f46420590a3b61f72e0c1c7.png', 0, '2025-11-21 18:01:56.250452', '2025-11-21 18:01:56.255866', 346),
(491, 'productos/268/95e32ed2f2374e27afeca0ae9fd7a801.webp', 0, '2025-11-21 18:01:57.457520', '2025-11-21 18:01:57.460206', 268),
(492, 'productos/393/a7e17b29ffe249b0ba2e97fa84094125.webp', 0, '2025-11-21 18:01:58.660274', '2025-11-21 18:01:58.661470', 393),
(493, 'productos/237/51a36c9b33894650b27047f6be83791b.webp', 0, '2025-11-21 18:02:12.078256', '2025-11-21 18:02:12.082092', 237),
(494, 'productos/301/5c37a8ce520546a7b3bc118a44e3f053.webp', 0, '2025-11-21 18:02:21.405355', '2025-11-21 18:02:21.408042', 301),
(495, 'productos/267/a1037b60111d47828e5b44818e20b5d8.webp', 0, '2025-11-21 18:02:26.739248', '2025-11-21 18:02:26.743110', 267),
(496, 'productos/255/0a78e0a3be2545ddb06dd90f80285bff.webp', 0, '2025-11-21 18:02:31.891768', '2025-11-21 18:02:31.894174', 255),
(497, 'productos/333/65b050a5829a4e88a94aa13d403ab12e.webp', 0, '2025-11-21 18:02:33.091180', '2025-11-21 18:02:33.092834', 333),
(498, 'productos/376/59dfc0914b83414f986d85971973e01f.webp', 0, '2025-11-21 18:02:34.281645', '2025-11-21 18:02:34.283398', 376),
(499, 'productos/283/9e5d3b66ada54af3958e3bfd90040c8d.webp', 0, '2025-11-21 18:02:44.189474', '2025-11-21 18:02:44.192831', 283),
(500, 'productos/217/b1d0a3ad53a8408cb503764c2f4fe516.webp', 0, '2025-11-21 18:02:58.504824', '2025-11-21 18:02:58.507162', 217),
(501, 'productos/223/25009b5fe12341b086607cdc5b6b7d9c.webp', 0, '2025-11-21 18:02:59.682273', '2025-11-21 18:02:59.685700', 223),
(502, 'productos/380/d44131b5d3d64537a26dbf3f7781416f.webp', 0, '2025-11-21 18:03:00.882128', '2025-11-21 18:03:00.884888', 380),
(503, 'productos/305/9a6c24fe3f8d42b09b80165a798e9661.webp', 0, '2025-11-21 18:03:02.089082', '2025-11-21 18:03:02.091251', 305),
(504, 'productos/329/1b073bfbc9e24f729cd9099f6babf523.webp', 0, '2025-11-21 18:03:15.303612', '2025-11-21 18:03:15.306674', 329),
(505, 'productos/378/d01116be1d1045179516df82ce0dbd2a.webp', 0, '2025-11-21 18:03:21.273814', '2025-11-21 18:03:21.275879', 378);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_productovariante`
--

CREATE TABLE IF NOT EXISTS `inventario_productovariante` (
  `id` bigint(20) NOT NULL,
  `nombre_variante` varchar(150) NOT NULL,
  `stock` int(10) UNSIGNED NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  `codigo_barras` varchar(100) DEFAULT NULL,
  `peso` decimal(10,2) NOT NULL,
  `sku` varchar(64) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `atributo_1` varchar(120) NOT NULL,
  `atributo_2` varchar(120) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `stock_actual` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 0,
  `qr_code` varchar(255) DEFAULT NULL
) ;

--
-- RELACIONES PARA LA TABLA `inventario_productovariante`:
--   `producto_id`
--       `inventario_producto` -> `id`
--

--
-- Volcado de datos para la tabla `inventario_productovariante`
--

INSERT INTO `inventario_productovariante` (`id`, `nombre_variante`, `stock`, `producto_id`, `codigo_barras`, `peso`, `sku`, `activo`, `actualizado`, `atributo_1`, `atributo_2`, `creado`, `stock_actual`, `stock_minimo`, `qr_code`) VALUES
(1, 'pata recta', 64, 2, NULL, 0.00, 'cargador-20w-pata-recta', 1, '2025-11-13 20:23:37.305696', 'pata recta', '', '2025-11-07 16:08:45.931486', 64, 0, NULL),
(4, 'iPhone 16 128GB Titanio Negro', 1, 11, '443395475901', 0.00, 'IPHONE-16-128GB-TITANIO-NEGRO', 1, '2025-11-13 16:21:56.571924', '128GB', 'Titanio Negro', '2025-11-13 03:44:05.956153', 0, 0, 'https://importstore.com/producto/IPHONE-16-128GB-TITANIO-NEGRO'),
(9, 'iPhone 15 Pro 64GB Titanio Natural', 1, 21, '805687808856', 0.00, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 1, '2025-11-13 18:59:41.084512', '64GB', 'Titanio Natural', '2025-11-13 15:28:11.020720', 0, 0, 'https://importstore.com/producto/IPHONE-15-PRO-64GB-TITANIO-NATURAL'),
(13, '', 12, 25, NULL, 0.00, 'fundas', 1, '2025-11-13 20:23:37.620359', '', '', '2025-11-13 16:51:03.147755', 12, 0, NULL),
(191, '', 91, 168, NULL, 0.00, 'CARGADOR-20W-TIPO-C', 1, '2025-11-13 20:23:37.317051', '', '', '2025-11-13 17:13:02.962262', 91, 0, NULL),
(192, ' (1)', 6, 168, NULL, 0.00, 'CARGADOR-20W-TIPO-C-1', 1, '2025-11-13 20:23:37.330054', '', '', '2025-11-13 17:13:02.988076', 6, 0, NULL),
(193, '', 0, 169, NULL, 0.00, 'PROYECTOR-HY300', 1, '2025-11-13 20:23:38.847714', '', '', '2025-11-13 17:13:03.003259', 0, 0, NULL),
(194, '', 53, 170, NULL, 0.00, 'CARGADOR-5W-USB-IPHONE', 1, '2025-11-13 20:23:37.353513', '', '', '2025-11-13 17:13:03.015959', 52, 0, NULL),
(195, '', 0, 171, NULL, 0.00, 'CABLE-USB-A-LIGHTNING-1MT', 1, '2025-11-13 20:23:37.168657', '', '', '2025-11-13 17:13:03.031144', 0, 0, NULL),
(196, '', 1, 172, NULL, 0.00, 'AURICULARES-F9-5', 1, '2025-11-13 20:23:36.659165', '', '', '2025-11-13 17:13:03.046349', 1, 0, NULL),
(197, '', 1, 173, NULL, 0.00, 'AURICULARES-VINCHA-P9', 1, '2025-11-13 20:23:36.915849', '', '', '2025-11-13 17:13:03.062052', 1, 0, NULL),
(198, ' (1)', 0, 173, NULL, 0.00, 'AURICULARES-VINCHA-P9-1', 1, '2025-11-13 20:23:36.926858', '', '', '2025-11-13 17:13:03.080123', 0, 0, NULL),
(199, '', 0, 174, NULL, 0.00, 'ADAPTADOR-5W-USB-IPHONE-CARGADORCABLE', 1, '2025-11-21 14:17:37.152278', '', '', '2025-11-13 17:13:03.095307', 0, 0, NULL),
(200, '', 1, 175, NULL, 0.00, 'CARGADOR-MAGSAFE-IPHONE', 1, '2025-11-13 20:23:37.374031', '', '', '2025-11-13 17:13:03.109479', 1, 0, NULL),
(201, '', 0, 176, NULL, 0.00, 'OFERTA-REFLECTOR-LUMINARIA-ALUMBRADO-PUBLICO-150W-REFLECTOR', 1, '2025-11-13 20:23:38.576219', '', '', '2025-11-13 17:13:03.124567', 0, 0, NULL),
(202, '', 0, 177, NULL, 0.00, 'CABLE-USB-C-A-C', 1, '2025-11-13 20:23:37.205081', '', '', '2025-11-13 17:13:03.139613', 0, 0, NULL),
(203, '', 10, 178, NULL, 0.00, 'MACBOOK-AIR-M2', 1, '2025-11-13 20:23:38.359793', '', '', '2025-11-13 17:13:03.154589', 10, 0, NULL),
(204, '', 13, 179, NULL, 0.00, 'MAGSAFE-BATTERY-PACK', 1, '2025-11-13 20:23:38.372793', '', '', '2025-11-13 17:13:03.167849', 13, 0, NULL),
(205, '', 0, 180, NULL, 0.00, 'AIRPODS-2-PRO-AAA', 1, '2025-11-13 20:23:36.333004', '', '', '2025-11-13 17:13:03.182803', 0, 0, NULL),
(206, '', 2, 181, NULL, 0.00, 'TV-BOX-PRO-5G-4K', 1, '2025-11-13 20:23:39.459312', '', '', '2025-11-13 17:13:03.195948', 2, 0, NULL),
(207, '', 0, 182, NULL, 0.00, 'AURICULARES-ULTRAPODS-MAX', 1, '2025-11-13 20:23:36.852952', '', '', '2025-11-13 17:13:03.208965', 0, 0, NULL),
(208, ' (1)', 0, 182, NULL, 0.00, 'AURICULARES-ULTRAPODS-MAX-1', 1, '2025-11-13 20:23:36.865979', '', '', '2025-11-13 17:13:03.227237', 0, 0, NULL),
(209, ' (2)', 0, 182, NULL, 0.00, 'AURICULARES-ULTRAPODS-MAX-2', 1, '2025-11-13 20:23:36.879992', '', '', '2025-11-13 17:13:03.246597', 0, 0, NULL),
(210, ' (3)', 0, 182, NULL, 0.00, 'AURICULARES-ULTRAPODS-MAX-3', 0, '2025-11-13 20:23:36.893641', '', '', '2025-11-13 17:13:03.268349', 0, 0, NULL),
(211, '', 0, 183, NULL, 0.00, 'VASO-TERMICO-STANLEY-CON-MANIJA-14-LITROS', 0, '2025-11-13 20:23:39.520088', '', '', '2025-11-13 17:13:03.283167', 0, 0, NULL),
(212, '', 8, 184, NULL, 0.00, 'CABLE-USB-A-IPHONE', 1, '2025-11-13 20:23:37.152840', '', '', '2025-11-13 17:13:03.296378', 8, 0, NULL),
(213, '', 1, 185, NULL, 0.00, 'CABLE-USB-A-MICRO-USB-MOTOROLA', 1, '2025-11-13 20:23:37.194471', '', '', '2025-11-13 17:13:03.312736', 1, 0, NULL),
(214, '', 0, 186, NULL, 0.00, 'CARGADOR-TIPO-C-31A-SAMSUNG', 1, '2025-11-13 20:23:37.394702', '', '', '2025-11-13 17:13:03.327479', 0, 0, NULL),
(215, '', 2, 187, NULL, 0.00, 'ADAPTADOR-AURICULAR-A-IPHONE', 1, '2025-11-13 20:23:36.138264', '', '', '2025-11-13 17:13:03.342494', 0, 0, NULL),
(216, '', 1, 188, NULL, 0.00, 'CALOVENTOR-PARA-AUTO', 1, '2025-11-13 20:23:37.284441', '', '', '2025-11-13 17:13:03.356505', 1, 0, NULL),
(217, '', 1, 189, NULL, 0.00, 'LUZ-LED-CON-PANEL-SOLAR-CON-FORMA-DE-COPOS', 1, '2025-11-13 20:23:38.347077', '', '', '2025-11-13 17:13:03.370804', 1, 0, NULL),
(218, '', 1, 190, NULL, 0.00, 'CASCO-REBATIBLE', 1, '2025-11-13 20:23:37.407817', '', '', '2025-11-13 17:13:03.383913', 1, 0, NULL),
(219, '', 0, 191, NULL, 0.00, 'ADAPTADOR-APPLE-20W-TIPO-C-ORIGINAL-APPLE', 1, '2025-11-21 14:17:37.150610', '', '', '2025-11-13 17:13:03.399118', 2, 0, NULL),
(220, '', 0, 192, NULL, 0.00, 'SMARTWATCH-ACCESORIOS', 1, '2025-11-13 20:23:39.136902', '', '', '2025-11-13 17:13:03.414510', 0, 0, NULL),
(221, '', 0, 193, NULL, 0.00, 'SMARTWATCH-7-MALLAS-AURICULARES', 1, '2025-11-13 20:23:39.164695', '', '', '2025-11-13 17:13:03.429326', 0, 0, NULL),
(222, '', 0, 194, NULL, 0.00, 'TERMO-500ML-STARRY-SKY', 1, '2025-11-13 20:23:39.327088', '', '', '2025-11-13 17:13:03.444638', 0, 0, NULL),
(223, ' (1)', 0, 194, NULL, 0.00, 'TERMO-500ML-STARRY-SKY-1', 1, '2025-11-13 20:23:39.340775', '', '', '2025-11-13 17:13:03.459884', 0, 0, NULL),
(224, ' (2)', 88, 194, NULL, 0.00, 'TERMO-500ML-STARRY-SKY-2', 1, '2025-11-13 20:23:39.356000', '', '', '2025-11-13 17:13:03.477895', 88, 0, NULL),
(225, '', 0, 195, NULL, 0.00, 'CABLE-USB-TIPO-C-A-LIGHTNING-1MT', 1, '2025-11-13 20:23:37.227898', '', '', '2025-11-13 17:13:03.492067', 0, 0, NULL),
(226, '', 8, 196, NULL, 0.00, 'AURICULARES-M10', 1, '2025-11-13 20:23:36.803270', '', '', '2025-11-13 17:13:03.507434', 8, 0, NULL),
(227, '', 1, 197, NULL, 0.00, 'CABEZAL-MASUYA-TIPO-C-64W', 1, '2025-11-13 20:23:36.972102', '', '', '2025-11-13 17:13:03.522131', 1, 0, NULL),
(228, '', 565, 198, NULL, 0.00, 'CABLE-USB-TIPO-C-A-C-IPHONE', 1, '2025-11-13 20:23:37.216897', '', '', '2025-11-13 17:13:03.533323', 565, 0, NULL),
(229, '', 0, 199, NULL, 0.00, 'FUNDA-SILICONE-CASE-IPHONE-CONSULTAR-MODELOS', 1, '2025-11-13 20:23:37.591754', '', '', '2025-11-13 17:13:03.547259', 0, 0, NULL),
(230, '', 0, 200, NULL, 0.00, 'FUNDA-TRANSPARENTE-MAGSAFE', 0, '2025-11-13 20:23:37.605572', '', '', '2025-11-13 17:13:03.561888', 0, 0, NULL),
(231, '', 0, 201, NULL, 0.00, 'EARPODS-LIGHTNING', 1, '2025-11-13 20:23:37.470527', '', '', '2025-11-13 17:13:03.574897', 0, 0, NULL),
(232, '', 3, 202, NULL, 0.00, 'ADAPTADOR-SAMSUNG-25W', 1, '2025-11-13 20:23:36.253955', '', '', '2025-11-13 17:13:03.589997', 3, 0, NULL),
(233, '', 0, 203, NULL, 0.00, 'CARGADOR-CARGA-RAPIDA-DITRON-31A-CON-CABLE', 1, '2025-11-13 20:23:37.362020', '', '', '2025-11-13 17:13:03.602183', 0, 0, NULL),
(234, '', 0, 204, NULL, 0.00, 'CABLE-USB-A-C-SAMSUNG', 1, '2025-11-13 20:23:37.140498', '', '', '2025-11-13 17:13:03.615886', 0, 0, NULL),
(235, '', 29, 205, NULL, 0.00, 'CABLE-C-A-C-MOTOROLA', 1, '2025-11-13 20:23:37.004228', '', '', '2025-11-13 17:13:03.630829', 29, 0, NULL),
(236, '', 8, 206, NULL, 0.00, 'FUNDA-RIGIDA-TRANSPARENTE', 1, '2025-11-13 20:23:37.563292', '', '', '2025-11-13 17:13:03.644841', 8, 0, NULL),
(237, '', 0, 207, NULL, 0.00, 'CABLE-AUX-A-2RCA', 1, '2025-11-13 20:23:36.983279', '', '', '2025-11-13 17:13:03.658013', 0, 0, NULL),
(238, '', 0, 208, NULL, 0.00, 'FUNDA-AIRPODS-PRO-2-LISA', 1, '2025-11-13 20:23:37.536638', '', '', '2025-11-13 17:13:03.671529', 0, 0, NULL),
(239, '', 3, 209, NULL, 0.00, 'CABLE-LIGHTNING-A-USB-IPHONE-2MT', 1, '2025-11-13 20:23:37.077673', '', '', '2025-11-13 17:13:03.685015', 2, 0, NULL),
(240, '', 0, 210, NULL, 0.00, 'AURICULARES-GAMER-PARA-XBOX-360', 1, '2025-11-13 20:23:36.687238', '', '', '2025-11-13 17:13:03.698180', 0, 0, NULL),
(241, '', 0, 211, NULL, 0.00, 'PARLANTE-PORTABLE-SPEAKER-HF-323-BLUETOOTH', 0, '2025-11-13 20:23:38.666707', '', '', '2025-11-13 17:13:03.711309', 0, 0, NULL),
(242, '', 1, 212, NULL, 0.00, 'PARLANTE-PORTABLE-SPEAKER-BLUETOOTH', 0, '2025-11-13 20:23:38.656191', '', '', '2025-11-13 17:13:03.725619', 1, 0, NULL),
(243, '', 0, 213, NULL, 0.00, 'CABLE-USB-A-LIGHTNING-2MT-BELKIN', 1, '2025-11-13 20:23:37.184961', '', '', '2025-11-13 17:13:03.738621', 0, 0, NULL),
(244, '', 0, 214, NULL, 0.00, 'CABLE-USB-A-C-2MT-BELKIN', 1, '2025-11-13 20:23:37.117300', '', '', '2025-11-13 17:13:03.752634', 0, 0, NULL),
(245, '', 0, 215, NULL, 0.00, 'ADAPTADOR-MOSQUITO-DE-PARED', 1, '2025-11-13 20:23:36.222581', '', '', '2025-11-13 17:13:03.765983', 0, 0, NULL),
(246, '', 4, 216, NULL, 0.00, 'ADAPTADOR-MOTOROLA-CABLE-TIPO-C', 1, '2025-11-13 20:23:36.239111', '', '', '2025-11-13 17:13:03.781903', 2, 0, NULL),
(247, '', 0, 217, NULL, 0.00, 'SOPORTE-ADHESIVO-PARA-PARED', 1, '2025-11-13 20:23:39.266611', '', '', '2025-11-13 17:13:03.793071', 0, 0, NULL),
(248, '', 0, 218, NULL, 0.00, 'AURICULARES-AKG-SAMSUNG', 1, '2025-11-13 20:23:36.593269', '', '', '2025-11-13 17:13:03.806077', 0, 0, NULL),
(249, ' (1)', 9, 218, NULL, 0.00, 'AURICULARES-AKG-SAMSUNG-1', 1, '2025-11-13 20:23:36.611910', '', '', '2025-11-13 17:13:03.822529', 9, 0, NULL),
(250, '', 6, 219, NULL, 0.00, 'ADAPTADOR-JACK-A-USB-C-SAMSUNG', 1, '2025-11-13 20:23:36.182095', '', '', '2025-11-13 17:13:03.836838', 6, 0, NULL),
(251, '', 0, 220, NULL, 0.00, 'ADAPTADOR-LIGHTNING-SPLITTER', 0, '2025-11-13 20:23:36.205146', '', '', '2025-11-13 17:13:03.849688', 0, 0, NULL),
(252, '', 2, 221, NULL, 0.00, 'CARGADOR-35W-APPLE-2-ENTRADAS-USB-C', 1, '2025-11-13 20:23:37.341222', '', '', '2025-11-13 17:13:03.862426', 2, 0, NULL),
(253, '', 8, 222, NULL, 0.00, 'IPHONE-WALLET-AAA', 1, '2025-11-13 20:23:37.904381', '', '', '2025-11-13 17:13:03.874065', 8, 0, NULL),
(254, '', 3, 223, NULL, 0.00, 'SOPORTE-CELULAR-CON-SOPAPA-PARA-VIDRIOS-Y-ESPEJO', 1, '2025-11-13 20:23:39.277611', '', '', '2025-11-13 17:13:03.887258', 3, 0, NULL),
(255, '', 1, 224, NULL, 0.00, 'FUNDAS-VARIAS', 1, '2025-11-13 20:23:37.758059', '', '', '2025-11-13 17:13:03.900448', 1, 0, NULL),
(256, ' (1)', 1, 224, NULL, 0.00, 'FUNDAS-VARIAS-1', 1, '2025-11-13 20:23:37.775064', '', '', '2025-11-13 17:13:03.920299', 1, 0, NULL),
(257, ' (2)', 2, 224, NULL, 0.00, 'FUNDAS-VARIAS-2', 1, '2025-11-13 20:23:37.793984', '', '', '2025-11-13 17:13:03.936240', 2, 0, NULL),
(258, ' (3)', 1, 224, NULL, 0.00, 'FUNDAS-VARIAS-3', 1, '2025-11-13 20:23:37.816226', '', '', '2025-11-13 17:13:03.955811', 1, 0, NULL),
(259, ' (4)', 1, 224, NULL, 0.00, 'FUNDAS-VARIAS-4', 1, '2025-11-13 20:23:37.836418', '', '', '2025-11-13 17:13:03.981101', 1, 0, NULL),
(260, ' (5)', 1, 224, NULL, 0.00, 'FUNDAS-VARIAS-5', 1, '2025-11-13 20:23:37.857651', '', '', '2025-11-13 17:13:04.006248', 1, 0, NULL),
(261, '', 19, 225, NULL, 0.00, 'MINI-PROYECTOR-ASTRONAUTA', 1, '2025-11-13 20:23:38.492292', '', '', '2025-11-13 17:13:04.019714', 19, 0, NULL),
(262, '', 0, 226, NULL, 0.00, 'DISPENSER-DE-AGUA-ELECTRICO', 1, '2025-11-13 20:23:37.443969', '', '', '2025-11-13 17:13:04.031457', 0, 0, NULL),
(263, '', 1, 227, NULL, 0.00, 'TIRA-LED-RGB-BLUETOOTH-5MT', 1, '2025-11-13 20:23:39.409611', '', '', '2025-11-13 17:13:04.044718', 1, 0, NULL),
(264, '', 2, 228, NULL, 0.00, 'MAQUINA-MINI-DONAS', 1, '2025-11-13 20:23:38.409024', '', '', '2025-11-13 17:13:04.057731', 2, 0, NULL),
(265, '', 1, 229, NULL, 0.00, 'MOCHILAS', 1, '2025-11-13 20:23:38.531961', '', '', '2025-11-13 17:13:04.071451', 1, 0, NULL),
(266, '', 2, 230, NULL, 0.00, 'LAMPARA-DE-CRISTAL-LED', 1, '2025-11-13 20:23:38.079006', '', '', '2025-11-13 17:13:04.085921', 2, 0, NULL),
(267, '', 2, 231, NULL, 0.00, 'AURICULARES-Y-09', 1, '2025-11-13 20:23:36.951976', '', '', '2025-11-13 17:13:04.101070', 2, 0, NULL),
(268, '', 1, 232, NULL, 0.00, 'MINI-LINTERNA-LED-CON-ENCENDEDOR-M8', 1, '2025-11-13 20:23:38.456113', '', '', '2025-11-13 17:13:04.114533', 1, 0, NULL),
(269, '', 2, 233, NULL, 0.00, 'MINI-LLAVERO-LINTERNA-LED', 1, '2025-11-13 20:23:38.469627', '', '', '2025-11-13 17:13:04.127349', 2, 0, NULL),
(270, '', 4, 234, NULL, 0.00, 'LAVA-COPAS', 1, '2025-11-13 20:23:38.299723', '', '', '2025-11-13 17:13:04.142327', 4, 0, NULL),
(271, '', 2, 235, NULL, 0.00, 'NEBLINERO-LED', 1, '2025-11-13 20:23:38.566219', '', '', '2025-11-13 17:13:04.156337', 2, 0, NULL),
(272, '', 1, 236, NULL, 0.00, 'LAMPARA-DE-TUBO-LED-USB', 1, '2025-11-13 20:23:38.105983', '', '', '2025-11-13 17:13:04.171129', 1, 0, NULL),
(273, '', 7, 237, NULL, 0.00, 'PINZA-SOPORTE-PARA-AUTO', 1, '2025-11-13 20:23:38.773864', '', '', '2025-11-13 17:13:04.185016', 7, 0, NULL),
(274, '', 3, 238, NULL, 0.00, 'TRIPODE-21MT', 1, '2025-11-13 20:23:39.435981', '', '', '2025-11-13 17:13:04.198200', 3, 0, NULL),
(275, '', 13, 239, NULL, 0.00, 'CAMARA-DE-VIGILANCIA-IP-INTELIGENTE-2', 1, '2025-11-13 20:23:37.293948', '', '', '2025-11-13 17:13:04.216220', 13, 0, NULL),
(276, '', 0, 240, NULL, 0.00, 'REPETIDOR-AMPLIFICADOR-WIFI-SENAL-300-MBP', 0, '2025-11-13 20:23:39.063019', '', '', '2025-11-13 17:13:04.231364', 0, 0, NULL),
(277, '', 9, 241, NULL, 0.00, 'JOYSTICK-INALAMBRICO-PS4', 1, '2025-11-13 20:23:37.929003', '', '', '2025-11-13 17:13:04.243275', 9, 0, NULL),
(278, '', 4, 242, NULL, 0.00, 'MINI-PLUG-A-RCA', 1, '2025-11-13 20:23:38.480632', '', '', '2025-11-13 17:13:04.257279', 4, 0, NULL),
(279, '', 0, 243, NULL, 0.00, 'JOYSTICK-PS3-NEGRO', 1, '2025-11-13 20:23:37.942743', '', '', '2025-11-13 17:13:04.269468', 0, 0, NULL),
(280, '', 0, 244, NULL, 0.00, 'MINI-TECLADO-SMART', 0, '2025-11-13 20:23:38.506292', '', '', '2025-11-13 17:13:04.283027', 0, 0, NULL),
(281, '', 9, 245, NULL, 0.00, 'AURICULARES-ROYALCELL', 1, '2025-11-13 20:23:36.815118', '', '', '2025-11-13 17:13:04.296177', 9, 0, NULL),
(282, '', 3, 246, NULL, 0.00, 'CABLE-C-A-C-APPLE-MALLADO-1MT', 1, '2025-11-13 20:23:36.992787', '', '', '2025-11-13 17:13:04.311679', 3, 0, NULL),
(283, '', 5, 247, NULL, 0.00, 'AURICULARES-BLUETOOTH-M90-MAX', 1, '2025-11-13 20:23:36.644310', '', '', '2025-11-13 17:13:04.326452', 5, 0, NULL),
(284, '', 0, 248, NULL, 0.00, 'LAMPARA-DE-MESA-CON-CARGADOR-INALAMBRICO-DE-CELULAR', 1, '2025-11-13 20:23:38.091463', '', '', '2025-11-13 17:13:04.338453', 0, 0, NULL),
(285, '', 0, 249, NULL, 0.00, 'JOYSTICK-PS4-EDICION-INTER-MIAMI-MESSI', 1, '2025-11-13 20:23:37.955128', '', '', '2025-11-13 17:13:04.353274', 0, 0, NULL),
(286, ' (1)', 0, 249, NULL, 0.00, 'JOYSTICK-PS4-EDICION-INTER-MIAMI-MESSI-1', 1, '2025-11-13 20:23:37.969944', '', '', '2025-11-13 17:13:04.370555', 0, 0, NULL),
(287, ' (2)', 0, 249, NULL, 0.00, 'JOYSTICK-PS4-EDICION-INTER-MIAMI-MESSI-2', 0, '2025-11-13 20:23:37.985299', '', '', '2025-11-13 17:13:04.388574', 0, 0, NULL),
(288, '', 5, 250, NULL, 0.00, 'EARPODS-35MM', 1, '2025-11-13 20:23:37.457203', '', '', '2025-11-13 17:13:04.398709', 5, 0, NULL),
(289, '', 12, 251, NULL, 0.00, 'PENDRIVE-64GB-SANDISK', 1, '2025-11-13 20:23:38.739329', '', '', '2025-11-13 17:13:04.408292', 12, 0, NULL),
(290, '', 3, 252, NULL, 0.00, 'MOUSE-INALAMBRICO-A-PILAS', 1, '2025-11-13 20:23:38.554470', '', '', '2025-11-13 17:13:04.418393', 3, 0, NULL),
(291, '', 0, 253, NULL, 0.00, 'REFLECTOR-LED-RGB', 0, '2025-11-13 20:23:38.879491', '', '', '2025-11-13 17:13:04.428543', 0, 0, NULL),
(292, '', 0, 254, NULL, 0.00, 'XIAOMI-A3X-64GB-3GB-RAM', 0, '2025-11-13 20:23:39.542844', '', '', '2025-11-13 17:13:04.438543', 0, 0, NULL),
(293, '', 2, 255, NULL, 0.00, 'SAMSUNG-GALAXY-A05-64GB', 1, '2025-11-13 20:23:39.075024', '', '', '2025-11-13 17:13:04.449587', 2, 0, NULL),
(294, '', 0, 256, NULL, 0.00, 'AURICULAR-BT-MUSIC-LIFE', 1, '2025-11-13 20:23:36.391726', '', '', '2025-11-13 17:13:04.459844', 0, 0, NULL),
(295, '', 5, 257, NULL, 0.00, 'AURICULAR-SPORT-BT-QX15', 1, '2025-11-13 20:23:36.574165', '', '', '2025-11-13 17:13:04.468355', 5, 0, NULL),
(296, '', 2, 258, NULL, 0.00, 'AURICULAR-M19', 1, '2025-11-13 20:23:36.556492', '', '', '2025-11-13 17:13:04.479244', 2, 0, NULL),
(297, '', 0, 259, NULL, 0.00, 'MINI-IMPRESORA-PORTATIL', 1, '2025-11-13 20:23:38.519955', '', '', '2025-11-13 17:13:04.489241', 0, 0, NULL),
(298, '', 7, 260, NULL, 0.00, 'FUNDAS-MAGSAFE-ELECTRO', 1, '2025-11-13 20:23:37.685830', '', '', '2025-11-13 17:13:04.498385', 7, 0, NULL),
(299, ' (1)', 2, 260, NULL, 0.00, 'FUNDAS-MAGSAFE-ELECTRO-1', 1, '2025-11-13 20:23:37.702626', '', '', '2025-11-13 17:13:04.511250', 2, 0, NULL),
(300, ' (2)', 2, 260, NULL, 0.00, 'FUNDAS-MAGSAFE-ELECTRO-2', 1, '2025-11-13 20:23:37.721857', '', '', '2025-11-13 17:13:04.525548', 2, 0, NULL),
(301, ' (3)', 0, 260, NULL, 0.00, 'FUNDAS-MAGSAFE-ELECTRO-3', 0, '2025-11-13 20:23:37.741941', '', '', '2025-11-13 17:13:04.541819', 0, 0, NULL),
(302, '', 3, 261, NULL, 0.00, 'FUNDA-MAGSAFE-FLEX-IPHONE-13-PRO', 1, '2025-11-13 20:23:37.550398', '', '', '2025-11-13 17:13:04.552533', 3, 0, NULL),
(303, '', 3, 262, NULL, 0.00, 'FUNDA-MAGSAFE-SOFT-IPHONE-12-12-PRO', 1, '2025-11-13 20:23:37.563292', '', '', '2025-11-13 17:13:04.562720', 3, 0, NULL),
(304, '', 2, 263, NULL, 0.00, 'FUNDAS-CON-DISIPACION-DE-CALOR-IPHONE-12', 1, '2025-11-13 20:23:37.635174', '', '', '2025-11-13 17:13:04.571353', 2, 0, NULL),
(305, ' (1)', 1, 263, NULL, 0.00, 'FUNDAS-CON-DISIPACION-DE-CALOR-IPHONE-12-1', 1, '2025-11-13 20:23:37.648495', '', '', '2025-11-13 17:13:04.584368', 1, 0, NULL),
(306, ' (2)', 0, 263, NULL, 0.00, 'FUNDAS-CON-DISIPACION-DE-CALOR-IPHONE-12-2', 1, '2025-11-13 20:23:37.668707', '', '', '2025-11-13 17:13:04.599062', 0, 0, NULL),
(307, '', 0, 264, NULL, 0.00, 'CABLE-USB-A-C-MOTOROLA', 1, '2025-11-13 20:23:37.129303', '', '', '2025-11-13 17:13:04.609474', 0, 0, NULL),
(308, '', 0, 265, NULL, 0.00, 'AURICULARES-INPODS-12', 1, '2025-11-13 20:23:36.699083', '', '', '2025-11-13 17:13:04.620593', 0, 0, NULL),
(309, ' (1)', 1, 265, NULL, 0.00, 'AURICULARES-INPODS-12-1', 1, '2025-11-13 20:23:36.710804', '', '', '2025-11-13 17:13:04.633754', 1, 0, NULL),
(310, ' (2)', 1, 265, NULL, 0.00, 'AURICULARES-INPODS-12-2', 1, '2025-11-13 20:23:36.725043', '', '', '2025-11-13 17:13:04.649659', 1, 0, NULL),
(311, ' (3)', 2, 265, NULL, 0.00, 'AURICULARES-INPODS-12-3', 1, '2025-11-13 20:23:36.739110', '', '', '2025-11-13 17:13:04.664909', 2, 0, NULL),
(312, ' (4)', 0, 265, NULL, 0.00, 'AURICULARES-INPODS-12-4', 1, '2025-11-13 20:23:36.756463', '', '', '2025-11-13 17:13:04.681298', 0, 0, NULL),
(313, ' (5)', 0, 265, NULL, 0.00, 'AURICULARES-INPODS-12-5', 1, '2025-11-13 20:23:36.774191', '', '', '2025-11-13 17:13:04.702397', 0, 0, NULL),
(314, ' (6)', 1, 265, NULL, 0.00, 'AURICULARES-INPODS-12-6', 1, '2025-11-13 20:23:36.791865', '', '', '2025-11-13 17:13:04.724422', 1, 0, NULL),
(315, '', 0, 266, NULL, 0.00, 'KIT-MOUSE-Y-TECLADO-ULTRA-FIT', 1, '2025-11-13 20:23:38.022098', '', '', '2025-11-13 17:13:04.733147', 0, 0, NULL),
(316, ' (1)', 0, 266, NULL, 0.00, 'KIT-MOUSE-Y-TECLADO-ULTRA-FIT-1', 1, '2025-11-13 20:23:38.036323', '', '', '2025-11-13 17:13:04.746124', 0, 0, NULL),
(317, ' (2)', 3, 266, NULL, 0.00, 'KIT-MOUSE-Y-TECLADO-ULTRA-FIT-2', 1, '2025-11-13 20:23:38.051234', '', '', '2025-11-13 17:13:04.759278', 3, 0, NULL),
(318, ' (3)', 0, 266, NULL, 0.00, 'KIT-MOUSE-Y-TECLADO-ULTRA-FIT-3', 1, '2025-11-13 20:23:38.067003', '', '', '2025-11-13 17:13:04.775371', 0, 0, NULL),
(319, '', 3, 267, NULL, 0.00, 'RECEPTOR-BLUETOOTH-AUXILIAR-PARA-AUTO', 1, '2025-11-13 20:23:38.861486', '', '', '2025-11-13 17:13:04.785369', 3, 0, NULL),
(320, '', 1, 268, NULL, 0.00, 'PAVA-ELECTRICA-PARA-AUTO-500ML', 1, '2025-11-13 20:23:38.713852', '', '', '2025-11-13 17:13:04.796294', 1, 0, NULL),
(321, '', 1, 269, NULL, 0.00, 'CALCULADORA-CIENTIFICA-COLORES', 1, '2025-11-13 20:23:37.250157', '', '', '2025-11-13 17:13:04.804299', 1, 0, NULL),
(322, ' (1)', 0, 269, NULL, 0.00, 'CALCULADORA-CIENTIFICA-COLORES-1', 0, '2025-11-13 20:23:37.260665', '', '', '2025-11-13 17:13:04.818331', 0, 0, NULL),
(323, '', 1, 270, NULL, 0.00, 'MOTO-E14', 1, '2025-11-13 20:23:38.542472', '', '', '2025-11-13 17:13:04.830106', 1, 0, NULL),
(324, '', 1, 271, NULL, 0.00, 'LATTAFA-AJWAD-60ML-FEMENINO', 1, '2025-11-13 20:23:38.158420', '', '', '2025-11-13 17:13:04.839105', 1, 0, NULL),
(325, '', 0, 272, NULL, 0.00, 'RELOJ-CURREN-MODELO-8346', 0, '2025-11-13 20:23:38.929154', '', '', '2025-11-13 17:13:04.853403', 0, 0, NULL),
(326, '', 1, 273, NULL, 0.00, 'VASO-STARBUCKS', 1, '2025-11-13 20:23:39.495949', '', '', '2025-11-13 17:13:04.864108', 1, 0, NULL),
(327, '', 0, 274, NULL, 0.00, 'MINI-LECTOR-DE-MEMORIA-SD', 0, '2025-11-13 20:23:38.444927', '', '', '2025-11-13 17:13:04.874455', 0, 0, NULL),
(328, '', 5, 275, NULL, 0.00, 'LAMPARA-LED-USB-BAJO-MESADA', 1, '2025-11-13 20:23:38.129292', '', '', '2025-11-13 17:13:04.884279', 5, 0, NULL),
(329, '', 0, 276, NULL, 0.00, 'HOLDER-PARA-AUTO-SOFT-TUBE', 1, '2025-11-13 20:23:37.868878', '', '', '2025-11-13 17:13:04.894449', 0, 0, NULL),
(330, '', 0, 277, NULL, 0.00, 'TERMO-VACUUM-STANLEY-1L', 1, '2025-11-13 20:23:39.368793', '', '', '2025-11-13 17:13:04.902453', 0, 0, NULL),
(331, ' (1)', 0, 277, NULL, 0.00, 'TERMO-VACUUM-STANLEY-1L-1', 1, '2025-11-13 20:23:39.382278', '', '', '2025-11-13 17:13:04.916289', 0, 0, NULL),
(332, ' (2)', 25, 277, NULL, 0.00, 'TERMO-VACUUM-STANLEY-1L-2', 1, '2025-11-13 20:23:39.395793', '', '', '2025-11-13 17:13:04.929055', 25, 0, NULL),
(333, '', 0, 278, NULL, 0.00, 'ADAPTADOR-SAMSUNG-45W', 0, '2025-11-13 20:23:36.269514', '', '', '2025-11-13 17:13:04.937055', 0, 0, NULL),
(334, '', 0, 279, NULL, 0.00, 'PROTECTOR-DE-CABLE-ESPIRAL-DE-SILICONA-FLEXIBLE', 0, '2025-11-13 20:23:38.786879', '', '', '2025-11-13 17:13:04.947636', 0, 0, NULL),
(335, '', 108, 280, NULL, 0.00, 'CALCULADORA-CIENTIFICA-KENKO', 1, '2025-11-13 20:23:37.273233', '', '', '2025-11-13 17:13:04.957639', 108, 0, NULL),
(336, '', 0, 281, NULL, 0.00, 'ADAPTADOR-20W-CABLE-C-A-LIGHTNING', 0, '2025-11-13 20:23:36.056120', '', '', '2025-11-13 17:13:04.967296', 0, 0, NULL),
(337, '', 2, 282, NULL, 0.00, 'VASO-TERMICO-STANLEY-BI-COLOR', 1, '2025-11-13 20:23:39.508361', '', '', '2025-11-13 17:13:04.978460', 2, 0, NULL),
(338, '', 3, 283, NULL, 0.00, 'SMARTWATCH-CON-PARLANTE-Y-ACCESORIOS', 1, '2025-11-13 20:23:39.178454', '', '', '2025-11-13 17:13:04.988459', 3, 0, NULL),
(339, '', 1, 284, NULL, 0.00, 'ESFERA-DE-LUZ-GRANDE', 0, '2025-11-13 20:23:37.483766', '', '', '2025-11-13 17:13:04.997599', 1, 0, NULL),
(340, ' (1)', 3, 284, NULL, 0.00, 'ESFERA-DE-LUZ-GRANDE-1', 1, '2025-11-13 20:23:37.497280', '', '', '2025-11-13 17:13:05.010637', 3, 0, NULL),
(341, '', 0, 285, NULL, 0.00, 'PARLANTE-BLUETOOTH-CON-MICROFONO-KARAOKE', 0, '2025-11-13 20:23:38.611318', '', '', '2025-11-13 17:13:05.021148', 0, 0, NULL),
(342, '', 0, 286, NULL, 0.00, 'ZTE-BLADE-A35-64-GB-6-GB', 1, '2025-11-13 20:23:39.590213', '', '', '2025-11-13 17:13:05.031936', 0, 0, NULL),
(343, '', 0, 287, NULL, 0.00, 'AURICULARES-TIPO-JBL-VINCHA-BLUETOOTH', 1, '2025-11-13 20:23:36.828117', '', '', '2025-11-13 17:13:05.042952', 0, 0, NULL),
(344, '', 1, 288, NULL, 0.00, 'AURICULARES-ANC-ENC-PURE-BASS-BT-ZERO-CABLESCOLOR-NEGRO', 1, '2025-11-13 20:23:36.629164', '', '', '2025-11-13 17:13:05.052966', 1, 0, NULL),
(345, '', 2, 289, NULL, 0.00, 'AIRPODS-4AAA', 1, '2025-11-13 20:23:36.345515', '', '', '2025-11-13 17:13:05.063616', 2, 0, NULL),
(346, '', 0, 290, NULL, 0.00, 'AIR-PODS-CON-PANTALLA', 1, '2025-11-13 20:23:36.320857', '', '', '2025-11-13 17:13:05.073620', 0, 0, NULL),
(347, '', 0, 291, NULL, 0.00, 'LUCES-NEON-LED-5-MT', 1, '2025-11-13 20:23:38.321554', '', '', '2025-11-13 17:13:05.084166', 0, 0, NULL),
(348, ' (1)', 0, 291, NULL, 0.00, 'LUCES-NEON-LED-5-MT-1', 0, '2025-11-13 20:23:38.334560', '', '', '2025-11-13 17:13:05.097333', 0, 0, NULL),
(349, '', 0, 292, NULL, 0.00, 'LUCES-LED-FLEXIBLKES-1-MT-RGB', 0, '2025-11-13 20:23:38.309229', '', '', '2025-11-13 17:13:05.108564', 0, 0, NULL),
(350, '', 0, 293, NULL, 0.00, 'SOPORTE-VIDEO-MAKING-LED-MICROPHONE', 0, '2025-11-13 20:23:39.316076', '', '', '2025-11-13 17:13:05.119698', 0, 0, NULL),
(351, '', 0, 294, NULL, 0.00, 'SMARTWACHT-T9-CON-CAJA', 0, '2025-11-13 20:23:39.123902', '', '', '2025-11-13 17:13:05.130021', 0, 0, NULL),
(352, '', 0, 295, NULL, 0.00, 'SMARTWACH-A100-7-MALLAS', 0, '2025-11-13 20:23:39.110376', '', '', '2025-11-13 17:13:05.140021', 0, 0, NULL),
(353, '', 0, 296, NULL, 0.00, 'SMARTWATCH-S300-MAX-7-MALLAS-AURICULARES-BLUETOOTH', 0, '2025-11-13 20:23:39.203957', '', '', '2025-11-13 17:13:05.150643', 0, 0, NULL),
(354, '', 0, 297, NULL, 0.00, 'SMARTWATCH-AURICULARES-VINCHA-P9-Y-7-MALLAS', 0, '2025-11-13 20:23:39.148415', '', '', '2025-11-13 17:13:05.161635', 0, 0, NULL),
(355, '', 4, 298, NULL, 0.00, 'KIT-DE-HERRAMIENTAS', 1, '2025-11-13 20:23:37.996826', '', '', '2025-11-13 17:13:05.169709', 4, 0, NULL),
(356, '', 0, 299, NULL, 0.00, 'PROYECTOR-ASTRONAUTA-CON-PARLANTE', 0, '2025-11-13 20:23:38.799396', '', '', '2025-11-13 17:13:05.180015', 0, 0, NULL),
(357, '', 1, 300, NULL, 0.00, 'PROYECTOR-ASTRONAUTA-CHICOCAJA-AZUL', 1, '2025-11-13 20:23:38.822900', '', '', '2025-11-13 17:13:05.188015', 1, 0, NULL),
(358, '', 1, 301, NULL, 0.00, 'PROYECTOR-CON-CONSOLA-DE-VIDEOJUEGOS', 1, '2025-11-13 20:23:38.836189', '', '', '2025-11-13 17:13:05.198261', 1, 0, NULL),
(359, '', 1, 302, NULL, 0.00, 'FOCO-PARLANTE-PARA-FIESTA', 1, '2025-11-13 20:23:37.510076', '', '', '2025-11-13 17:13:05.207598', 1, 0, NULL),
(360, '', 0, 303, NULL, 0.00, 'PARLANTE-BLUETOOTH-HF3223', 0, '2025-11-13 20:23:38.622313', '', '', '2025-11-13 17:13:05.218685', 0, 0, NULL),
(361, '', 2, 304, NULL, 0.00, 'CONSOLA-GAMEPAD-CON-PANTALLA', 1, '2025-11-13 20:23:37.420208', '', '', '2025-11-13 17:13:05.228859', 2, 0, NULL),
(362, '', 7, 305, NULL, 0.00, 'SOPORTE-PARA-TABLET', 1, '2025-11-13 20:23:39.303297', '', '', '2025-11-13 17:13:05.236859', 7, 0, NULL),
(363, '', 0, 306, NULL, 0.00, 'MALLAS-VARIAS_X000D__X000D__X000D__X000D__X000D__X000D__X000', 0, '2025-11-13 20:23:38.395513', '', '', '2025-11-13 17:13:05.247827', 0, 0, NULL),
(364, '', 1, 307, NULL, 0.00, 'SMARTWATCH-T9-OUTLET', 1, '2025-11-13 20:23:39.216950', '', '', '2025-11-13 17:13:05.256826', 1, 0, NULL),
(365, '', 1, 308, NULL, 0.00, 'PARLANTE-LAMPARA-PORTABLE', 1, '2025-11-13 20:23:38.643071', '', '', '2025-11-13 17:13:05.267501', 1, 0, NULL),
(366, '', 4, 309, NULL, 0.00, 'HUMIDIFICADOR-DIFUSOR-AROMATIZADOR-ULTRASONICO-LLAMA', 1, '2025-11-13 20:23:37.892043', '', '', '2025-11-13 17:13:05.278967', 4, 0, NULL),
(367, '', 0, 310, NULL, 0.00, 'LATTAFA-FAKHAR-BLACK-100ML', 1, '2025-11-13 20:23:38.223654', '', '', '2025-11-13 17:13:05.287964', 0, 0, NULL),
(368, '', 1, 311, NULL, 0.00, 'MAISON-ALHAMBRA-PINK-VELVET-80-ML-EDP', 1, '2025-11-13 20:23:38.385003', '', '', '2025-11-13 17:13:05.298121', 1, 0, NULL),
(369, '', 0, 312, NULL, 0.00, 'RELOJ-DUANTAI-MODELO-1173', 0, '2025-11-13 20:23:38.997986', '', '', '2025-11-13 17:13:05.307125', 0, 0, NULL),
(370, '', 0, 313, NULL, 0.00, 'RELOJ-DUANTAI-MODELO-1187', 0, '2025-11-13 20:23:39.015443', '', '', '2025-11-13 17:13:05.317501', 0, 0, NULL),
(371, '', 0, 314, NULL, 0.00, 'RELOJ-DUANTAI-MODELO-8190', 0, '2025-11-13 20:23:39.033458', '', '', '2025-11-13 17:13:05.327157', 0, 0, NULL),
(372, '', 0, 315, NULL, 0.00, 'RELOJ-KADIBIN-RICHARD-MILLE', 0, '2025-11-13 20:23:39.050509', '', '', '2025-11-13 17:13:05.337158', 0, 0, NULL),
(373, '', 0, 316, NULL, 0.00, 'RELOJ-CURREN-MODELO-8149', 0, '2025-11-13 20:23:38.898417', '', '', '2025-11-13 17:13:05.348354', 0, 0, NULL),
(374, '', 0, 317, NULL, 0.00, 'RELOJ-CURREN-MODELO-8362', 0, '2025-11-13 20:23:38.947669', '', '', '2025-11-13 17:13:05.358595', 0, 0, NULL),
(375, '', 0, 318, NULL, 0.00, 'RELOJ-CURREN-MODELO-8443', 0, '2025-11-13 20:23:38.965457', '', '', '2025-11-13 17:13:05.369107', 0, 0, NULL),
(376, '', 0, 319, NULL, 0.00, 'RELOJ-CURREN-MODELO-8229', 0, '2025-11-13 20:23:38.916143', '', '', '2025-11-13 17:13:05.383437', 0, 0, NULL),
(377, '', 0, 320, NULL, 0.00, 'RELOJ-DEPORTIVO-BANAMI-MODELO-1815G', 1, '2025-11-13 20:23:38.982465', '', '', '2025-11-13 17:13:05.398597', 0, 0, NULL),
(378, '', 13, 321, NULL, 0.00, 'AURICULARES-GAMER-MICROFONO-PC-NOGA-STORMER-ST-HEX-HEADSET', 1, '2025-11-13 20:23:36.672835', '', '', '2025-11-13 17:13:05.414220', 13, 0, NULL),
(379, '', 2, 322, NULL, 0.00, 'ADAPTADOR-XIAOMI-120W-USB', 1, '2025-11-13 20:23:36.295289', '', '', '2025-11-13 17:13:05.429956', 2, 0, NULL),
(380, '', 39, 323, NULL, 0.00, 'ADAPTADOR-XIAOMI-67W-USB', 1, '2025-11-13 20:23:36.309077', '', '', '2025-11-13 17:13:05.444332', 38, 0, NULL),
(381, '', 40, 324, NULL, 0.00, 'PILAS-AAA-ORYX', 1, '2025-11-13 20:23:38.761859', '', '', '2025-11-13 17:13:05.458513', 40, 0, NULL),
(382, '', 18, 325, NULL, 0.00, 'PILAS-AA-HYTOSHY', 1, '2025-11-13 20:23:38.752350', '', '', '2025-11-13 17:13:05.471672', 18, 0, NULL),
(383, '', 0, 326, NULL, 0.00, 'AURICULARES-VINCHA-PLEGABLES-CON-CABLE-DESMONTABLE', 0, '2025-11-13 20:23:36.939672', '', '', '2025-11-13 17:13:05.487207', 0, 0, NULL),
(384, '', 0, 327, NULL, 0.00, 'AURICULAR-EARPOD-SIMIL-TIPO-C', 0, '2025-11-13 20:23:36.426466', '', '', '2025-11-13 17:13:05.501370', 0, 0, NULL),
(385, '', 0, 328, NULL, 0.00, 'SMARTWATCH-TK-ULTRA-2', 0, '2025-11-13 20:23:39.227960', '', '', '2025-11-13 17:13:05.514744', 0, 0, NULL),
(386, '', 0, 329, NULL, 0.00, 'TIRA-NEON-1MT-CON-CONTROL', 1, '2025-11-13 20:23:39.423759', '', '', '2025-11-13 17:13:05.527891', 0, 0, NULL),
(387, '', 0, 330, NULL, 0.00, 'ADAPTADOR-20W-TIPO-C-OOGAN-1-1', 1, '2025-11-21 20:03:41.985088', '', '', '2025-11-13 17:13:05.542481', 20, 0, NULL),
(388, '', 0, 331, NULL, 0.00, 'ADAPTADOR-20W-TIPO-C-CON-CABLE-TIPO-C-A-C-OOGAN', 0, '2025-11-13 20:23:36.074549', '', '', '2025-11-13 17:13:05.558705', 0, 0, NULL),
(389, '', 0, 332, NULL, 0.00, 'LAMPARA-FILAMENTO-LED-IMAN-RECARGABLE-VELADOR-DECORATIVO-TL4', 0, '2025-11-13 20:23:38.119286', '', '', '2025-11-13 17:13:05.572211', 0, 0, NULL),
(390, '', 10, 333, NULL, 0.00, 'SAMSUNG-GALAXY-A06-64GB-4RAM', 1, '2025-11-13 20:23:39.087355', '', '', '2025-11-13 17:13:05.586668', 10, 0, NULL),
(391, '', 0, 334, NULL, 0.00, 'VIDRIOS-TEMPLADOS', 1, '2025-11-13 20:23:39.533335', '', '', '2025-11-13 17:13:05.600830', 0, 0, NULL),
(392, '', 0, 335, NULL, 0.00, 'CABLE-C-A-LIGHTNING-2MT', 0, '2025-11-13 20:23:37.018080', '', '', '2025-11-13 17:13:05.616357', 0, 0, NULL),
(393, '', 0, 336, NULL, 0.00, 'CABLE-UNIVERSAL-TIPO-C-USB-LIGHTNING', 0, '2025-11-13 20:23:37.105956', '', '', '2025-11-13 17:13:05.629509', 0, 0, NULL),
(394, '', 9, 337, NULL, 0.00, 'PARLANTE-JBL-CLIP5', 1, '2025-11-13 20:23:38.633566', '', '', '2025-11-13 17:13:05.641374', 9, 0, NULL),
(395, '', 0, 338, NULL, 0.00, 'CARGADOR-PARA-AUTO-MIXOR-12V', 0, '2025-11-13 20:23:37.385200', '', '', '2025-11-13 17:13:05.656098', 0, 0, NULL),
(396, '', 1, 339, NULL, 0.00, 'TV-STICK-WATCH', 1, '2025-11-13 20:23:39.483898', '', '', '2025-11-13 17:13:05.669760', 2, 0, NULL),
(397, '', 0, 340, NULL, 0.00, 'SMARTWATCH-GT1', 0, '2025-11-13 20:23:39.192773', '', '', '2025-11-13 17:13:05.680708', 0, 0, NULL),
(398, '', 2, 341, NULL, 0.00, 'MEMORIA-MICRO-SD-128GB-SPEED-FLASH', 1, '2025-11-13 20:23:38.421410', '', '', '2025-11-13 17:13:05.693738', 2, 0, NULL),
(399, '', 3, 342, NULL, 0.00, 'SMARTWATCH-Y20-7-MALLAS', 1, '2025-11-13 20:23:39.253838', '', '', '2025-11-13 17:13:05.706742', 3, 0, NULL),
(400, '', 3, 343, NULL, 0.00, 'AURICULARES-TWS-123-CON-PANTALLA', 1, '2025-11-13 20:23:36.840095', '', '', '2025-11-13 17:13:05.721244', 3, 0, NULL),
(401, '', 0, 344, NULL, 0.00, 'PROYECTOR-ASTRONAUTA-SIN-PARLANTE', 1, '2025-11-13 20:23:38.809900', '', '', '2025-11-13 17:13:05.733438', 0, 0, NULL),
(402, '', 3, 345, NULL, 0.00, 'CABLE-HDMI-MALLADO', 1, '2025-11-13 20:23:37.028085', '', '', '2025-11-13 17:13:05.747707', 3, 0, NULL),
(403, ' (1)', 2, 345, NULL, 0.00, 'CABLE-HDMI-MALLADO-1', 1, '2025-11-13 20:23:37.042347', '', '', '2025-11-13 17:13:05.763355', 2, 0, NULL),
(404, ' (2)', 0, 345, NULL, 0.00, 'CABLE-HDMI-MALLADO-2', 0, '2025-11-13 20:23:37.056683', '', '', '2025-11-13 17:13:05.781530', 0, 0, NULL),
(405, '', 1, 346, NULL, 0.00, 'PARLANTE-TIPO-JBL-GO4-PRO', 1, '2025-11-13 20:23:38.703338', '', '', '2025-11-13 17:13:05.794690', 1, 0, NULL),
(406, '', 0, 347, NULL, 0.00, 'PARLANTE-TIPO-JBL-GO3', 0, '2025-11-13 20:23:38.690338', '', '', '2025-11-13 17:13:05.805699', 0, 0, NULL),
(407, '', 1, 348, NULL, 0.00, 'PARLANTE-TIPO-JBL-ALEXA', 1, '2025-11-13 20:23:38.676708', '', '', '2025-11-13 17:13:05.818497', 1, 0, NULL),
(408, '', 0, 349, NULL, 0.00, 'AIRPODS-PRO-MAX', 1, '2025-11-13 20:23:36.357517', '', '', '2025-11-13 17:13:05.832645', 10, 0, NULL),
(409, '', 7, 350, NULL, 0.00, 'SMARTWATCH-ULTRA-9-7-MALLAS-INTERCAMBIABLES', 1, '2025-11-13 20:23:39.240689', '', '', '2025-11-13 17:13:05.847693', 7, 0, NULL),
(410, '', 0, 351, NULL, 0.00, 'ARMAS-DE-HIDROGEL', 1, '2025-11-13 20:23:36.368696', '', '', '2025-11-13 17:13:05.861347', 30, 0, NULL),
(411, '', 0, 352, NULL, 0.00, 'LATTAFA-AJWAD-PINK-TO-60ML', 1, '2025-11-13 20:23:38.173933', '', '', '2025-11-13 17:13:05.875932', 0, 0, NULL),
(412, '', 0, 353, NULL, 0.00, 'LATTAFA-ASAD-BOURBON-100ML', 1, '2025-11-13 20:23:38.187977', '', '', '2025-11-13 17:13:05.890456', 0, 0, NULL),
(413, '', 0, 354, NULL, 0.00, 'LATTAFA-BADEE-NOBLE-BLUSH-100ML', 1, '2025-11-13 20:23:38.201137', '', '', '2025-11-13 17:13:05.903615', 0, 0, NULL),
(414, '', 0, 355, NULL, 0.00, 'LATTAFA-ECLAIRE-FEMENINO-100ML', 1, '2025-11-13 20:23:38.211646', '', '', '2025-11-13 17:13:05.920419', 0, 0, NULL),
(415, '', 0, 356, NULL, 0.00, 'LATTAFA-YARA-CANDY-100ML', 1, '2025-11-13 20:23:38.287208', '', '', '2025-11-13 17:13:05.934085', 0, 0, NULL),
(416, '', 0, 357, NULL, 0.00, 'ZIMAYA-ONLY-YOU-100ML', 0, '2025-11-13 20:23:39.577316', '', '', '2025-11-13 17:13:05.949499', 0, 0, NULL),
(417, '', 4, 358, NULL, 0.00, 'ORIENTICA-ROYAL-AMBER-UNISEX', 1, '2025-11-13 20:23:38.588800', '', '', '2025-11-13 17:13:05.962442', 4, 0, NULL),
(418, '', 1, 359, NULL, 0.00, 'BOLSO-JORDAN-AIR-FESTIVAL-ORIGINAL', 1, '2025-11-13 20:23:36.961485', '', '', '2025-11-13 17:13:05.974812', 1, 0, NULL),
(419, '', 1, 360, NULL, 0.00, 'LATTAFA-HABIK-WOMEN-100ML', 1, '2025-11-13 20:23:38.247390', '', '', '2025-11-13 17:13:05.988711', 1, 0, NULL),
(420, '', 1, 361, NULL, 0.00, 'LATTAFA-SHAHD-EAU-DE-PARFUM-100ML', 1, '2025-11-13 20:23:38.260898', '', '', '2025-11-13 17:13:06.000893', 1, 0, NULL),
(421, '', 1, 362, NULL, 0.00, 'LATTAFA-FHAKAR-GOLD-100ML', 1, '2025-11-13 20:23:38.235876', '', '', '2025-11-13 17:13:06.015755', 1, 0, NULL),
(422, '', 1, 363, NULL, 0.00, 'ZIMAYA-HAYAM-EAU-DE-PARFUM-100ML', 1, '2025-11-13 20:23:39.564099', '', '', '2025-11-13 17:13:06.028896', 1, 0, NULL),
(423, '', 1, 364, NULL, 0.00, 'ZIMAYA-FATIMA-PINK-100ML', 1, '2025-11-13 20:23:39.554275', '', '', '2025-11-13 17:13:06.041720', 1, 0, NULL),
(424, '', 11, 365, NULL, 0.00, 'LATTAFA-THE-KINGDOM-MAN-100ML', 1, '2025-11-13 20:23:38.273900', '', '', '2025-11-13 17:13:06.053806', 11, 0, NULL),
(425, '', 3, 366, NULL, 0.00, 'ADAPTADOR-TIPO-C-A-AUDIOCHARGING', 1, '2025-11-13 20:23:36.283781', '', '', '2025-11-13 17:13:06.068432', 0, 0, NULL),
(426, '', 1, 367, NULL, 0.00, 'HUB-TIPO-C', 1, '2025-11-13 20:23:37.878882', '', '', '2025-11-13 17:13:06.084719', 1, 0, NULL),
(427, '', 2, 368, NULL, 0.00, 'MICROFONO-LU-B24', 1, '2025-11-13 20:23:38.432420', '', '', '2025-11-13 17:13:06.097867', 2, 0, NULL),
(428, '', 5, 369, NULL, 0.00, 'FREIDORA-DE-AIRE-10L', 1, '2025-11-13 20:23:37.523352', '', '', '2025-11-13 17:13:06.109746', 5, 0, NULL),
(429, '', 6, 370, NULL, 0.00, 'LAMPARA-SUNSET-LIGHT-CON-TRIPODE', 1, '2025-11-13 20:23:38.143115', '', '', '2025-11-13 17:13:06.124260', 6, 0, NULL),
(430, '', 20, 371, NULL, 0.00, 'PAD-ESCRITORIO-600X300X2MM', 1, '2025-11-13 20:23:38.600806', '', '', '2025-11-13 17:13:06.137917', 20, 0, NULL),
(431, '', 3, 372, NULL, 0.00, 'AURICULAR-CABLE-S8', 1, '2025-11-13 20:23:36.403966', '', '', '2025-11-13 17:13:06.153594', 3, 0, NULL),
(432, '', 2, 373, NULL, 0.00, 'AURICULARES-VINCHA-BT', 1, '2025-11-13 20:23:36.904213', '', '', '2025-11-13 17:13:06.168273', 2, 0, NULL),
(433, '', 4, 374, NULL, 0.00, 'TV-STICK-8G-4K', 1, '2025-11-13 20:23:39.472564', '', '', '2025-11-13 17:13:06.182666', 4, 0, NULL),
(434, '', 3, 375, NULL, 0.00, 'CORTA-PELO-DE-COLORES-DIGITAL-MELECH', 1, '2025-11-13 20:23:37.433930', '', '', '2025-11-13 17:13:06.193814', 3, 0, NULL),
(435, '', 5, 376, NULL, 0.00, 'SET-5-BOWLS-DE-ACERO-INOXIDABLE-CON-TAPA-RECIPIENTE-METALICO', 1, '2025-11-13 20:23:39.098876', '', '', '2025-11-13 17:13:06.205818', 5, 0, NULL),
(436, '', 2, 377, NULL, 0.00, 'KIT-MOCHILA-ANTIRROBO-URBANA-PARA-NOTEBOOK-MORRAL-ESTUCHE-3-', 1, '2025-11-13 20:23:38.009614', '', '', '2025-11-13 17:13:06.219818', 2, 0, NULL),
(437, '', 10, 378, NULL, 0.00, 'TV-BOX-CAJA-VERDE-4K-ULTRA-HD-512GB-64GB-RAM', 1, '2025-11-13 20:23:39.447809', '', '', '2025-11-13 17:13:06.233577', 10, 0, NULL),
(438, '', 9, 379, NULL, 0.00, 'ADAPTADOR-CARGADO-AUTO-A-TIPO-C', 1, '2025-11-21 20:03:41.988676', '', '', '2025-11-13 17:13:06.248604', 7, 0, NULL),
(439, '', 10, 380, NULL, 0.00, 'SOPORTE-PARA-CELULAR-PLEGABLE-METALICO', 1, '2025-11-13 20:23:39.290654', '', '', '2025-11-13 17:13:06.261329', 10, 0, NULL),
(440, '', 100, 381, NULL, 0.00, 'CABLE-KLGO-AUXILIAR-35-A-35-EN-L-COLORES-1MT', 1, '2025-11-13 20:23:37.068669', '', '', '2025-11-13 17:13:06.274690', 100, 0, NULL),
(441, '', 20, 382, NULL, 0.00, 'CABLE-SAMSUNG-2A-TIPO-C-CARGA-RAPIDA-BOLSA-AZUL', 1, '2025-11-13 20:23:37.094163', '', '', '2025-11-13 17:13:06.286709', 20, 0, NULL),
(442, '', 3, 383, NULL, 0.00, 'CABLE-USB-TIPO-C-A-TIPO-C-SAMSUNG-CAJA', 1, '2025-11-13 20:23:37.238896', '', '', '2025-11-13 17:13:06.299869', 3, 0, NULL),
(443, '', 10, 384, NULL, 0.00, 'AURICULAR-GAMER-GM-06-PC-PS4-HEADPHONES', 1, '2025-11-13 20:23:36.503808', '', '', '2025-11-13 17:13:06.312300', 10, 0, NULL),
(444, '', 4, 385, NULL, 0.00, 'AURICULAR-GAMING-CON-CABLE', 1, '2025-11-13 20:23:36.521023', '', '', '2025-11-13 17:13:06.324302', 4, 0, NULL),
(445, '', 4, 386, NULL, 0.00, 'AURICULAR-EARPODS-LIGHTNING', 1, '2025-11-13 20:23:36.452795', '', '', '2025-11-13 17:13:06.335972', 4, 0, NULL),
(446, '', 4, 387, NULL, 0.00, 'AURICULAR-EARPODS-AUX', 1, '2025-11-13 20:23:36.440221', '', '', '2025-11-13 17:13:06.348857', 4, 0, NULL),
(447, '', 4, 388, NULL, 0.00, 'AURICULAR-EARPODS-TIPO-C', 1, '2025-11-13 20:23:36.470661', '', '', '2025-11-13 17:13:06.361535', 4, 0, NULL),
(448, '', 2, 389, NULL, 0.00, 'JACK-APPLE-TIPO-C-A-35', 1, '2025-11-13 20:23:37.916882', '', '', '2025-11-13 17:13:06.374545', 2, 0, NULL),
(449, '', 3, 390, NULL, 0.00, 'AURICULAR-GALAXY-BUDS-3', 1, '2025-11-13 20:23:36.486495', '', '', '2025-11-13 17:13:06.386891', 3, 0, NULL),
(450, '', 4, 391, NULL, 0.00, 'AURICULAR-CAJA-BLANCA-TIPO-C', 1, '2025-11-13 20:23:36.415456', '', '', '2025-11-13 17:13:06.398086', 35, 0, NULL),
(451, '', 7, 392, NULL, 0.00, 'AURICULAR-LIGHTNING-CAJA-TRANSPARENTE', 1, '2025-11-13 20:23:36.538653', '', '', '2025-11-13 17:13:06.410221', 7, 0, NULL),
(452, '', 0, 393, NULL, 0.00, 'PEGATINA-SOPAPA-PARA-CELULAR-CON-ANILLO', 1, '2025-11-13 20:23:38.726658', '', '', '2025-11-13 17:13:06.422826', 0, 0, NULL),
(453, '', 0, 394, NULL, 0.00, 'ascasc', 1, '2025-11-13 20:23:36.378690', '', '', '2025-11-13 20:14:45.441624', 0, 0, NULL),
(454, 'iPhone 11 64GB Morado', 1, 395, NULL, 0.00, 'IPHONE-11-64GB-MORADO', 1, '2025-11-21 20:12:24.982593', '64GB', 'Morado', '2025-11-14 00:07:07.831165', 2, 0, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_proveedor`
--

CREATE TABLE IF NOT EXISTS `inventario_proveedor` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `inventario_proveedor`:
--

--
-- Volcado de datos para la tabla `inventario_proveedor`
--

INSERT INTO `inventario_proveedor` (`id`, `nombre`, `telefono`, `email`, `activo`) VALUES
(1, 'VARIOS', '266503', 'emanuelsosa4436@gmail.com', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `locales_local`
--

CREATE TABLE IF NOT EXISTS `locales_local` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `locales_local`:
--

--
-- Volcado de datos para la tabla `locales_local`
--

INSERT INTO `locales_local` (`id`, `nombre`, `direccion`, `creado`, `actualizado`) VALUES
(1, 'ImportST', 'Belgrano 47, San Luis', '2025-11-12 16:57:31.035108', '2025-11-12 16:57:31.035108');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_carritoremoto`
--

CREATE TABLE IF NOT EXISTS `ventas_carritoremoto` (
  `id` bigint(20) NOT NULL,
  `items` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`items`)),
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `ventas_carritoremoto`:
--   `usuario_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `ventas_carritoremoto`
--

INSERT INTO `ventas_carritoremoto` (`id`, `items`, `actualizado`, `usuario_id`) VALUES
(1, '[]', '2025-11-21 20:19:09.856149', 2),
(2, '[]', '2025-11-21 20:03:42.009867', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_cupon`
--

CREATE TABLE IF NOT EXISTS `ventas_cupon` (
  `id` bigint(20) NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `tipo_descuento` varchar(20) NOT NULL,
  `valor_descuento` decimal(10,2) NOT NULL,
  `monto_minimo` decimal(12,2) NOT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_fin` datetime(6) NOT NULL,
  `usos_maximos` int(11) NOT NULL,
  `usos_actuales` int(11) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `solo_mayoristas` tinyint(1) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `ventas_cupon`:
--

--
-- Volcado de datos para la tabla `ventas_cupon`
--

INSERT INTO `ventas_cupon` (`id`, `codigo`, `descripcion`, `tipo_descuento`, `valor_descuento`, `monto_minimo`, `fecha_inicio`, `fecha_fin`, `usos_maximos`, `usos_actuales`, `activo`, `solo_mayoristas`, `creado`, `actualizado`) VALUES
(1, 'TEST', '', 'PORCENTAJE', 10.00, 0.00, '2025-11-21 15:43:58.409715', '2025-11-21 15:43:58.410020', 0, 0, 1, 0, '2025-11-21 15:43:58.420417', '2025-11-21 15:43:58.420431');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_detalleventa`
--

CREATE TABLE IF NOT EXISTS `ventas_detalleventa` (
  `id` bigint(20) NOT NULL,
  `sku` varchar(60) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL,
  `precio_unitario_ars_congelado` decimal(12,2) NOT NULL,
  `subtotal_ars` decimal(12,2) NOT NULL,
  `variante_id` bigint(20) DEFAULT NULL,
  `venta_id` varchar(20) NOT NULL,
  `precio_unitario_usd_original` decimal(12,2) DEFAULT NULL,
  `tipo_cambio_usado` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `ventas_detalleventa`:
--   `variante_id`
--       `inventario_productovariante` -> `id`
--   `venta_id`
--       `ventas_venta` -> `id`
--

--
-- Volcado de datos para la tabla `ventas_detalleventa`
--

INSERT INTO `ventas_detalleventa` (`id`, `sku`, `descripcion`, `cantidad`, `precio_unitario_ars_congelado`, `subtotal_ars`, `variante_id`, `venta_id`, `precio_unitario_usd_original`, `tipo_cambio_usado`) VALUES
(1, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-BE12561B', NULL, NULL),
(3, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-6251D818', NULL, NULL),
(4, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-CB216F2A', NULL, NULL),
(5, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-119A299D', NULL, NULL),
(7, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 12121212.00, 12121212.00, NULL, 'POS-B627CAD1', NULL, NULL),
(8, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-4B6258AE', NULL, NULL),
(9, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 12121212.00, 12121212.00, NULL, 'POS-3BABAE79', 12121212.00, 1420.00),
(10, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 8800.00, 1, 'POS-B0240418', NULL, NULL),
(11, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 9988.00, 1, 'POS-F5DB5517', NULL, NULL),
(12, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 12121212.00, 606060.60, NULL, 'POS-F5DB5517', 12121212.00, 1420.00),
(13, 'SKU-000002', 'iPhone 13 mini Sin especificar', 1, 350.00, 350.00, NULL, 'POS-5D3E5CE4', 350.00, 1420.00),
(14, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 8800.00, 1, 'POS-553AE394', NULL, NULL),
(15, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 8778.00, 1, 'POS-298C6FD3', NULL, NULL),
(16, 'VAR-1762980757.047442', 'Producto varios', 1, 1500.00, 1488.00, NULL, 'POS-5BEC9024', NULL, NULL),
(17, 'VAR-1762980788.462759', 'Producto varios', 1, 1999.00, 1999.00, NULL, 'POS-796712CB', NULL, NULL),
(19, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-90825F5D', NULL, NULL),
(20, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1222.00, 1222.00, NULL, 'POS-65B108DF', 1222.00, 1415.00),
(21, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-65B108DF', NULL, NULL),
(22, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, NULL, 'POS-DF47FA7E', 1222.00, 1415.00),
(23, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, NULL, 'POS-C21BAE7C', 1222.00, 1415.00),
(24, 'SKU-000001', 'CArgador Sin especificar', 2, 10000.00, 20000.00, 1, 'POS-A4518974', NULL, NULL),
(25, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, NULL, 'POS-39941E37', 1222.00, 1415.00),
(26, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, NULL, 'POS-9EB7FA22', 1222.00, 1415.00),
(27, 'VAR-1762985874.181103', 'Producto varios', 1, 50000.00, 50000.00, NULL, 'POS-00EA9703', NULL, NULL),
(28, 'VAR-1762986087.653159', 'Producto varios', 1, 12121212.00, 12121212.00, NULL, 'POS-B80FE78F', NULL, NULL),
(29, 'VAR-1762988766.550541', 'Producto varios', 1, 1300.00, 1288.00, NULL, 'POS-FE370894', NULL, NULL),
(30, 'VAR-1762988989.885236', 'Producto varios', 1, 21212.00, 21212.00, NULL, 'POS-92C3F826', NULL, NULL),
(31, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-ECB1CCF8', NULL, NULL),
(32, 'VAR-1762989339.28968', 'Producto varios', 1, 1212.00, 1212.00, NULL, 'POS-ECB1CCF8', NULL, NULL),
(33, 'VAR-1762989784.326604', 'Producto varios', 1, 121.00, 121.00, NULL, 'POS-130AD6CE', NULL, NULL),
(34, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-D990084C', NULL, NULL),
(35, 'IPHONE-13-MINI-64GB-TITANIO-NATURAL', 'iPhone 13 mini 64GB / Titanio Natural', 1, 1729130.00, 1729130.00, NULL, 'POS-ABFC278E', 1222.00, 1415.00),
(36, 'VAR-1762991096597', 'cacsscacs', 1, 1212.00, 1212.00, NULL, 'POS-F74FFB14', NULL, NULL),
(37, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-248DDA43', NULL, NULL),
(38, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-3650B009', NULL, NULL),
(39, 'SKU-000001', 'CArgador Sin especificar', 1, 10000.00, 10000.00, 1, 'POS-0E5CFD36', NULL, NULL),
(40, 'VAR-1762992012680', 'CARGADOR 20W', 1, 2222.00, 2222.00, NULL, 'POS-0E5CFD36', NULL, NULL),
(41, 'IPHONE-16-128GB-TITANIO-NEGRO', 'iPhone 16 128GB / Titanio Negro', 1, 1729130.00, 1729130.00, 4, 'POS-1E7960FF', 1222.00, 1415.00),
(42, 'cargador', 'CArgador Sin especificar', 1, 10000.00, 9000.00, 1, 'POS-040397B8', NULL, NULL),
(43, 'VAR-1763006399390', 'tv', 1, 1222.00, 1222.00, NULL, 'POS-040397B8', NULL, NULL),
(44, 'VAR-1763006565804', 'aaaa', 1, 11.00, 11.00, NULL, 'POS-8D0BAA4A', NULL, NULL),
(45, 'VAR-1763011627490', 'Parlante', 1, 6500.00, 6500.00, NULL, 'POS-41E8B8C7', NULL, NULL),
(46, 'VAR-1763011991916', 'TV box', 1, 50500.00, 50500.00, NULL, 'POS-A074FD78', NULL, NULL),
(47, 'VAR-1763014697928', 'Fundas 2x1', 1, 9990.00, 9990.00, NULL, 'POS-A518A580', NULL, NULL),
(48, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-5773F459', NULL, NULL),
(49, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-049D4502', NULL, NULL),
(50, 'IPHONE-16-128GB-TITANIO-NEGRO', 'iPhone 16 128GB / Titanio Negro', 1, 1729130.00, 1729130.00, 4, 'POS-049D4502', 1222.00, 1415.00),
(51, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-20F0E7F3', NULL, NULL),
(52, 'VAR-1763019751174', 'Cargador', 1, 5600.00, 5600.00, NULL, 'POS-D4BF06D2', NULL, NULL),
(53, 'cargador-20w-pata-recta', 'Cargador 20w pata recta', 1, 9500.00, 9500.00, 1, 'POS-CDE476D4', NULL, NULL),
(54, 'ARMAS-DE-HIDROGEL', 'Armas de Hidrogel Sin especificar', 1, 74250.00, 742.50, 410, 'POS-31A9A44D', NULL, NULL),
(55, 'AIRPODS-4AAA', 'AirPods 4(+AAA) Sin especificar', 1, 48125.00, 40906.25, 345, 'POS-31A9A44D', NULL, NULL),
(56, 'AURICULAR-BT-MUSIC-LIFE', 'AURICULAR BT MUSIC LIFE Sin especificar', 1, 26952.77, 26952.77, 294, 'POS-6B100E8F', NULL, NULL),
(57, 'ADAPTADOR-AURICULAR-A-IPHONE', 'Adaptador Auricular a IPhone Sin especificar', 1, 43098.97, 43098.97, 215, 'POS-6B100E8F', NULL, NULL),
(58, 'IPHONE-16-128GB-TITANIO-NEGRO', 'iPhone 16 128GB / Titanio Negro', 1, 1729130.00, 1729130.00, 4, 'POS-6B100E8F', 1222.00, 1415.00),
(59, 'ADAPTADOR-XIAOMI-67W-USB', 'Adaptador XIAOMI 67W USB Sin especificar', 1, 1500.00, 1500.00, 380, 'POS-B00486BF', NULL, NULL),
(60, 'ADAPTADOR-MOTOROLA-CABLE-TIPO-C', 'Adaptador Motorola + Cable Tipo C Sin especificar', 1, 4426.59, 4426.59, 246, 'POS-B00486BF', NULL, NULL),
(61, 'ADAPTADOR-CARGADO-AUTO-A-TIPO-C', 'Adaptador Cargado Auto a Tipo C Sin especificar', 1, 11990.00, 11990.00, 438, 'POS-B00486BF', NULL, NULL),
(62, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 'iPhone 15 Pro 64GB / Titanio Natural', 1, 2122500.00, 2122500.00, 9, 'POS-CA846B38', 1500.00, 1415.00),
(63, 'AURICULAR-LIGHTNING-CAJA-TRANSPARENTE', 'AURICULAR LIGHTNING CAJA TRANSPARENTE Sin especificar', 1, 4990.00, 4990.00, 451, 'POS-762454C2', NULL, NULL),
(64, 'AIRPODS-4AAA', 'AirPods 4(+AAA) Sin especificar', 2, 48125.00, 96250.00, 345, 'POS-98BB15AC', NULL, NULL),
(65, 'ADAPTADOR-XIAOMI-67W-USB', 'Adaptador XIAOMI 67W USB Sin especificar', 4, 1500.00, 6000.00, 380, 'POS-98BB15AC', NULL, NULL),
(66, 'ADAPTADOR-JACK-A-USB-C-SAMSUNG', 'Adaptador Jack a USB C Samsung Sin especificar', 4, 5055.75, 20223.00, 250, 'POS-98BB15AC', NULL, NULL),
(67, 'AURICULAR-CAJA-BLANCA-TIPO-C', 'AURICULAR CAJA BLANCA TIPO C Sin especificar', 1, 11990.00, 11990.00, 450, 'POS-98BB15AC', NULL, NULL),
(68, 'AURICULAR-CABLE-S8', 'AURICULAR CABLE S8 Sin especificar', 2, 19990.00, 39980.00, 431, 'POS-98BB15AC', NULL, NULL),
(69, 'ADAPTADOR-CARGADO-AUTO-A-TIPO-C', 'Adaptador Cargado Auto a Tipo C Sin especificar', 3, 11990.00, 35970.00, 438, 'POS-98BB15AC', NULL, NULL),
(70, 'ADAPTADOR-MOTOROLA-CABLE-TIPO-C', 'Adaptador Motorola + Cable Tipo C Sin especificar', 1, 4426.59, 4426.59, 246, 'POS-98BB15AC', NULL, NULL),
(71, 'ADAPTADOR-SAMSUNG-25W', 'Adaptador Samsung 25W Sin especificar', 3, 6373.89, 19121.67, 232, 'POS-98BB15AC', NULL, NULL),
(72, 'ADAPTADOR-AURICULAR-A-IPHONE', 'Adaptador Auricular a IPhone Sin especificar', 1, 43098.97, 43098.97, 215, 'POS-98BB15AC', NULL, NULL),
(73, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 'iPhone 15 Pro 64GB / Titanio Natural', 1, 2122500.00, 2122500.00, 9, 'POS-D485FC80', 1500.00, 1415.00),
(74, 'ADAPTADOR-MOTOROLA-CABLE-TIPO-C', 'Adaptador Motorola + Cable Tipo C ', 2, 1.00, 2.00, 246, 'POS-90E0619E', NULL, NULL),
(75, 'ADAPTADOR-XIAOMI-67W-USB', 'Adaptador XIAOMI 67W USB ', 1, 1.00, 1.00, 380, 'POS-90E0619E', NULL, NULL),
(76, 'ADAPTADOR-TIPO-C-A-AUDIOCHARGING', 'Adaptador Tipo C a Audio/Charging ', 3, 1.00, 3.00, 425, 'POS-90E0619E', NULL, NULL),
(77, 'ADAPTADOR-AURICULAR-A-IPHONE', 'Adaptador Auricular a IPhone ', 2, 1.00, 2.00, 215, 'POS-90E0619E', NULL, NULL),
(78, 'CABLE-LIGHTNING-A-USB-IPHONE-2MT', 'Cable Lightning A Usb IPhone 2Mt ', 1, 1.00, 1.00, 239, 'POS-611E669B', NULL, NULL),
(79, 'CARGADOR-5W-USB-IPHONE', 'Cargador 5w USB IPhone ', 1, 1.00, 1.00, 194, 'POS-56C4E11D', NULL, NULL),
(80, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 'iPhone 15 Pro 64GB / Titanio Natural', 1, 2122500.00, 2122500.00, 9, 'POS-56C4E11D', 1500.00, 1415.00),
(81, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 'iPhone 15 Pro 64GB / Titanio Natural', 1, 2122500.00, 2122500.00, 9, 'POS-1AF59883', 1500.00, 1415.00),
(82, 'VAR-1763137612832-0', 'Fuente 20w Tipo apple', 5, 4600.00, 23000.00, NULL, 'POS-3EEECD18', NULL, NULL),
(83, 'VAR-1763137612832-1', 'Cable c a iphone 1mt', 5, 2350.00, 11750.00, NULL, 'POS-3EEECD18', NULL, NULL),
(84, 'VAR-1763137612832-2', 'Cable usb a iphone 1mt', 5, 2000.00, 10000.00, NULL, 'POS-3EEECD18', NULL, NULL),
(85, 'VAR-1763137696436-0', 'Cable C a C mallado', 5, 2850.00, 14250.00, NULL, 'POS-3EEECD18', NULL, NULL),
(86, 'VAR-1763137831336-0', 'Templados varios 9d', 34, 890.00, 30260.00, NULL, 'POS-3EEECD18', NULL, NULL),
(87, 'VAR-1763137831336-1', 'Fundas magsafe', 16, 2650.00, 42400.00, NULL, 'POS-3EEECD18', NULL, NULL),
(88, 'VAR-1763137831336-2', 'protector de camara/ funda con proyector de camara', 23, 1500.00, 34500.00, NULL, 'POS-3EEECD18', NULL, NULL),
(89, 'VAR-1763137831336-3', 'Mix de fundas 1', 8, 1600.00, 12800.00, NULL, 'POS-3EEECD18', NULL, NULL),
(90, 'VAR-1763137831336-4', 'mix de fundas 2', 10, 1990.00, 19900.00, NULL, 'POS-3EEECD18', NULL, NULL),
(91, 'VAR-1763138174757-0', 'templado linea 17', 3, 1000.00, 3000.00, NULL, 'POS-3EEECD18', NULL, NULL),
(92, 'IPHONE-15-PRO-64GB-TITANIO-NATURAL', 'iPhone 15 Pro 64GB / Titanio Natural', 1, 2115000.00, 2115000.00, 9, 'POS-6B0D8096', 1500.00, 1410.00),
(93, 'TV-STICK-WATCH', 'TV Stick Watch', 1, 1.00, 1.00, 396, 'WEB-20251121150919', NULL, NULL),
(94, 'ADAPTADOR-20W-TIPO-C-OOGAN', 'Adaptador 20W Tipo C Oogan', 2, 1560000.00, 3120000.00, 387, 'WEB-20251121150919', NULL, NULL),
(95, 'ADAPTADOR-APPLE-20W-TIPO-C-ORIGINAL-APPLE', 'Adaptador Apple 20w Tipo C (ORIGINAL APPLE)', 2, 1.00, 2.00, 219, 'WEB-20251121150919', NULL, NULL),
(96, 'ADAPTADOR-20W-TIPO-C-OOGAN', 'Adaptador 20W Tipo C Oogan', 4, 1560000.00, 6240000.00, 387, 'WEB-251121160421-137', NULL, NULL),
(97, 'ADAPTADOR-APPLE-20W-TIPO-C-ORIGINAL-APPLE', 'Adaptador Apple 20w Tipo C (ORIGINAL APPLE)', 4, 1.00, 4.00, 219, 'WEB-251121160421-137', NULL, NULL),
(98, 'ADAPTADOR-5W-USB-IPHONE-CARGADORCABLE', 'Adaptador 5w USB IPhone Cargador+Cable', 2, 1.00, 2.00, 199, 'WEB-251121160421-137', NULL, NULL),
(99, 'NEBLINERO-LED', 'Neblinero Led', 1, 1.00, 1.00, 271, 'WEB-251121160421-137', NULL, NULL),
(100, 'MOUSE-INALAMBRICO-A-PILAS', 'Mouse Inalámbrico a Pilas', 1, 1.00, 1.00, 290, 'WEB-251121160421-137', NULL, NULL),
(101, 'MOTO-E14', 'Moto E14', 1, 1.00, 1.00, 323, 'WEB-251121160421-137', NULL, NULL),
(102, 'IPHONE-11-64GB-MORADO', 'iPhone 11 64GB / Morado', 1, 351250.00, 351250.00, 454, 'WEB-251121164708-985', NULL, NULL),
(103, 'IPHONE-11-64GB-MORADO', 'iPhone 11 64GB / Morado', 1, 351250.00, 351250.00, 454, 'WEB-251121164842-385', NULL, NULL),
(104, 'IPHONE-11-64GB-MORADO', 'iPhone 11 64GB / Morado', 1, 351250.00, 351250.00, 454, 'WEB-251121170232-788', NULL, NULL),
(105, 'ADAPTADOR-20W-TIPO-C-OOGAN', 'Adaptador 20W Tipo C Oogan', 4, 1560000.00, 6240000.00, 387, 'WEB-251121170742-675', NULL, NULL),
(107, 'ADAPTADOR-APPLE-20W-TIPO-C-ORIGINAL-APPLE', 'Adaptador Apple 20w Tipo C (ORIGINAL APPLE) ', 2, 1.00, 2.00, 219, 'POS-BD33A466', NULL, NULL),
(108, 'ADAPTADOR-5W-USB-IPHONE-CARGADORCABLE', 'Adaptador 5w USB IPhone Cargador+Cable ', 2, 1.00, 2.00, 199, 'POS-BD33A466', NULL, NULL),
(109, 'ADAPTADOR-20W-TIPO-C-OOGAN', 'Adaptador 20W Tipo C Oogan ', 2, 1560000.00, 3120000.00, 387, 'POS-BD33A466', NULL, NULL),
(110, 'ADAPTADOR-CARGADO-AUTO-A-TIPO-C', 'Adaptador Cargado Auto a Tipo C ', 1, 1.00, 1.00, 438, 'POS-3CD519E6', NULL, NULL),
(111, 'ADAPTADOR-20W-TIPO-C-OOGAN-1-1', 'Adaptador 20W Tipo C Oogan', 1, 1560000.00, 1560000.00, 387, 'WEB-251121200341-751', NULL, NULL),
(112, 'ADAPTADOR-CARGADO-AUTO-A-TIPO-C', 'Adaptador Cargado Auto a Tipo C', 1, 1.00, 1.00, 438, 'WEB-251121200341-751', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_historialestadoventa`
--

CREATE TABLE IF NOT EXISTS `ventas_historialestadoventa` (
  `id` bigint(20) NOT NULL,
  `estado_anterior` varchar(30) DEFAULT NULL,
  `estado_nuevo` varchar(30) NOT NULL,
  `nota` longtext DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `venta_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `ventas_historialestadoventa`:
--   `usuario_id`
--       `auth_user` -> `id`
--   `venta_id`
--       `ventas_venta` -> `id`
--

--
-- Volcado de datos para la tabla `ventas_historialestadoventa`
--

INSERT INTO `ventas_historialestadoventa` (`id`, `estado_anterior`, `estado_nuevo`, `nota`, `creado`, `usuario_id`, `venta_id`) VALUES
(1, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 15:09:19.312158', 7, 'WEB-20251121150919'),
(2, 'PENDIENTE_PAGO', 'PENDIENTE_ARMADO', '', '2025-11-21 15:30:32.630086', 2, 'WEB-20251121150919'),
(3, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 16:04:21.602972', 7, 'WEB-251121160421-137'),
(4, 'PENDIENTE_PAGO', 'LISTO_RETIRAR', '', '2025-11-21 16:05:00.919588', 2, 'WEB-251121160421-137'),
(5, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 16:47:08.687012', 7, 'WEB-251121164708-985'),
(6, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 16:48:42.475723', 7, 'WEB-251121164842-385'),
(7, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 17:02:32.255778', 7, 'WEB-251121170232-788'),
(8, 'PENDIENTE_PAGO', 'COMPLETADO', '', '2025-11-21 17:05:33.726877', 2, 'WEB-251121170232-788'),
(9, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 17:07:42.999706', 7, 'WEB-251121170742-675'),
(10, 'PENDIENTE_PAGO', 'DEVUELTO', '', '2025-11-21 18:09:41.883320', 2, 'WEB-251121170742-675'),
(11, NULL, 'PENDIENTE_PAGO', 'Pedido creado desde la web', '2025-11-21 20:03:41.975615', 7, 'WEB-251121200341-751'),
(12, 'PENDIENTE_PAGO', 'PENDIENTE_ARMADO', '', '2025-11-21 20:04:42.741656', 2, 'WEB-251121200341-751');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_solicitudimpresion`
--

CREATE TABLE IF NOT EXISTS `ventas_solicitudimpresion` (
  `id` bigint(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `error` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `procesado` datetime(6) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `venta_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `ventas_solicitudimpresion`:
--   `usuario_id`
--       `auth_user` -> `id`
--   `venta_id`
--       `ventas_venta` -> `id`
--

--
-- Volcado de datos para la tabla `ventas_solicitudimpresion`
--

INSERT INTO `ventas_solicitudimpresion` (`id`, `estado`, `error`, `creado`, `procesado`, `usuario_id`, `venta_id`) VALUES
(1, 'COMPLETADA', '', '2025-11-13 07:12:34.063212', '2025-11-13 07:12:38.890269', 2, 'POS-A518A580'),
(2, 'COMPLETADA', '', '2025-11-13 07:12:54.397019', '2025-11-13 07:12:58.402907', 2, 'POS-A074FD78'),
(3, 'COMPLETADA', '', '2025-11-13 07:13:22.956973', '2025-11-13 07:13:28.999677', 2, 'POS-5773F459'),
(4, 'COMPLETADA', '', '2025-11-13 07:14:15.090431', '2025-11-13 07:15:08.346292', 2, 'POS-5773F459'),
(5, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 07:18:35.087974', NULL, 2, 'POS-049D4502'),
(6, 'COMPLETADA', '', '2025-11-13 07:19:39.944664', '2025-11-13 07:21:30.271004', 2, 'POS-A518A580'),
(7, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 07:21:43.526031', NULL, 2, 'POS-8D0BAA4A'),
(8, 'PROCESANDO', '', '2025-11-13 07:21:58.960741', NULL, 2, 'POS-41E8B8C7'),
(9, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 14:15:31.797308', NULL, 2, 'POS-CDE476D4'),
(10, 'COMPLETADA', '', '2025-11-13 14:15:56.956312', '2025-11-13 14:16:04.531638', 2, 'POS-CDE476D4'),
(11, 'ERROR', 'No se pudo abrir la ventana de impresión. Verifica que los pop-ups estén habilitados.', '2025-11-13 15:14:16.049903', NULL, 2, 'POS-CDE476D4'),
(12, 'COMPLETADA', '', '2025-11-13 20:10:44.511737', '2025-11-13 20:11:41.921844', 2, 'POS-98BB15AC');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_venta`
--

CREATE TABLE IF NOT EXISTS `ventas_venta` (
  `id` varchar(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `nota` longtext NOT NULL,
  `cliente_documento` varchar(40) NOT NULL,
  `cliente_nombre` varchar(120) NOT NULL,
  `comprobante_pdf` varchar(100) DEFAULT NULL,
  `vendedor_id` int(11) DEFAULT NULL,
  `actualizado` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `cliente_id` bigint(20) DEFAULT NULL,
  `descuento_total_ars` decimal(12,2) NOT NULL,
  `impuestos_ars` decimal(12,2) NOT NULL,
  `status` varchar(30) NOT NULL,
  `subtotal_ars` decimal(12,2) NOT NULL,
  `total_ars` decimal(12,2) NOT NULL,
  `es_pago_mixto` tinyint(1) NOT NULL,
  `metodo_pago_2` varchar(20) DEFAULT NULL,
  `monto_pago_1` decimal(12,2) DEFAULT NULL,
  `monto_pago_2` decimal(12,2) DEFAULT NULL,
  `descuento_metodo_pago_ars` decimal(12,2) NOT NULL,
  `motivo_cancelacion` longtext DEFAULT NULL,
  `origen` varchar(10) NOT NULL,
  `estado_pago` varchar(20) NOT NULL,
  `estado_entrega` varchar(20) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `descuento_cupon_ars` decimal(12,2) NOT NULL,
  `cupon_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELACIONES PARA LA TABLA `ventas_venta`:
--   `cliente_id`
--       `crm_cliente` -> `id`
--   `cupon_id`
--       `ventas_cupon` -> `id`
--   `vendedor_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `ventas_venta`
--

INSERT INTO `ventas_venta` (`id`, `fecha`, `metodo_pago`, `nota`, `cliente_documento`, `cliente_nombre`, `comprobante_pdf`, `vendedor_id`, `actualizado`, `cliente_id`, `descuento_total_ars`, `impuestos_ars`, `status`, `subtotal_ars`, `total_ars`, `es_pago_mixto`, `metodo_pago_2`, `monto_pago_1`, `monto_pago_2`, `descuento_metodo_pago_ars`, `motivo_cancelacion`, `origen`, `estado_pago`, `estado_entrega`, `observaciones`, `descuento_cupon_ars`, `cupon_id`) VALUES
('1', '2025-11-11 20:09:48.089697', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-0686AF2B.pdf', NULL, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('2', '2025-11-11 20:13:01.217921', 'efectivo', '', '123123123', 'gordero 1', 'comprobantes/comprobante_POS-7C627328.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('3', '2025-11-11 20:22:27.187346', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-6A89ADAE.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('4', '2025-11-11 20:44:58.355407', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-88CA0C8B.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('5', '2025-11-12 15:22:13.767144', 'efectivo', '', '', '', 'comprobantes/comprobante_POS-CF4E18B1.pdf', 2, '2025-11-12 15:48:39.276930', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-00EA9703', '2025-11-12 22:17:54.183117', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-00EA9703.pdf', 2, '2025-11-12 22:17:54.346782', NULL, 0.00, 0.00, 'COMPLETADO', 50000.00, 50000.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-040397B8', '2025-11-13 04:02:07.491310', 'EFECTIVO_ARS', 'caca', '', 's', 'comprobantes/comprobante_POS-040397B8.pdf', 2, '2025-11-13 04:02:07.774856', 2, 2533.30, 1824.63, 'COMPLETADO', 11222.00, 10513.33, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-049D4502', '2025-11-13 07:17:04.318906', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-049D4502.pdf', 2, '2025-11-13 07:17:04.576610', NULL, 260794.50, 0.00, 'COMPLETADO', 1738630.00, 1477835.50, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-0E5CFD36', '2025-11-13 00:00:21.101847', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-0E5CFD36.pdf', 2, '2025-11-13 00:00:21.296106', NULL, 0.00, 0.00, 'COMPLETADO', 12222.00, 12222.00, 1, 'EFECTIVO_ARS', 1222.00, 11000.00, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-119A299D', '2025-11-12 18:07:21.145364', 'EFECTIVO_USD', '', '', '', 'comprobantes/comprobante_POS-119A299D.pdf', 2, '2025-11-12 18:07:21.190508', NULL, 12.00, 2097.48, 'COMPLETADO', 10000.00, 12085.48, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-130AD6CE', '2025-11-12 23:23:04.328608', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-130AD6CE.pdf', 2, '2025-11-12 23:23:04.632146', NULL, 0.00, 0.00, 'COMPLETADO', 121.00, 121.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-1AF59883', '2025-11-13 23:46:13.169168', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-1AF59883.pdf', 2, '2025-11-13 23:46:13.398718', NULL, 0.00, 0.00, 'COMPLETADO', 2122500.00, 2122500.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-1E7960FF', '2025-11-13 03:44:33.887235', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-1E7960FF.pdf', 2, '2025-11-13 03:44:34.102633', NULL, 0.00, 363117.30, 'COMPLETADO', 1729130.00, 2092247.30, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-20F0E7F3', '2025-11-13 07:23:37.277469', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-20F0E7F3.pdf', 2, '2025-11-13 07:23:37.458667', NULL, 0.00, 0.00, 'COMPLETADO', 9500.00, 9500.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-248DDA43', '2025-11-12 23:47:12.393869', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-248DDA43.pdf', 2, '2025-11-12 23:47:12.601363', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-298C6FD3', '2025-11-12 20:41:38.952500', 'TRANSFERENCIA', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-298C6FD3.pdf', 2, '2025-11-12 20:41:39.122907', 1, 1222.00, 1843.38, 'COMPLETADO', 10000.00, 10621.38, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-31A9A44D', '2025-11-13 18:23:20.234003', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-31A9A44D.pdf', 2, '2025-11-13 18:23:20.512273', NULL, 80909.55, 0.00, 'COMPLETADO', 122375.00, 41465.45, 1, 'TARJETA', 1222.00, 40426.75, 183.30, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-3650B009', '2025-11-12 23:54:24.248014', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-3650B009.pdf', 2, '2025-11-12 23:54:24.431187', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 1, 'EFECTIVO_ARS', 122.00, 9878.00, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-39941E37', '2025-11-12 22:07:47.675612', 'TRANSFERENCIA', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-39941E37.pdf', 2, '2025-11-12 22:07:47.844889', 1, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-3BABAE79', '2025-11-12 19:21:00.021769', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-3BABAE79.pdf', 2, '2025-11-12 19:21:00.158587', NULL, 6060606.00, 1272727.26, 'COMPLETADO', 12121212.00, 7333333.26, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-3CD519E6', '2025-11-21 17:20:01.774233', 'efectivo', '', '44360403', 'Emanuel Sosa', NULL, 2, '2025-11-21 14:20:01.778377', 7, 0.00, 0.00, 'COMPLETADO', 1.00, 1.00, 0, NULL, NULL, NULL, 0.00, NULL, 'local', 'pagado', 'retirado', '', 0.00, NULL),
('POS-3EEECD18', '2025-11-14 16:37:09.313901', 'EFECTIVO_ARS', 'Retirado por el Local a Consignacion ', '', 'Facundo Bastias', 'comprobantes/comprobante_POS-3EEECD18.pdf', 2, '2025-11-14 16:37:09.736437', 4, 0.00, 0.00, 'PENDIENTE_PAGO', 201860.00, 201860.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-41E8B8C7', '2025-11-13 05:27:20.990994', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-41E8B8C7.pdf', 2, '2025-11-13 05:27:21.142723', NULL, 975.00, 1160.25, 'CANCELADO', 6500.00, 6685.25, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-4B6258AE', '2025-11-12 18:41:40.039495', 'EFECTIVO_ARS', 'asdasd', '', '', 'comprobantes/comprobante_POS-4B6258AE.pdf', 2, '2025-11-12 18:41:40.155953', NULL, 12.00, 2097.48, 'COMPLETADO', 10000.00, 12085.48, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-553AE394', '2025-11-12 20:34:26.173955', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-553AE394.pdf', 2, '2025-11-12 20:34:26.326001', 1, 1200.00, 1848.00, 'COMPLETADO', 10000.00, 10648.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-56C4E11D', '2025-11-13 23:13:09.150122', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-56C4E11D.pdf', 2, '2025-11-13 23:13:09.409816', NULL, 0.00, 0.00, 'COMPLETADO', 2122501.00, 2122501.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-5773F459', '2025-11-13 06:50:19.659311', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-5773F459.pdf', 2, '2025-11-13 06:50:20.269159', NULL, 1425.00, 0.00, 'CANCELADO', 9500.00, 8075.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-5BEC9024', '2025-11-12 20:52:37.049452', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-5BEC9024.pdf', 2, '2025-11-12 20:52:37.258244', NULL, 12.00, 0.00, 'COMPLETADO', 1500.00, 1488.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-5D3E5CE4', '2025-11-12 20:25:57.543526', 'TARJETA', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-5D3E5CE4.pdf', 2, '2025-11-12 20:25:57.699048', 1, 35.00, 66.15, 'COMPLETADO', 350.00, 381.15, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-611E669B', '2025-11-13 23:12:47.308361', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-611E669B.pdf', 2, '2025-11-13 23:12:47.590545', NULL, 0.00, 0.00, 'COMPLETADO', 1.00, 1.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-6251D818', '2025-11-12 17:58:54.795182', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-6251D818.pdf', 2, '2025-11-12 17:58:54.866074', NULL, 12.00, 2097.48, 'COMPLETADO', 10000.00, 12085.48, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-65B108DF', '2025-11-12 21:38:39.249947', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-65B108DF.pdf', 2, '2025-11-12 21:38:39.400957', NULL, 1346.64, 2073.83, 'COMPLETADO', 11222.00, 11949.19, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-6B0D8096', '2025-11-15 00:57:54.260839', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-6B0D8096.pdf', 2, '2025-11-15 00:57:54.544811', NULL, 0.00, 444150.00, 'COMPLETADO', 2115000.00, 2559150.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-6B100E8F', '2025-11-13 18:27:06.712040', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-6B100E8F.pdf', 2, '2025-11-13 18:27:06.991148', 1, 0.00, 0.00, 'COMPLETADO', 1799181.74, 1799181.74, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-762454C2', '2025-11-13 19:44:22.118175', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-762454C2.pdf', 2, '2025-11-13 19:44:22.399872', NULL, 0.00, 0.00, 'COMPLETADO', 4990.00, 4990.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-796712CB', '2025-11-12 20:53:08.464769', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-796712CB.pdf', 2, '2025-11-12 20:53:08.597025', NULL, 0.00, 0.00, 'COMPLETADO', 1999.00, 1999.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-8D0BAA4A', '2025-11-13 04:02:47.967546', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-8D0BAA4A.pdf', 2, '2025-11-13 04:02:48.166005', NULL, 0.00, 0.00, 'COMPLETADO', 11.00, 11.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-90825F5D', '2025-11-12 21:36:40.280224', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-90825F5D.pdf', 2, '2025-11-12 21:36:40.452042', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-90E0619E', '2025-11-13 23:05:30.912430', 'EFECTIVO_ARS', '', '', 'caca', 'comprobantes/comprobante_POS-90E0619E.pdf', 2, '2025-11-13 23:05:31.214598', 3, 0.00, 0.00, 'COMPLETADO', 8.00, 8.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-92C3F826', '2025-11-12 23:09:49.886234', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-92C3F826.pdf', 2, '2025-11-12 23:09:50.056432', NULL, 0.00, 0.00, 'COMPLETADO', 21212.00, 21212.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-98BB15AC', '2025-11-13 19:52:34.409944', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-98BB15AC.pdf', 2, '2025-11-13 19:52:34.835277', 1, 41559.03, 49455.25, 'CANCELADO', 277060.23, 284956.45, 0, NULL, NULL, NULL, 41559.03, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-9EB7FA22', '2025-11-12 22:13:24.934916', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-9EB7FA22.pdf', 2, '2025-11-12 22:13:25.102620', NULL, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-A074FD78', '2025-11-13 05:33:48.483253', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-A074FD78.pdf', 2, '2025-11-13 05:33:48.634537', 1, 750.00, 10447.50, 'COMPLETADO', 50500.00, 60197.50, 1, 'TARJETA', 5000.00, 45500.00, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-A4518974', '2025-11-12 22:01:07.471405', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-A4518974.pdf', 2, '2025-11-12 22:01:07.610354', NULL, 0.00, 0.00, 'COMPLETADO', 20000.00, 20000.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-A518A580', '2025-11-13 06:18:20.885089', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-A518A580.pdf', 2, '2025-11-13 06:18:21.049358', NULL, 0.00, 0.00, 'COMPLETADO', 9990.00, 9990.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-ABFC278E', '2025-11-12 23:43:15.684592', 'EFECTIVO_ARS', 'COn funda', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-ABFC278E.pdf', 2, '2025-11-12 23:43:15.918130', 1, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 1, 'TRANSFERENCIA', 250000.00, 1479130.00, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-B00486BF', '2025-11-13 18:39:43.757209', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B00486BF.pdf', 2, '2025-11-13 18:39:44.022967', NULL, 0.00, 0.00, 'COMPLETADO', 17916.59, 17916.59, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-B0240418', '2025-11-12 20:00:17.929528', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B0240418.pdf', 2, '2025-11-12 20:00:18.038066', NULL, 1200.00, 1848.00, 'COMPLETADO', 10000.00, 10648.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-B627CAD1', '2025-11-12 18:14:47.961261', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B627CAD1.pdf', 2, '2025-11-12 18:14:48.098310', NULL, 0.00, 0.00, 'COMPLETADO', 12121212.00, 12121212.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-B80FE78F', '2025-11-12 22:21:27.655169', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-B80FE78F.pdf', 2, '2025-11-12 22:21:27.782262', NULL, 0.00, 2545454.52, 'COMPLETADO', 12121212.00, 14666666.52, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-BD33A466', '2025-11-21 17:17:37.143138', 'efectivo', '', '', 'Emanuel Sosa', NULL, 2, '2025-11-21 14:17:37.145581', 7, 0.00, 0.00, 'COMPLETADO', 3120004.00, 3120004.00, 0, NULL, NULL, NULL, 0.00, NULL, 'local', 'pagado', 'retirado', '', 0.00, NULL),
('POS-BE12561B', '2025-11-12 16:58:29.669824', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-BE12561B.pdf', 2, '2025-11-12 16:58:29.698736', NULL, 0.00, 0.00, 'COMPLETADO', 10000.00, 10000.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-C21BAE7C', '2025-11-12 21:58:46.683945', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-C21BAE7C.pdf', 2, '2025-11-12 21:58:46.858811', NULL, 0.00, 363117.30, 'COMPLETADO', 1729130.00, 2092247.30, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-CA846B38', '2025-11-13 18:50:39.142976', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-CA846B38.pdf', 2, '2025-11-13 18:50:39.396166', 1, 318375.00, 0.00, 'COMPLETADO', 2122500.00, 1804125.00, 0, NULL, NULL, NULL, 318375.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-CB216F2A', '2025-11-12 18:04:34.598211', 'EFECTIVO_ARS', 'ascasc', '', '', 'comprobantes/comprobante_POS-CB216F2A.pdf', 2, '2025-11-12 18:04:34.648647', NULL, 1200.00, 1848.00, 'COMPLETADO', 10000.00, 10648.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-CDE476D4', '2025-11-13 14:15:02.716818', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-CDE476D4.pdf', 2, '2025-11-13 14:15:02.956888', 1, 1425.00, 1695.75, 'COMPLETADO', 9500.00, 9770.75, 1, 'EFECTIVO_ARS', 3500.00, 6000.00, 1425.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-D485FC80', '2025-11-13 22:51:38.730466', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-D485FC80.pdf', 2, '2025-11-13 22:51:39.023980', NULL, 0.00, 0.00, 'COMPLETADO', 2122500.00, 2122500.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-D4BF06D2', '2025-11-13 07:42:42.517379', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-D4BF06D2.pdf', 2, '2025-11-13 07:42:42.701696', NULL, 840.00, 999.60, 'COMPLETADO', 5600.00, 5759.60, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-D990084C', '2025-11-12 23:41:57.742660', 'TRANSFERENCIA', 'hola asdasdasd', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-D990084C.pdf', 2, '2025-11-12 23:41:58.009839', 1, 0.00, 0.00, 'PENDIENTE_PAGO', 10000.00, 10000.00, 1, 'EFECTIVO_ARS', 1222.00, 8778.00, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-DF47FA7E', '2025-11-12 21:53:35.425668', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-DF47FA7E.pdf', 2, '2025-11-12 21:53:35.623968', NULL, 0.00, 0.00, 'COMPLETADO', 1729130.00, 1729130.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-ECB1CCF8', '2025-11-12 23:15:39.290686', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-ECB1CCF8.pdf', 2, '2025-11-12 23:15:39.505819', 1, 12.00, 2352.00, 'COMPLETADO', 11212.00, 13552.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-F5DB5517', '2025-11-12 20:10:17.624549', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-F5DB5517.pdf', 2, '2025-11-12 20:10:17.723034', 1, 11515163.40, 0.00, 'COMPLETADO', 12131212.00, 616048.60, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-F74FFB14', '2025-11-12 23:44:59.184877', 'EFECTIVO_ARS', '', '', '', 'comprobantes/comprobante_POS-F74FFB14.pdf', 2, '2025-11-12 23:44:59.357497', NULL, 0.00, 0.00, 'COMPLETADO', 1212.00, 1212.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('POS-FE370894', '2025-11-12 23:06:06.550541', 'EFECTIVO_ARS', '', '2665032890', 'Sosa Raul emanuel', 'comprobantes/comprobante_POS-FE370894.pdf', 2, '2025-11-12 23:06:06.703033', 1, 12.00, 0.00, 'COMPLETADO', 1300.00, 1288.00, 0, NULL, NULL, NULL, 0.00, NULL, 'POS', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('WEB-20251121144006', '2025-11-21 14:40:06.935033', 'EFECTIVO_ARS', '', '12', 'admin', '', 2, '2025-11-21 14:40:06.936185', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'WEB', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('WEB-20251121144630', '2025-11-21 14:46:30.483126', 'EFECTIVO_ARS', '', '', 'admin', '', 2, '2025-11-21 14:46:30.484574', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'WEB', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('WEB-20251121144652', '2025-11-21 14:46:52.112321', 'EFECTIVO_ARS', '', '', 'admin', '', 2, '2025-11-21 14:46:52.113354', NULL, 0.00, 0.00, 'PENDIENTE_PAGO', 0.00, 0.00, 0, NULL, NULL, NULL, 0.00, NULL, 'WEB', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('WEB-20251121150919', '2025-11-21 15:09:19.299853', 'TRANSFERENCIA', 'l😍asdfafs\n\n[ANULADA] por gil', '44360403', 'Emanuel Sosa', 'comprobantes/comprobante_WEB-20251121150919.pdf', 7, '2025-11-21 15:09:53.350778', NULL, 0.00, 0.00, 'CANCELADO', 3120003.00, 3120003.00, 0, NULL, NULL, NULL, 0.00, NULL, 'WEB', 'pendiente', 'pendiente', NULL, 0.00, NULL),
('WEB-251121160421-137', '2025-11-21 16:04:21.594068', 'efectivo', '', '44360403', 'Emanuel Sosa', NULL, 7, '2025-11-21 13:05:00.917817', 7, 0.00, 0.00, 'LISTO_RETIRAR', 6240009.00, 6240009.00, 0, NULL, NULL, NULL, 0.00, NULL, 'web', 'pendiente', 'pendiente', '', 0.00, NULL),
('WEB-251121164708-985', '2025-11-21 16:47:08.671763', 'efectivo', '', '44360403', 'Emanuel Sosa', NULL, 7, '2025-11-21 13:47:08.698026', 7, 0.00, 0.00, 'PENDIENTE_PAGO', 351250.00, 351250.00, 0, NULL, NULL, NULL, 0.00, NULL, 'web', 'pendiente', 'pendiente', '', 0.00, NULL),
('WEB-251121164842-385', '2025-11-21 16:48:42.469433', 'efectivo', '', '44360403', 'Emanuel Sosa', NULL, 7, '2025-11-21 13:48:42.489738', 7, 0.00, 0.00, 'PENDIENTE_PAGO', 351250.00, 351250.00, 0, NULL, NULL, NULL, 0.00, NULL, 'web', 'pendiente', 'pendiente', '', 0.00, NULL),
('WEB-251121170232-788', '2025-11-21 17:02:32.250807', 'efectivo', '', '44360403', 'Emanuel Sosa', NULL, 7, '2025-11-21 14:05:33.721577', 7, 0.00, 0.00, 'COMPLETADO', 351250.00, 351250.00, 0, NULL, NULL, NULL, 0.00, NULL, 'web', 'pendiente', 'pendiente', '', 0.00, NULL),
('WEB-251121170742-675', '2025-11-21 17:07:42.994760', 'efectivo', '', '44360403', 'Emanuel Sosa', NULL, 7, '2025-11-21 15:09:41.878004', 7, 0.00, 0.00, 'DEVUELTO', 6240000.00, 6240000.00, 0, NULL, NULL, NULL, 0.00, '', 'web', 'pendiente', 'pendiente', '', 0.00, NULL),
('WEB-251121200341-751', '2025-11-21 20:03:41.963735', 'transferencia', '', '44360403', 'Emanuel Sosa', NULL, 7, '2025-11-21 17:04:42.733052', 7, 0.00, 0.00, 'PENDIENTE_ARMADO', 1560001.00, 1560001.00, 0, NULL, NULL, NULL, 0.00, NULL, 'web', 'pendiente', 'pendiente', '', 0.00, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asistente_ia_assistantknowledgearticle`
--
ALTER TABLE `asistente_ia_assistantknowledgearticle`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `asistente_ia_assistantplaybook`
--
ALTER TABLE `asistente_ia_assistantplaybook`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `asistente_ia_assistantquickreply`
--
ALTER TABLE `asistente_ia_assistantquickreply`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `asistente_ia_conversationmessage`
--
ALTER TABLE `asistente_ia_conversationmessage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `asistente_ia_convers_thread_id_db7f5658_fk_asistente` (`thread_id`);

--
-- Indices de la tabla `asistente_ia_conversationthread`
--
ALTER TABLE `asistente_ia_conversationthread`
  ADD PRIMARY KEY (`id`),
  ADD KEY `asistente_ia_convers_usuario_id_456ba82a_fk_auth_user` (`usuario_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `caja_cajadiaria`
--
ALTER TABLE `caja_cajadiaria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_caja_local_estado` (`local_id`,`estado`),
  ADD KEY `idx_caja_fecha` (`fecha_apertura`),
  ADD KEY `caja_cajadiaria_usuario_apertura_id_3670adb1_fk_auth_user_id` (`usuario_apertura_id`);

--
-- Indices de la tabla `caja_movimientocaja`
--
ALTER TABLE `caja_movimientocaja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_mov_caja_tipo` (`caja_diaria_id`,`tipo`),
  ADD KEY `idx_mov_venta` (`venta_asociada_id`),
  ADD KEY `caja_movimientocaja_usuario_id_788e149a_fk_auth_user_id` (`usuario_id`);

--
-- Indices de la tabla `configuracion_configuracionsistema`
--
ALTER TABLE `configuracion_configuracionsistema`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `configuracion_configuraciontienda`
--
ALTER TABLE `configuracion_configuraciontienda`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `configuracion_escalapreciomayorista`
--
ALTER TABLE `configuracion_escalapreciomayorista`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_escala_config` (`configuracion_id`),
  ADD KEY `configuraci_configu_0bb6c8_idx` (`configuracion_id`,`activo`,`orden`),
  ADD KEY `configuraci_cantida_64b3cf_idx` (`cantidad_minima`,`cantidad_maxima`);

--
-- Indices de la tabla `configuracion_escalapreciomayorista_categorias`
--
ALTER TABLE `configuracion_escalapreciomayorista_categorias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `configuracion_escalaprec_escalapreciomayorista_id_0089b61f_uniq` (`escalapreciomayorista_id`,`categoria_id`),
  ADD KEY `configuracion_escala_categoria_id_d1e116db_fk_inventari` (`categoria_id`);

--
-- Indices de la tabla `configuracion_preferenciausuario`
--
ALTER TABLE `configuracion_preferenciausuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `core_direccionenvio`
--
ALTER TABLE `core_direccionenvio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_direccionenvio_usuario_id_686668d4_fk_auth_user_id` (`usuario_id`);

--
-- Indices de la tabla `core_favorito`
--
ALTER TABLE `core_favorito`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_favorito_usuario_id_variante_id_da7103d6_uniq` (`usuario_id`,`variante_id`),
  ADD KEY `core_favorito_variante_id_13417d3b_fk_inventari` (`variante_id`);

--
-- Indices de la tabla `core_notificacioninterna`
--
ALTER TABLE `core_notificacioninterna`
  ADD PRIMARY KEY (`id`),
  ADD KEY `leida_por_id` (`leida_por_id`),
  ADD KEY `idx_leida_creada` (`leida`,`creada`),
  ADD KEY `idx_tipo_creada` (`tipo`,`creada`);

--
-- Indices de la tabla `core_perfilusuario`
--
ALTER TABLE `core_perfilusuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `core_solicitudmayorista`
--
ALTER TABLE `core_solicitudmayorista`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_solicitudmayorista_revisado_por_id_382071e5_fk_auth_user_id` (`revisado_por_id`);

--
-- Indices de la tabla `crm_cliente`
--
ALTER TABLE `crm_cliente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `telefono` (`telefono`);

--
-- Indices de la tabla `crm_clientecontexto`
--
ALTER TABLE `crm_clientecontexto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cliente_id` (`cliente_id`);

--
-- Indices de la tabla `crm_conversacion`
--
ALTER TABLE `crm_conversacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `crm_conversacion_asesor_asignado_id_b38461f1_fk_auth_user_id` (`asesor_asignado_id`),
  ADD KEY `crm_conversacion_cliente_id_6d9bafb1_fk_crm_cliente_id` (`cliente_id`);

--
-- Indices de la tabla `crm_conversacion_etiquetas`
--
ALTER TABLE `crm_conversacion_etiquetas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `crm_conversacion_etiquet_conversacion_id_etiqueta_e3e8c740_uniq` (`conversacion_id`,`etiqueta_id`),
  ADD KEY `crm_conversacion_eti_etiqueta_id_9048b1b9_fk_crm_etiqu` (`etiqueta_id`);

--
-- Indices de la tabla `crm_cotizacion`
--
ALTER TABLE `crm_cotizacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `crm_cotizacion_cliente_id_77934741_fk_crm_cliente_id` (`cliente_id`),
  ADD KEY `crm_cotizacion_conversacion_id_56749d32_fk_crm_conversacion_id` (`conversacion_id`),
  ADD KEY `crm_cotizacion_venta_relacionada_id_690d174b_fk_ventas_venta_id` (`venta_relacionada_id`);

--
-- Indices de la tabla `crm_etiqueta`
--
ALTER TABLE `crm_etiqueta`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `crm_mensaje`
--
ALTER TABLE `crm_mensaje`
  ADD PRIMARY KEY (`id`),
  ADD KEY `crm_mensaje_conversacion_id_4226bb24_fk_crm_conversacion_id` (`conversacion_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `historial_registrohistorial`
--
ALTER TABLE `historial_registrohistorial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `historial_registrohistorial_usuario_id_ccace41c_fk_auth_user_id` (`usuario_id`);

--
-- Indices de la tabla `inventario_categoria`
--
ALTER TABLE `inventario_categoria`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_categoria_nombre_parent` (`nombre`,`parent_id`),
  ADD KEY `idx_categoria_nombre` (`nombre`),
  ADD KEY `idx_categoria_parent` (`parent_id`);

--
-- Indices de la tabla `inventario_detalleiphone`
--
ALTER TABLE `inventario_detalleiphone`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `variante_id` (`variante_id`),
  ADD UNIQUE KEY `imei` (`imei`);

--
-- Indices de la tabla `inventario_plancanjetransaccion`
--
ALTER TABLE `inventario_plancanjetransaccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_plancanje_detalle_iphone_recib_c6e63b68_fk_inventari` (`detalle_iphone_recibido_id`),
  ADD KEY `inventario_plancanje_iphone_entregado_id_ae5bd27f_fk_inventari` (`iphone_entregado_id`),
  ADD KEY `inventario_plancanje_vendedor_id_d1fcc04e_fk_auth_user` (`vendedor_id`),
  ADD KEY `inventario_plancanje_venta_asociada_id_69fed8c1_fk_ventas_ve` (`venta_asociada_id`),
  ADD KEY `idx_canje_fecha` (`fecha`),
  ADD KEY `idx_canje_cliente` (`cliente_id`);

--
-- Indices de la tabla `inventario_precio`
--
ALTER TABLE `inventario_precio`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inventario_precio_variante_id_tipo_precio_moneda_0026b93e_uniq` (`variante_id`,`tipo_precio`,`moneda`),
  ADD KEY `inventario_precio_variante_id_28e3c002` (`variante_id`),
  ADD KEY `idx_precio_activo` (`activo`),
  ADD KEY `idx_precio_var_tipo_mon` (`variante_id`,`tipo`,`moneda`);

--
-- Indices de la tabla `inventario_producto`
--
ALTER TABLE `inventario_producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_producto_proveedor_id_2feee190_fk_inventari` (`proveedor_id`),
  ADD KEY `inventario_producto_categoria_id_7033fb47_fk_inventari` (`categoria_id`),
  ADD KEY `idx_producto_codigo_barras` (`codigo_barras`),
  ADD KEY `idx_producto_activo` (`activo`),
  ADD KEY `idx_producto_nombre` (`nombre`),
  ADD KEY `idx_producto_cod_barras` (`codigo_barras`);

--
-- Indices de la tabla `inventario_productoimagen`
--
ALTER TABLE `inventario_productoimagen`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_productoi_producto_id_dc6f4534_fk_inventari` (`producto_id`);

--
-- Indices de la tabla `inventario_productovariante`
--
ALTER TABLE `inventario_productovariante`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inventario_productovaria_producto_id_nombre_varia_9e2b3846_uniq` (`producto_id`,`nombre_variante`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD UNIQUE KEY `codigo_barras` (`codigo_barras`),
  ADD KEY `idx_var_sku` (`sku`),
  ADD KEY `idx_var_activo` (`activo`),
  ADD KEY `idx_var_stock` (`stock_actual`);

--
-- Indices de la tabla `inventario_proveedor`
--
ALTER TABLE `inventario_proveedor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD KEY `idx_proveedor_activo` (`activo`),
  ADD KEY `idx_proveedor_nombre` (`nombre`);

--
-- Indices de la tabla `locales_local`
--
ALTER TABLE `locales_local`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `ventas_carritoremoto`
--
ALTER TABLE `ventas_carritoremoto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `ventas_cupon`
--
ALTER TABLE `ventas_cupon`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `ventas_detalleventa`
--
ALTER TABLE `ventas_detalleventa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ventas_detalleventa_venta_id_c370bcd7_fk_ventas_venta_id` (`venta_id`),
  ADD KEY `ventas_detalleventa_variante_id_67772d78_fk_inventari` (`variante_id`);

--
-- Indices de la tabla `ventas_historialestadoventa`
--
ALTER TABLE `ventas_historialestadoventa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` (`usuario_id`),
  ADD KEY `ventas_hist_venta_i_65b196_idx` (`venta_id`,`creado`);

--
-- Indices de la tabla `ventas_solicitudimpresion`
--
ALTER TABLE `ventas_solicitudimpresion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ventas_solicitudimpresion_usuario_id_eb5afc53_fk_auth_user_id` (`usuario_id`),
  ADD KEY `ventas_solicitudimpresion_venta_id_0965f3de_fk_ventas_venta_id` (`venta_id`);

--
-- Indices de la tabla `ventas_venta`
--
ALTER TABLE `ventas_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ventas_venta_vendedor_id_2f6b0d76_fk_auth_user_id` (`vendedor_id`),
  ADD KEY `ventas_venta_cliente_id_85f33a80_fk_crm_cliente_id` (`cliente_id`),
  ADD KEY `ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id` (`cupon_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asistente_ia_assistantknowledgearticle`
--
ALTER TABLE `asistente_ia_assistantknowledgearticle`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `asistente_ia_assistantplaybook`
--
ALTER TABLE `asistente_ia_assistantplaybook`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `asistente_ia_assistantquickreply`
--
ALTER TABLE `asistente_ia_assistantquickreply`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistente_ia_conversationmessage`
--
ALTER TABLE `asistente_ia_conversationmessage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `asistente_ia_conversationthread`
--
ALTER TABLE `asistente_ia_conversationthread`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=185;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `caja_cajadiaria`
--
ALTER TABLE `caja_cajadiaria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `caja_movimientocaja`
--
ALTER TABLE `caja_movimientocaja`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `configuracion_configuracionsistema`
--
ALTER TABLE `configuracion_configuracionsistema`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `configuracion_configuraciontienda`
--
ALTER TABLE `configuracion_configuraciontienda`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `configuracion_escalapreciomayorista`
--
ALTER TABLE `configuracion_escalapreciomayorista`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `configuracion_escalapreciomayorista_categorias`
--
ALTER TABLE `configuracion_escalapreciomayorista_categorias`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `configuracion_preferenciausuario`
--
ALTER TABLE `configuracion_preferenciausuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `core_direccionenvio`
--
ALTER TABLE `core_direccionenvio`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `core_favorito`
--
ALTER TABLE `core_favorito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `core_notificacioninterna`
--
ALTER TABLE `core_notificacioninterna`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `core_perfilusuario`
--
ALTER TABLE `core_perfilusuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `core_solicitudmayorista`
--
ALTER TABLE `core_solicitudmayorista`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `crm_cliente`
--
ALTER TABLE `crm_cliente`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `crm_clientecontexto`
--
ALTER TABLE `crm_clientecontexto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `crm_conversacion`
--
ALTER TABLE `crm_conversacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `crm_conversacion_etiquetas`
--
ALTER TABLE `crm_conversacion_etiquetas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `crm_cotizacion`
--
ALTER TABLE `crm_cotizacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `crm_etiqueta`
--
ALTER TABLE `crm_etiqueta`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `crm_mensaje`
--
ALTER TABLE `crm_mensaje`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=191;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT de la tabla `historial_registrohistorial`
--
ALTER TABLE `historial_registrohistorial`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=118;

--
-- AUTO_INCREMENT de la tabla `inventario_categoria`
--
ALTER TABLE `inventario_categoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_detalleiphone`
--
ALTER TABLE `inventario_detalleiphone`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_plancanjeconfig`
--
ALTER TABLE `inventario_plancanjeconfig`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_plancanjetransaccion`
--
ALTER TABLE `inventario_plancanjetransaccion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_precio`
--
ALTER TABLE `inventario_precio`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=451;

--
-- AUTO_INCREMENT de la tabla `inventario_producto`
--
ALTER TABLE `inventario_producto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=396;

--
-- AUTO_INCREMENT de la tabla `inventario_productoimagen`
--
ALTER TABLE `inventario_productoimagen`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_productovariante`
--
ALTER TABLE `inventario_productovariante`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_proveedor`
--
ALTER TABLE `inventario_proveedor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `locales_local`
--
ALTER TABLE `locales_local`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `ventas_carritoremoto`
--
ALTER TABLE `ventas_carritoremoto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `ventas_cupon`
--
ALTER TABLE `ventas_cupon`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `ventas_detalleventa`
--
ALTER TABLE `ventas_detalleventa`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ventas_historialestadoventa`
--
ALTER TABLE `ventas_historialestadoventa`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `ventas_solicitudimpresion`
--
ALTER TABLE `ventas_solicitudimpresion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistente_ia_conversationmessage`
--
ALTER TABLE `asistente_ia_conversationmessage`
  ADD CONSTRAINT `asistente_ia_convers_thread_id_db7f5658_fk_asistente` FOREIGN KEY (`thread_id`) REFERENCES `asistente_ia_conversationthread` (`id`);

--
-- Filtros para la tabla `asistente_ia_conversationthread`
--
ALTER TABLE `asistente_ia_conversationthread`
  ADD CONSTRAINT `asistente_ia_convers_usuario_id_456ba82a_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `caja_cajadiaria`
--
ALTER TABLE `caja_cajadiaria`
  ADD CONSTRAINT `caja_cajadiaria_local_id_425ca589_fk_locales_local_id` FOREIGN KEY (`local_id`) REFERENCES `locales_local` (`id`),
  ADD CONSTRAINT `caja_cajadiaria_usuario_apertura_id_3670adb1_fk_auth_user_id` FOREIGN KEY (`usuario_apertura_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `caja_movimientocaja`
--
ALTER TABLE `caja_movimientocaja`
  ADD CONSTRAINT `caja_movimientocaja_caja_diaria_id_0363354b_fk_caja_caja` FOREIGN KEY (`caja_diaria_id`) REFERENCES `caja_cajadiaria` (`id`),
  ADD CONSTRAINT `caja_movimientocaja_usuario_id_788e149a_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `caja_movimientocaja_venta_asociada_id_6098e59a_fk_ventas_ve` FOREIGN KEY (`venta_asociada_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `configuracion_escalapreciomayorista`
--
ALTER TABLE `configuracion_escalapreciomayorista`
  ADD CONSTRAINT `configuracion_escalapreciomayorista_ibfk_1` FOREIGN KEY (`configuracion_id`) REFERENCES `configuracion_configuracionsistema` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `configuracion_escalapreciomayorista_categorias`
--
ALTER TABLE `configuracion_escalapreciomayorista_categorias`
  ADD CONSTRAINT `configuracion_escala_categoria_id_d1e116db_fk_inventari` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`),
  ADD CONSTRAINT `configuracion_escala_escalapreciomayorist_84717e6f_fk_configura` FOREIGN KEY (`escalapreciomayorista_id`) REFERENCES `configuracion_escalapreciomayorista` (`id`);

--
-- Filtros para la tabla `configuracion_preferenciausuario`
--
ALTER TABLE `configuracion_preferenciausuario`
  ADD CONSTRAINT `configuracion_prefer_usuario_id_333b55ea_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `core_direccionenvio`
--
ALTER TABLE `core_direccionenvio`
  ADD CONSTRAINT `core_direccionenvio_usuario_id_686668d4_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `core_favorito`
--
ALTER TABLE `core_favorito`
  ADD CONSTRAINT `core_favorito_usuario_id_e381b6ab_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_favorito_variante_id_13417d3b_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`);

--
-- Filtros para la tabla `core_notificacioninterna`
--
ALTER TABLE `core_notificacioninterna`
  ADD CONSTRAINT `core_notificacioninterna_ibfk_1` FOREIGN KEY (`leida_por_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `core_perfilusuario`
--
ALTER TABLE `core_perfilusuario`
  ADD CONSTRAINT `core_perfilusuario_usuario_id_c2ee2ea4_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `core_solicitudmayorista`
--
ALTER TABLE `core_solicitudmayorista`
  ADD CONSTRAINT `core_solicitudmayorista_revisado_por_id_382071e5_fk_auth_user_id` FOREIGN KEY (`revisado_por_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `crm_clientecontexto`
--
ALTER TABLE `crm_clientecontexto`
  ADD CONSTRAINT `crm_clientecontexto_cliente_id_e7e1a085_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`);

--
-- Filtros para la tabla `crm_conversacion`
--
ALTER TABLE `crm_conversacion`
  ADD CONSTRAINT `crm_conversacion_asesor_asignado_id_b38461f1_fk_auth_user_id` FOREIGN KEY (`asesor_asignado_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `crm_conversacion_cliente_id_6d9bafb1_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`);

--
-- Filtros para la tabla `crm_conversacion_etiquetas`
--
ALTER TABLE `crm_conversacion_etiquetas`
  ADD CONSTRAINT `crm_conversacion_eti_conversacion_id_9d07f708_fk_crm_conve` FOREIGN KEY (`conversacion_id`) REFERENCES `crm_conversacion` (`id`),
  ADD CONSTRAINT `crm_conversacion_eti_etiqueta_id_9048b1b9_fk_crm_etiqu` FOREIGN KEY (`etiqueta_id`) REFERENCES `crm_etiqueta` (`id`);

--
-- Filtros para la tabla `crm_cotizacion`
--
ALTER TABLE `crm_cotizacion`
  ADD CONSTRAINT `crm_cotizacion_cliente_id_77934741_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`),
  ADD CONSTRAINT `crm_cotizacion_conversacion_id_56749d32_fk_crm_conversacion_id` FOREIGN KEY (`conversacion_id`) REFERENCES `crm_conversacion` (`id`),
  ADD CONSTRAINT `crm_cotizacion_venta_relacionada_id_690d174b_fk_ventas_venta_id` FOREIGN KEY (`venta_relacionada_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `crm_mensaje`
--
ALTER TABLE `crm_mensaje`
  ADD CONSTRAINT `crm_mensaje_conversacion_id_4226bb24_fk_crm_conversacion_id` FOREIGN KEY (`conversacion_id`) REFERENCES `crm_conversacion` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `historial_registrohistorial`
--
ALTER TABLE `historial_registrohistorial`
  ADD CONSTRAINT `historial_registrohistorial_usuario_id_ccace41c_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `inventario_categoria`
--
ALTER TABLE `inventario_categoria`
  ADD CONSTRAINT `inventario_categoria_parent_id_ca5d5e55_fk_inventari` FOREIGN KEY (`parent_id`) REFERENCES `inventario_categoria` (`id`);

--
-- Filtros para la tabla `inventario_detalleiphone`
--
ALTER TABLE `inventario_detalleiphone`
  ADD CONSTRAINT `inventario_detalleip_variante_id_aea6e6f8_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`);

--
-- Filtros para la tabla `inventario_plancanjetransaccion`
--
ALTER TABLE `inventario_plancanjetransaccion`
  ADD CONSTRAINT `inventario_plancanje_cliente_id_417bc6c0_fk_crm_clien` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`),
  ADD CONSTRAINT `inventario_plancanje_detalle_iphone_recib_c6e63b68_fk_inventari` FOREIGN KEY (`detalle_iphone_recibido_id`) REFERENCES `inventario_detalleiphone` (`id`),
  ADD CONSTRAINT `inventario_plancanje_iphone_entregado_id_ae5bd27f_fk_inventari` FOREIGN KEY (`iphone_entregado_id`) REFERENCES `inventario_productovariante` (`id`),
  ADD CONSTRAINT `inventario_plancanje_vendedor_id_d1fcc04e_fk_auth_user` FOREIGN KEY (`vendedor_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `inventario_plancanje_venta_asociada_id_69fed8c1_fk_ventas_ve` FOREIGN KEY (`venta_asociada_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `inventario_precio`
--
ALTER TABLE `inventario_precio`
  ADD CONSTRAINT `inventario_precio_variante_id_28e3c002_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`);

--
-- Filtros para la tabla `inventario_producto`
--
ALTER TABLE `inventario_producto`
  ADD CONSTRAINT `inventario_producto_categoria_id_7033fb47_fk_inventari` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`),
  ADD CONSTRAINT `inventario_producto_proveedor_id_2feee190_fk_inventari` FOREIGN KEY (`proveedor_id`) REFERENCES `inventario_proveedor` (`id`);

--
-- Filtros para la tabla `inventario_productoimagen`
--
ALTER TABLE `inventario_productoimagen`
  ADD CONSTRAINT `inventario_productoi_producto_id_dc6f4534_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`);

--
-- Filtros para la tabla `inventario_productovariante`
--
ALTER TABLE `inventario_productovariante`
  ADD CONSTRAINT `inventario_productov_producto_id_23032fd0_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`);

--
-- Filtros para la tabla `ventas_carritoremoto`
--
ALTER TABLE `ventas_carritoremoto`
  ADD CONSTRAINT `ventas_carritoremoto_usuario_id_ab0111ac_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `ventas_detalleventa`
--
ALTER TABLE `ventas_detalleventa`
  ADD CONSTRAINT `ventas_detalleventa_variante_id_67772d78_fk_inventari` FOREIGN KEY (`variante_id`) REFERENCES `inventario_productovariante` (`id`),
  ADD CONSTRAINT `ventas_detalleventa_venta_id_c370bcd7_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `ventas_historialestadoventa`
--
ALTER TABLE `ventas_historialestadoventa`
  ADD CONSTRAINT `ventas_historialestadoventa_usuario_id_e969538d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `ventas_historialestadoventa_venta_id_4f46ae91_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `ventas_solicitudimpresion`
--
ALTER TABLE `ventas_solicitudimpresion`
  ADD CONSTRAINT `ventas_solicitudimpresion_usuario_id_eb5afc53_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `ventas_solicitudimpresion_venta_id_0965f3de_fk_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `ventas_venta`
--
ALTER TABLE `ventas_venta`
  ADD CONSTRAINT `ventas_venta_cliente_id_85f33a80_fk_crm_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `crm_cliente` (`id`),
  ADD CONSTRAINT `ventas_venta_cupon_id_53a5a689_fk_ventas_cupon_id` FOREIGN KEY (`cupon_id`) REFERENCES `ventas_cupon` (`id`),
  ADD CONSTRAINT `ventas_venta_vendedor_id_2f6b0d76_fk_auth_user_id` FOREIGN KEY (`vendedor_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
