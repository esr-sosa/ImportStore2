"""
Script para verificar si los puertos de Laragon están ocupados
"""

import socket

def verificar_puerto(host, port):
    """Verifica si un puerto está en uso"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

print("=" * 70)
print("VERIFICACION DE PUERTOS DE LARAGON")
print("=" * 70)
print()

puertos = {
    'MySQL': 3306,
    'Apache (HTTP)': 80,
    'Apache (HTTPS)': 443,
    'Django (desarrollo)': 8000,
}

print("Verificando puertos...")
print("-" * 70)

for nombre, puerto in puertos.items():
    ocupado = verificar_puerto('localhost', puerto)
    estado = "[OCUPADO]" if ocupado else "[LIBRE]"
    print(f"{estado} {nombre}: puerto {puerto}")

print()
print("=" * 70)
print("SOLUCIONES:")
print("=" * 70)
print()
print("Si MySQL (3306) está OCUPADO:")
print("  - Otro servicio MySQL puede estar corriendo")
print("  - Detené otros servicios MySQL")
print()
print("Si Apache (80) está OCUPADO:")
print("  - Otro servidor web puede estar usando el puerto 80")
print("  - Cambiá el puerto en Laragon o detené el otro servidor")
print()
print("Si Django (8000) está OCUPADO:")
print("  - Tu servidor Django puede estar corriendo")
print("  - Detené el servidor Django si querés usar Laragon")
print()

