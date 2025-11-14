from django.db import migrations, models

import inventario.models


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0015_categoria_garantia_dias"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductoImagen",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("imagen", models.ImageField(upload_to=inventario.models._producto_imagen_upload_to)),
                ("orden", models.PositiveIntegerField(default=0)),
                ("creado", models.DateTimeField(auto_now_add=True)),
                ("actualizado", models.DateTimeField(auto_now=True)),
                (
                    "producto",
                    models.ForeignKey(on_delete=models.CASCADE, related_name="imagenes", to="inventario.producto"),
                ),
            ],
            options={
                "verbose_name": "Imagen de producto",
                "verbose_name_plural": "Imágenes de producto",
                "ordering": ["orden", "id"],
            },
        ),
    ]

