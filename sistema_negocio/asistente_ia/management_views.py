# asistente_ia/management_views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import AssistantQuickReply, AssistantPlaybook, AssistantKnowledgeArticle


@login_required
def manage_quick_replies(request):
    """Vista para gestionar respuestas rápidas."""
    replies = AssistantQuickReply.objects.all().order_by('categoria', 'orden', 'titulo')
    return render(request, 'asistente_ia/manage_quick_replies.html', {
        'replies': replies,
        'categories': AssistantQuickReply.CATEGORIES,
    })


@login_required
@require_POST
def quick_reply_create(request):
    """Crear nueva respuesta rápida."""
    try:
        reply = AssistantQuickReply.objects.create(
            titulo=request.POST.get('titulo', ''),
            prompt=request.POST.get('prompt', ''),
            categoria=request.POST.get('categoria', 'general'),
            orden=int(request.POST.get('orden', 0)),
            activo=request.POST.get('activo') == 'on',
        )
        messages.success(request, f'Respuesta rápida "{reply.titulo}" creada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al crear respuesta rápida: {e}')
    return redirect('asistente_ia:manage_quick_replies')


@login_required
@require_POST
def quick_reply_update(request, pk):
    """Actualizar respuesta rápida."""
    reply = get_object_or_404(AssistantQuickReply, pk=pk)
    try:
        reply.titulo = request.POST.get('titulo', '')
        reply.prompt = request.POST.get('prompt', '')
        reply.categoria = request.POST.get('categoria', 'general')
        reply.orden = int(request.POST.get('orden', 0))
        reply.activo = request.POST.get('activo') == 'on'
        reply.save()
        messages.success(request, f'Respuesta rápida "{reply.titulo}" actualizada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al actualizar respuesta rápida: {e}')
    return redirect('asistente_ia:manage_quick_replies')


@login_required
@require_POST
def quick_reply_delete(request, pk):
    """Eliminar respuesta rápida."""
    reply = get_object_or_404(AssistantQuickReply, pk=pk)
    try:
        titulo = reply.titulo
        reply.delete()
        messages.success(request, f'Respuesta rápida "{titulo}" eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar respuesta rápida: {e}')
    return redirect('asistente_ia:manage_quick_replies')


@login_required
def manage_playbooks(request):
    """Vista para gestionar playbooks."""
    playbooks = AssistantPlaybook.objects.all().order_by('titulo')
    return render(request, 'asistente_ia/manage_playbooks.html', {
        'playbooks': playbooks,
    })


@login_required
@require_POST
def playbook_create(request):
    """Crear nuevo playbook."""
    try:
        pasos = json.loads(request.POST.get('pasos', '[]'))
        playbook = AssistantPlaybook.objects.create(
            titulo=request.POST.get('titulo', ''),
            descripcion=request.POST.get('descripcion', ''),
            pasos=pasos,
            es_template=request.POST.get('es_template') == 'on',
        )
        messages.success(request, f'Playbook "{playbook.titulo}" creado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al crear playbook: {e}')
    return redirect('asistente_ia:manage_playbooks')


@login_required
@require_POST
def playbook_update(request, pk):
    """Actualizar playbook."""
    playbook = get_object_or_404(AssistantPlaybook, pk=pk)
    try:
        playbook.titulo = request.POST.get('titulo', '')
        playbook.descripcion = request.POST.get('descripcion', '')
        playbook.pasos = json.loads(request.POST.get('pasos', '[]'))
        playbook.es_template = request.POST.get('es_template') == 'on'
        playbook.save()
        messages.success(request, f'Playbook "{playbook.titulo}" actualizado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al actualizar playbook: {e}')
    return redirect('asistente_ia:manage_playbooks')


@login_required
@require_POST
def playbook_delete(request, pk):
    """Eliminar playbook."""
    playbook = get_object_or_404(AssistantPlaybook, pk=pk)
    try:
        titulo = playbook.titulo
        playbook.delete()
        messages.success(request, f'Playbook "{titulo}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar playbook: {e}')
    return redirect('asistente_ia:manage_playbooks')


@login_required
def manage_knowledge(request):
    """Vista para gestionar artículos de conocimiento."""
    articles = AssistantKnowledgeArticle.objects.all().order_by('-destacado', 'titulo')
    return render(request, 'asistente_ia/manage_knowledge.html', {
        'articles': articles,
    })


@login_required
@require_POST
def knowledge_create(request):
    """Crear nuevo artículo de conocimiento."""
    try:
        article = AssistantKnowledgeArticle.objects.create(
            titulo=request.POST.get('titulo', ''),
            resumen=request.POST.get('resumen', ''),
            contenido=request.POST.get('contenido', ''),
            tags=request.POST.get('tags', ''),
            destacado=request.POST.get('destacado') == 'on',
        )
        messages.success(request, f'Artículo "{article.titulo}" creado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al crear artículo: {e}')
    return redirect('asistente_ia:manage_knowledge')


@login_required
@require_POST
def knowledge_update(request, pk):
    """Actualizar artículo de conocimiento."""
    article = get_object_or_404(AssistantKnowledgeArticle, pk=pk)
    try:
        article.titulo = request.POST.get('titulo', '')
        article.resumen = request.POST.get('resumen', '')
        article.contenido = request.POST.get('contenido', '')
        article.tags = request.POST.get('tags', '')
        article.destacado = request.POST.get('destacado') == 'on'
        article.save()
        messages.success(request, f'Artículo "{article.titulo}" actualizado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al actualizar artículo: {e}')
    return redirect('asistente_ia:manage_knowledge')


@login_required
@require_POST
def knowledge_delete(request, pk):
    """Eliminar artículo de conocimiento."""
    article = get_object_or_404(AssistantKnowledgeArticle, pk=pk)
    try:
        titulo = article.titulo
        article.delete()
        messages.success(request, f'Artículo "{titulo}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar artículo: {e}')
    return redirect('asistente_ia:manage_knowledge')

