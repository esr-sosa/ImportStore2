"""
Script para diagnosticar problemas con el archivo .env
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

print("=" * 70)
print("DIAGNOSTICO DEL ARCHIVO .env")
print("=" * 70)
print()
print(f"Archivo: {env_path}")
print(f"Existe: {env_path.exists()}")
print()

if env_path.exists():
    print("Leyendo contenido del archivo...")
    print("-" * 70)
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Total de lineas: {len(lines)}")
        print()
        
        whatsapp_lines = []
        for i, line in enumerate(lines, 1):
            # Buscar lineas relacionadas con WhatsApp
            if 'WHATSAPP' in line.upper():
                whatsapp_lines.append((i, line))
                # Mostrar la linea con caracteres visibles
                clean_line = repr(line)
                print(f"Linea {i}: {clean_line}")
        
        print()
        print("-" * 70)
        print("ANALISIS DE LINEAS DE WHATSAPP:")
        print()
        
        for line_num, line in whatsapp_lines:
            # Verificar si tiene el formato correcto
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                print(f"Linea {line_num}: [COMENTARIO O VACIA] - {repr(line)}")
                continue
            
            # Buscar el patrón VARIABLE=valor
            match = re.match(r'^([A-Z_]+)\s*=\s*(.*)$', stripped)
            if match:
                var_name = match.group(1)
                var_value = match.group(2)
                
                # Verificar si el valor está vacío
                if not var_value or var_value.strip() == '':
                    print(f"Linea {line_num}: [VACIA] {var_name}= (sin valor)")
                else:
                    # Mostrar primeros caracteres del valor
                    display_value = var_value[:30] + "..." if len(var_value) > 30 else var_value
                    print(f"Linea {line_num}: [OK] {var_name}={display_value}")
                    
                    # Verificar espacios problemáticos
                    if var_value.startswith(' ') or var_value.endswith(' '):
                        print(f"         [ADVERTENCIA] El valor tiene espacios al inicio o final")
                    if '"' in var_value or "'" in var_value:
                        print(f"         [ADVERTENCIA] El valor tiene comillas (no debería tenerlas)")
            else:
                print(f"Linea {line_num}: [FORMATO INCORRECTO] - {repr(line)}")
        
        print()
        print("=" * 70)
        print("RECOMENDACIONES:")
        print()
        
        # Verificar específicamente WHATSAPP_VERIFY_TOKEN
        verify_token_found = False
        for line_num, line in whatsapp_lines:
            if 'WHATSAPP_VERIFY_TOKEN' in line.upper():
                verify_token_found = True
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    print(f"❌ WHATSAPP_VERIFY_TOKEN está comentado o vacío en la linea {line_num}")
                else:
                    match = re.match(r'^WHATSAPP_VERIFY_TOKEN\s*=\s*(.*)$', stripped, re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                        if not value:
                            print(f"❌ WHATSAPP_VERIFY_TOKEN está definido pero sin valor en la linea {line_num}")
                            print(f"   Debería ser: WHATSAPP_VERIFY_TOKEN=importstore_token_secreto_123")
                        elif value != "importstore_token_secreto_123":
                            print(f"⚠️  WHATSAPP_VERIFY_TOKEN tiene un valor diferente: {value[:30]}")
                            print(f"   Debería ser: importstore_token_secreto_123")
                        else:
                            print(f"✅ WHATSAPP_VERIFY_TOKEN está correctamente configurado")
        
        if not verify_token_found:
            print("❌ WHATSAPP_VERIFY_TOKEN no se encontró en el archivo")
            print("   Agrega esta linea:")
            print("   WHATSAPP_VERIFY_TOKEN=importstore_token_secreto_123")
        
    except Exception as e:
        print(f"ERROR al leer el archivo: {e}")
else:
    print("❌ El archivo .env NO existe!")
    print(f"   Creá el archivo en: {env_path}")

print()
print("=" * 70)

