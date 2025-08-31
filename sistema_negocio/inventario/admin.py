# inventario/admin.py

from django.contrib import admin
from .models import Proveedor, Categoria, Producto, ProductoVariante, Precio, DetalleIphone

# --- Clases Inline ---

class PrecioInline(admin.TabularInline):
    model = Precio
    extra = 1
    verbose_name_plural = "Precios (Minorista y Mayorista)"

class DetalleIphoneInline(admin.StackedInline):
    model = DetalleIphone
    can_delete = False
    verbose_name_plural = 'Detalles Específicos para iPhones'

# --- Vista de ProductoVariante (AQUÍ ESTÁ LA MEJORA) ---
class ProductoVarianteInline(admin.TabularInline):
    model = ProductoVariante
    extra = 1
    verbose_name_plural = "Variantes del Producto (Color, Capacidad, etc.)"
    # Esta línea mágica hace que el nombre de la variante sea un link a su propia página de edición
    show_change_link = True 

# --- Vistas de Administración Personalizadas ---

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'proveedor', 'fecha_creacion')
    list_filter = ('categoria', 'proveedor')
    search_fields = ('nombre', 'descripcion')
    inlines = [ProductoVarianteInline] 
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'categoria', 'proveedor')
        }),
        ('Códigos y Fechas (generado automáticamente)', {
            'fields': ('codigo_barras', 'imagen_codigo_barras', 'fecha_creacion', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion', 'codigo_barras', 'imagen_codigo_barras')

@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre_variante', 'stock')
    list_filter = ('producto__categoria',)
    search_fields = ('producto__nombre', 'nombre_variante')
    inlines = [PrecioInline, DetalleIphoneInline]
    autocomplete_fields = ['producto']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'contacto')