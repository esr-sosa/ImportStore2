"""
Script para ver una línea específica del .env
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total de lineas: {len(lines)}")
    print()
    
    # Mostrar línea 18 (índice 17)
    if len(lines) > 17:
        print(f"Linea 18: {repr(lines[17])}")
        print(f"Contenido: {lines[17]}")
    else:
        print("La linea 18 no existe")
    
    # Mostrar contexto (líneas 15-20)
    print()
    print("Contexto (lineas 15-20):")
    print("-" * 70)
    for i in range(14, min(20, len(lines))):
        print(f"Linea {i+1}: {repr(lines[i])}")
else:
    print("El archivo .env no existe")

