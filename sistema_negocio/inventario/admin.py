# inventario/admin.py

from django.contrib import admin
from .models import Proveedor, Categoria, Producto, ProductoVariante, Precio, DetalleIphone

# --- Clases para mostrar modelos relacionados "dentro" de otros ---

class PrecioInline(admin.TabularInline):
    """Permite ver y editar los precios directamente desde la variante del producto."""
    model = Precio
    extra = 1
    verbose_name_plural = "Precios (Minorista y Mayorista)"

class DetalleIphoneInline(admin.StackedInline):
    """Permite añadir los detalles específicos de un iPhone desde la variante."""
    model = DetalleIphone
    can_delete = False
    verbose_name_plural = 'Detalles Específicos para iPhones'

class ProductoVarianteInline(admin.TabularInline):
    """Permite ver y editar las variantes directamente desde el producto principal."""
    model = ProductoVariante
    extra = 1
    verbose_name_plural = "Variantes del Producto (Color, Capacidad, etc.)"


# --- Vistas de Administración Personalizadas para cada Modelo ---

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Vista personalizada para el modelo Producto en el admin."""
    list_display = ('nombre', 'categoria', 'proveedor', 'fecha_creacion')
    list_filter = ('categoria', 'proveedor')
    search_fields = ('nombre', 'descripcion')
    inlines = [ProductoVarianteInline] # Muestra las variantes dentro del producto
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'categoria', 'proveedor')
        }),
        ('Códigos y Fechas (generado automáticamente)', {
            'fields': ('codigo_barras', 'imagen_codigo_barras', 'fecha_creacion', 'ultima_actualizacion'),
            'classes': ('collapse',) # Oculta esta sección por defecto
        }),
    )
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion', 'codigo_barras', 'imagen_codigo_barras')

@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    """Vista personalizada para las Variantes."""
    list_display = ('producto', 'nombre_variante', 'stock')
    list_filter = ('producto__categoria',)
    search_fields = ('producto__nombre', 'nombre_variante')
    inlines = [PrecioInline, DetalleIphoneInline]
    autocomplete_fields = ['producto']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Vista simple para Categorías."""
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """Vista simple para Proveedores."""
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'contacto')