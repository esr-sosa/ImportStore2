from django.contrib import admin

from .models import AssistantKnowledgeArticle, AssistantPlaybook, AssistantQuickReply, ConversationThread, ConversationMessage


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


@admin.register(ConversationThread)
class ConversationThreadAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "creado", "actualizado", "activo")
    list_filter = ("activo", "creado")
    search_fields = ("titulo", "usuario__username")
    readonly_fields = ("creado", "actualizado")


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "rol", "contenido_preview", "creado")
    list_filter = ("rol", "creado")
    search_fields = ("contenido", "thread__titulo")
    readonly_fields = ("creado",)
    
    def contenido_preview(self, obj):
        return obj.contenido[:50] + "..." if len(obj.contenido) > 50 else obj.contenido
    contenido_preview.short_description = "Contenido"
