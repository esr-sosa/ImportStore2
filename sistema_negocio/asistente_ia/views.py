import json
from random import sample

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from . import interpreter
from core.db_inspector import table_exists
from .models import AssistantKnowledgeArticle, AssistantPlaybook, AssistantQuickReply

@login_required
def chat_view(request):
    """Renderiza la experiencia completa del asistente."""

    quick_replies = AssistantQuickReply.objects.none()
    knowledge = AssistantKnowledgeArticle.objects.none()
    playbooks = AssistantPlaybook.objects.none()
    missing_entities: list[str] = []

    if table_exists("asistente_ia_assistantquickreply"):
        quick_replies = (
            AssistantQuickReply.objects.filter(activo=True)
            .order_by("categoria", "orden", "titulo")
        )
    else:
        missing_entities.append("respuestas rápidas")

    if table_exists("asistente_ia_assistantknowledgearticle"):
        knowledge = AssistantKnowledgeArticle.objects.all()[:6]
    else:
        missing_entities.append("base de conocimiento")

    if table_exists("asistente_ia_assistantplaybook"):
        playbooks = AssistantPlaybook.objects.filter(es_template=True)[:6]
    else:
        missing_entities.append("playbooks")

    if missing_entities:
        messages.warning(
            request,
            "Faltan migraciones del asistente IA: ejecutá `python manage.py migrate` para preparar "
            + ", ".join(missing_entities)
            + ".",
        )

    context = {
        "quick_replies": quick_replies,
        "knowledge": knowledge,
        "playbooks": playbooks,
    }
    return render(request, "asistente_ia/chat.html", context)

@login_required
def ask_question(request):
    """
    Recibe una pregunta, la pasa al intérprete para consultar la BD,
    y devuelve una respuesta final generada por la IA.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get("question", "").strip()
            quick_reply_id = data.get("quick_reply_id")
            extra_context = data.get("context", [])

            if not user_question:
                return JsonResponse({"error": "No se recibió ninguna pregunta."}, status=400)

            # Mantener un historial corto en sesión para conversaciones más fluidas
            history = request.session.get("assistant_history", [])[-6:]
            if extra_context:
                for snippet in extra_context:
                    history.append({"role": "system", "content": str(snippet)[:400]})

            if user_question:
                history.append({"role": "user", "content": user_question})

            # 1. Pregunta -> JSON de Consulta
            query_json = interpreter.generate_query_json_from_question(
                user_question,
                chat_history="\n".join(item["content"] for item in history if item["role"] == "user"),
            )

            if not query_json:
                # Si la IA no pudo generar un JSON, le pedimos que explique por qué.
                final_answer = interpreter.generate_final_response(
                    user_question,
                    "No se pudo generar una consulta válida para esta pregunta.",
                )
                return JsonResponse({"answer": final_answer, "history": history})

            # 2. Ejecutar la consulta desde el JSON para obtener datos
            query_results = interpreter.run_query_from_json(query_json)

            # 3. Datos -> Respuesta Final en lenguaje natural
            final_answer = interpreter.generate_final_response(
                user_question,
                query_results,
                chat_history="\n".join(item["content"] for item in history[-6:]),
            )

            history.append({"role": "assistant", "content": final_answer})
            request.session["assistant_history"] = history[-10:]

            suggested_cards = []
            if table_exists("asistente_ia_assistantquickreply"):
                suggested_cards = list(
                    AssistantQuickReply.objects.filter(activo=True)
                    .exclude(id=quick_reply_id)
                    .order_by("orden")
                )
            suggested_payload = []
            if suggested_cards:
                # Tomamos hasta 3 sugerencias variadas
                picks = sample(suggested_cards, k=min(3, len(suggested_cards)))
                for card in picks:
                    suggested_payload.append(
                        {
                            "id": card.id,
                            "titulo": card.titulo,
                            "categoria": card.get_categoria_display(),
                            "prompt": card.prompt,
                        }
                    )

            return JsonResponse(
                {
                    "answer": final_answer,
                    "history": history[-10:],
                    "suggested": suggested_payload,
                }
            )

        except Exception as e:
            print(f"Error en la vista ask_question: {e}")
            return JsonResponse({"error": f"Hubo un error inesperado en el servidor: {e}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@login_required
@require_GET
def quick_replies_catalogue(request):
    """Retorna la lista de respuestas rápidas agrupadas por categoría."""

    if not table_exists("asistente_ia_assistantquickreply"):
        return JsonResponse({"quick_replies": {}}, status=200)

    replies = AssistantQuickReply.objects.filter(activo=True)
    payload: dict[str, list[dict[str, str]]] = {}
    for reply in replies.order_by("categoria", "orden"):
        payload.setdefault(reply.categoria, []).append(
            {
                "id": reply.id,
                "titulo": reply.titulo,
                "prompt": reply.prompt,
            }
        )
    return JsonResponse({"quick_replies": payload})


@login_required
@require_GET
def playbook_detail(request, pk: int):
    """Devuelve el detalle de un playbook para poder guiar una gestión."""

    if not table_exists("asistente_ia_assistantplaybook"):
        return JsonResponse({"error": "Las migraciones del asistente IA no están aplicadas."}, status=503)

    try:
        playbook = AssistantPlaybook.objects.get(pk=pk)
    except AssistantPlaybook.DoesNotExist:
        return JsonResponse({"error": "Playbook no encontrado"}, status=404)

    return JsonResponse(
        {
            "titulo": playbook.titulo,
            "descripcion": playbook.descripcion,
            "pasos": playbook.pasos,
        }
    )

