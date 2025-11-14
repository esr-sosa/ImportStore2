from django.db import models


class AssistantQuickReply(models.Model):
    """Respuestas rápidas curadas para el asistente virtual."""

    CATEGORIES = (
        ("inventario", "Inventario"),
        ("ventas", "Ventas"),
        ("soporte", "Soporte"),
        ("finanzas", "Finanzas"),
        ("general", "General"),
    )

    titulo = models.CharField(max_length=80)
    prompt = models.TextField(help_text="Instrucción que se enviará a ISAC cuando el usuario pulse la tarjeta")
    categoria = models.CharField(max_length=20, choices=CATEGORIES, default="general")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["categoria", "orden", "titulo"]
        verbose_name = "Respuesta rápida"
        verbose_name_plural = "Respuestas rápidas"

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"{self.titulo} ({self.get_categoria_display()})"


class AssistantKnowledgeArticle(models.Model):
    """Ficha de conocimiento estático que se puede consultar desde la UI."""

    titulo = models.CharField(max_length=140)
    resumen = models.TextField(help_text="Resumen breve que se mostrará en la tarjeta")
    contenido = models.TextField(help_text="Detalle completo del procedimiento o política")
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Lista de etiquetas separadas por coma para facilitar la búsqueda",
    )
    destacado = models.BooleanField(default=False)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-destacado", "titulo"]
        verbose_name = "Artículo de conocimiento"
        verbose_name_plural = "Artículos de conocimiento"

    def tag_list(self) -> list[str]:
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.titulo


class AssistantPlaybook(models.Model):
    """Checklist guiado para ejecutar procesos de negocio desde el asistente."""

    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    pasos = models.JSONField(
        default=list,
        help_text="Lista ordenada de pasos con titulo y descripcion",
    )
    es_template = models.BooleanField(
        default=True,
        help_text="Marca si el playbook aparece en la sección de flujos recomendados",
    )
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "Playbook del asistente"
        verbose_name_plural = "Playbooks del asistente"

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.titulo
