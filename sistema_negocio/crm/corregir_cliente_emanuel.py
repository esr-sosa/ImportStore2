#!/usr/bin/env python
"""Script para corregir el nombre del cliente Emanuel Sosa"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Cliente, Mensaje, Conversacion
from crm.services.ai_crm_service import extraer_y_guardar_nombre

def corregir_emanuel():
    """Corrige el nombre del cliente que dijo 'me llamo emanuel sosa'"""
    
    # Buscar cliente por teléfono mencionado
    telefono = '5492665032890'
    
    try:
        cliente = Cliente.objects.get(telefono=telefono)
        print(f"Cliente encontrado: {cliente.telefono}")
        print(f"Nombre actual: '{cliente.nombre}'")
        
        # Buscar en los mensajes si hay algún nombre mencionado
        conversaciones = Conversacion.objects.filter(cliente=cliente)
        
        for conversacion in conversaciones:
            mensajes = conversacion.mensajes.filter(emisor='Cliente').order_by('fecha_envio')
            for mensaje in mensajes:
                print(f"\nRevisando mensaje: '{mensaje.contenido[:100]}...'")
                nombre_candidato = extraer_y_guardar_nombre(mensaje.contenido, cliente)
                if nombre_candidato:
                    cliente.refresh_from_db()
                    print(f"  → Nombre extraído: '{nombre_candidato}'")
                    print(f"  → Nombre actualizado en DB: '{cliente.nombre}'")
        
        cliente.refresh_from_db()
        print(f"\n✅ Nombre final del cliente: '{cliente.nombre}'")
        
    except Cliente.DoesNotExist:
        print(f"Cliente con teléfono {telefono} no encontrado")
        # Buscar todos los clientes
        print("\nClientes existentes:")
        for c in Cliente.objects.all()[:10]:
            print(f"  - {c.telefono}: '{c.nombre}'")

if __name__ == '__main__':
    corregir_emanuel()

