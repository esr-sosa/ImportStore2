from django.db import models
from django.contrib.auth.models import User


class ConversationThread(models.Model):
    """Hilo de conversación estilo ChatGPT para mantener contexto separado."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversaciones')
    titulo = models.CharField(max_length=200, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-actualizado']
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"
    
    def __str__(self):
        return f"{self.titulo or 'Sin título'} - {self.usuario.username}"


class ConversationMessage(models.Model):
    """Mensaje individual dentro de una conversación."""
    thread = models.ForeignKey(ConversationThread, on_delete=models.CASCADE, related_name='mensajes')
    rol = models.CharField(max_length=20, choices=[('user', 'Usuario'), ('assistant', 'Asistente'), ('system', 'Sistema')])
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['creado']
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
    
    def __str__(self):
        return f"{self.rol}: {self.contenido[:50]}..."


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
