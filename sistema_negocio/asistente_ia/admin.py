from django.contrib import admin

from .models import AssistantKnowledgeArticle, AssistantPlaybook, AssistantQuickReply


@admin.register(AssistantQuickReply)
class AssistantQuickReplyAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "orden", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("titulo", "prompt")
    ordering = ("categoria", "orden")


@admin.register(AssistantKnowledgeArticle)
class AssistantKnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ("titulo", "destacado", "actualizado")
    list_filter = ("destacado",)
    search_fields = ("titulo", "resumen", "contenido", "tags")
    ordering = ("-destacado", "titulo")


@admin.register(AssistantPlaybook)
class AssistantPlaybookAdmin(admin.ModelAdmin):
    list_display = ("titulo", "es_template", "actualizado")
    list_filter = ("es_template",)
    search_fields = ("titulo", "descripcion")
