from django.db import models


class Local(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "local"
        verbose_name_plural = "locales"

    def __str__(self) -> str:
        return self.nombre
