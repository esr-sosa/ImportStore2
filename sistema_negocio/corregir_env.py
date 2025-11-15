"""
Script para corregir automáticamente el archivo .env
Elimina variables duplicadas y corrige comillas
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

print("=" * 70)
print("CORRECCION DEL ARCHIVO .env")
print("=" * 70)
print()

if not env_path.exists():
    print("[ERROR] El archivo .env no existe!")
    exit(1)

# Leer el archivo
with open(env_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Archivo leido: {len(lines)} lineas")
print()

# Procesar lineas
seen_vars = {}  # Para rastrear qué variables ya vimos
new_lines = []
whatsapp_vars = {
    'WHATSAPP_ACCESS_TOKEN': None,
    'WHATSAPP_PHONE_NUMBER_ID': None,
    'WHATSAPP_VERIFY_TOKEN': None,
}

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    
    # Si la linea tiene un comentario pero también tiene una variable, separarla
    if '#' in line and '=' in line:
        # Buscar si hay una variable de WhatsApp en cualquier parte de la linea
        for var_name in ['WHATSAPP_ACCESS_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'WHATSAPP_VERIFY_TOKEN']:
            if var_name in line:
                # Buscar el patrón VARIABLE=valor (puede estar antes o después del #)
                pattern = rf'{var_name}\s*=\s*([^\s#]+)'
                match = re.search(pattern, line)
                if match:
                    var_value = match.group(1).strip()
                    # Quitar comillas si las tiene
                    if var_value.startswith('"') and var_value.endswith('"'):
                        var_value = var_value[1:-1]
                    elif var_value.startswith("'") and var_value.endswith("'"):
                        var_value = var_value[1:-1]
                    # Guardar la variable
                    if var_value and (var_name not in seen_vars or not seen_vars[var_name]):
                        whatsapp_vars[var_name] = var_value
                        seen_vars[var_name] = True
                        print(f"[OK] Linea {i}: {var_name} encontrado (estaba en comentario) = {var_value[:30]}...")
                # No procesar esta linea más, ya la extrajimos
                continue
    
    # Mantener lineas vacias y comentarios puros
    if not stripped or (stripped.startswith('#') and '=' not in stripped):
        new_lines.append(line)
        continue
    
    # Buscar patron VARIABLE=valor
    match = re.match(r'^([A-Z_]+)\s*=\s*(.*)$', stripped)
    if match:
        var_name = match.group(1)
        var_value = match.group(2).strip()
        
        # Quitar comillas si las tiene
        if var_value.startswith('"') and var_value.endswith('"'):
            var_value = var_value[1:-1]
        elif var_name.startswith("'") and var_value.endswith("'"):
            var_value = var_value[1:-1]
        
        # Si es una variable de WhatsApp, guardarla
        if var_name in whatsapp_vars:
            # Solo guardar si tiene valor y no la hemos visto antes con valor
            if var_value and (var_name not in seen_vars or not seen_vars[var_name]):
                whatsapp_vars[var_name] = var_value
                seen_vars[var_name] = True
                print(f"[OK] Linea {i}: {var_name} = {var_value[:30]}...")
            elif not var_value:
                print(f"[VACIA] Linea {i}: {var_name} está vacía (se ignorará)")
            else:
                print(f"[DUPLICADA] Linea {i}: {var_name} duplicada (se ignorará)")
            # No agregar esta linea, la agregaremos al final
            continue
        else:
            # Otras variables: agregar si no está duplicada
            if var_name not in seen_vars:
                seen_vars[var_name] = True
                new_lines.append(f"{var_name}={var_value}\n")
            else:
                print(f"[DUPLICADA] Linea {i}: {var_name} duplicada (se ignorará)")
    else:
        # Linea que no coincide con el patrón, mantenerla
        new_lines.append(line)

print()
print("-" * 70)
print("AGREGANDO VARIABLES DE WHATSAPP CORREGIDAS:")
print()

# Agregar las variables de WhatsApp al final (sin duplicados)
for var_name, var_value in whatsapp_vars.items():
    if var_value:
        new_lines.append(f"{var_name}={var_value}\n")
        print(f"[OK] {var_name}={var_value[:50]}...")
    else:
        # Si no tiene valor, usar el valor por defecto para VERIFY_TOKEN
        if var_name == 'WHATSAPP_VERIFY_TOKEN':
            new_lines.append(f"{var_name}=importstore_token_secreto_123\n")
            print(f"[OK] {var_name}=importstore_token_secreto_123 (valor por defecto)")
        else:
            print(f"[FALTA] {var_name} no tiene valor configurado")

print()
print("-" * 70)
print("GUARDANDO ARCHIVO CORREGIDO...")
print()

# Hacer backup
backup_path = env_path.with_suffix('.env.backup')
with open(backup_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"[OK] Backup guardado en: {backup_path}")

# Guardar archivo corregido
with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"[OK] Archivo .env corregido y guardado")
print()
print("=" * 70)
print("[LISTO] Ahora reinicia el servidor Django para que tome los cambios.")
print("=" * 70)

