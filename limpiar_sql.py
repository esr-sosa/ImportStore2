#!/usr/bin/env python3
"""
Script para limpiar el SQL y arreglar errores de sintaxis
"""
import re

# Leer el archivo SQL
with open('sistema_negocio.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Arreglar el error en la línea 1662: DEFAULT _utf8mb4 -> DEFAULT '{}'
content = content.replace(
    "`descuentos_botones` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT _utf8mb4\n) ;",
    "`descuentos_botones` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '{}'\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
)

# 2. Agregar IF NOT EXISTS a todas las CREATE TABLE
content = re.sub(
    r'CREATE TABLE `([^`]+)`',
    r'CREATE TABLE IF NOT EXISTS `\1`',
    content
)

# 3. Arreglar tablas que terminan solo con ) ; (sin ENGINE)
# Buscar patrones como:
#   ...
#   `campo` tipo
# ) ;
#
# Y reemplazarlos con:
#   ...
#   `campo` tipo
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

# Primero, arreglar inventario_productoimagen
content = content.replace(
    "  `producto_id` bigint(20) NOT NULL\n) ;",
    "  `producto_id` bigint(20) NOT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
)

# Arreglar ventas_detalleventa
content = content.replace(
    "  `tipo_cambio_usado` decimal(10,2) DEFAULT NULL\n) ;",
    "  `tipo_cambio_usado` decimal(10,2) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
)

# 4. Buscar y arreglar cualquier otra tabla que termine con ) ; sin ENGINE
# Usar regex para encontrar líneas que terminan con ) ; y no tienen ENGINE en las siguientes líneas
lines = content.split('\n')
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Si la línea termina con ) ; y no es parte de un comentario
    if line.strip().endswith(') ;') and not line.strip().startswith('--'):
        # Verificar las siguientes 3 líneas para ver si hay ENGINE
        next_lines = '\n'.join(lines[i+1:min(i+4, len(lines))])
        if 'ENGINE' not in next_lines and 'RELACIONES' not in next_lines and 'Volcado' not in next_lines:
            # Reemplazar ) ; con ENGINE
            fixed_lines.append(line.replace(') ;', ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'))
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)
    i += 1

content = '\n'.join(fixed_lines)

# 5. Cambiar el nombre de la base de datos de sistema_negocio a railway
content = content.replace('`sistema_negocio`', '`railway`')
content = content.replace("Base de datos: `sistema_negocio`", "Base de datos: `railway`")

# Guardar el archivo limpio
with open('sistema_negocio_limpio.sql', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ SQL limpiado y guardado en sistema_negocio_limpio.sql')
print('📝 Cambios realizados:')
print('   - Agregado IF NOT EXISTS a todas las CREATE TABLE (evita errores de tablas duplicadas)')
print('   - Arreglado error de sintaxis en inventario_plancanjeconfig (DEFAULT _utf8mb4 -> DEFAULT \'{}\')')
print('   - Agregado ENGINE=InnoDB a tablas que no lo tenían')
print('   - Cambiado nombre de base de datos de sistema_negocio a railway')
print('')
print('💡 Ahora puedes importar sistema_negocio_limpio.sql en MySQL Workbench')

