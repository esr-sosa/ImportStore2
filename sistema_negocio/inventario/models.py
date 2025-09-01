# inventario/models.py

from django.db import models
from django.core.exceptions import ValidationError
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True, help_text="Nombre del proveedor")
    contacto = models.CharField(max_length=150, blank=True, null=True, help_text="Persona de contacto")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nombre
    class Meta: verbose_name, verbose_name_plural = "Proveedor", "Proveedores"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre
    class Meta: verbose_name, verbose_name_plural = "Categoría", "Categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=200, help_text="Nombre del producto. Ej: iPhone 15 Pro Max")
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="productos")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, related_name="productos")
    activo = models.BooleanField(default=True, help_text="Indica si el producto está activo y visible para la venta")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Foto principal del producto")
    codigo_barras = models.CharField(max_length=13, unique=True, blank=True, help_text="Código de barras (EAN-13). Se genera automáticamente.")
    imagen_codigo_barras = models.ImageField(upload_to='codigos_de_barras/', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    def __str__(self): return self.nombre
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.codigo_barras:
            numero_base = f"{self.pk:012d}"
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(numero_base, writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.imagen_codigo_barras.save(f'{numero_base}.png', File(buffer), save=False)
            self.codigo_barras = numero_base
            super().save(update_fields=['codigo_barras', 'imagen_codigo_barras'])
    class Meta: verbose_name, verbose_name_plural = "Producto", "Productos"

class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    nombre_variante = models.CharField(max_length=150, help_text="Descripción de la variante. Ej: 128GB / Azul Titanio")
    stock = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.producto.nombre} - {self.nombre_variante}"
    class Meta:
        verbose_name, verbose_name_plural = "Variante de Producto", "Variantes de Productos"
        unique_together = ('producto', 'nombre_variante')

class Precio(models.Model):
    MONEDA_CHOICES = [
        ('ARS', 'Pesos Argentinos (ARS)'),
        ('USD', 'Dólares Estadounidenses (USD)'),
    ]
    TIPO_PRECIO_CHOICES = [
        ('Minorista', 'Minorista'),
        ('Mayorista', 'Mayorista'),
    ]
    variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name="precios")
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='ARS')
    tipo_precio = models.CharField(max_length=20, choices=TIPO_PRECIO_CHOICES, default='Minorista')
    costo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Costo de adquisición del producto")
    precio_venta_normal = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de venta estándar")
    precio_venta_minimo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio mínimo al que se puede vender")
    precio_venta_descuento = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, help_text="Precio con descuento (opcional)")
    def clean(self):
        if self.precio_venta_minimo < self.costo: raise ValidationError("El precio mínimo no puede ser menor que el costo.")
        if self.precio_venta_normal < self.precio_venta_minimo: raise ValidationError("El precio normal no puede ser menor que el precio mínimo.")
    def __str__(self): return f"{self.variante} ({self.tipo_precio}) - {self.moneda} ${self.precio_venta_normal}"
    class Meta:
        verbose_name, verbose_name_plural = "Precio", "Precios"
        unique_together = ('variante', 'tipo_precio')

class DetalleIphone(models.Model):
    variante = models.OneToOneField(ProductoVariante, on_delete=models.CASCADE, related_name="detalle_iphone")
    imei = models.CharField(max_length=15, unique=True, help_text="IMEI único del equipo")
    salud_bateria = models.PositiveIntegerField(help_text="Porcentaje de salud de la batería (ej: 98)")
    fallas_detectadas = models.TextField(blank=True, null=True, help_text="Descripción de cualquier falla o detalle")
    fecha_compra = models.DateField()
    def __str__(self): return f"iPhone con IMEI: {self.imei}"
    class Meta: verbose_name, verbose_name_plural = "Detalle de iPhone", "Detalles de iPhones"
    def clean(self):
        if not self.imei.isdigit() or len(self.imei) not in [14, 15]:
            raise ValidationError("El IMEI debe ser un número de 14 o 15 dígitos.")