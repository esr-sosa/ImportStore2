#!/usr/bin/env python
"""Script para corregir nombres de clientes que fueron guardados incorrectamente"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Cliente, Mensaje, Conversacion
from crm.services.ai_crm_service import extraer_y_guardar_nombre

def corregir_nombres():
    """Corrige nombres de clientes que fueron guardados incorrectamente"""
    
    # Buscar clientes con nombres inválidos
    nombres_invalidos = ['Hola', 'hola', 'Holi', 'holi', 'Hi', 'hi', 'Hey', 'hey']
    clientes_problema = Cliente.objects.filter(nombre__in=nombres_invalidos)
    
    print(f"Encontrados {clientes_problema.count()} clientes con nombres inválidos")
    
    for cliente in clientes_problema:
        print(f"\nCliente: {cliente.telefono} - Nombre actual: '{cliente.nombre}'")
        
        # Buscar en los mensajes del cliente si hay algún nombre mencionado
        conversaciones = Conversacion.objects.filter(cliente=cliente)
        nombre_encontrado = None
        
        for conversacion in conversaciones:
            mensajes = conversacion.mensajes.filter(emisor='Cliente').order_by('fecha_envio')
            for mensaje in mensajes:
                nombre_candidato = extraer_y_guardar_nombre(mensaje.contenido, cliente)
                if nombre_candidato and nombre_candidato not in nombres_invalidos:
                    nombre_encontrado = nombre_candidato
                    print(f"  → Nombre encontrado en mensaje: '{nombre_encontrado}'")
                    break
            if nombre_encontrado:
                break
        
        if not nombre_encontrado:
            # Si no se encontró nombre, usar el formato genérico
            cliente.nombre = f"Cliente {cliente.telefono[-4:]}"
            cliente.save()
            print(f"  → Nombre actualizado a: '{cliente.nombre}' (genérico)")
        else:
            print(f"  → Nombre ya actualizado a: '{cliente.nombre}'")
    
    print("\n✅ Corrección completada")

if __name__ == '__main__':
    corregir_nombres()

