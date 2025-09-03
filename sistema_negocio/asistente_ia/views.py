from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from . import interpreter

@login_required
def chat_view(request):
    """
    Renderiza la interfaz principal del chat.
    """
    return render(request, 'asistente_ia/chat.html')

@login_required
def ask_question(request):
    """
    Recibe una pregunta, la pasa al intérprete para consultar la BD,
    y devuelve una respuesta final generada por la IA.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get('question', '')

            if not user_question:
                return JsonResponse({'error': 'No se recibió ninguna pregunta.'}, status=400)
            
            # --- El Flujo de Inteligencia de ISAC (CORREGIDO) ---
            
            # 1. Pregunta -> JSON de Consulta
            query_json = interpreter.generate_query_json_from_question(user_question)
            
            if not query_json:
                # Si la IA no pudo generar un JSON, le pedimos que explique por qué.
                final_answer = interpreter.generate_final_response(user_question, "No se pudo generar una consulta válida para esta pregunta.")
                return JsonResponse({'answer': final_answer})

            # 2. Ejecutar la consulta desde el JSON para obtener datos
            query_results = interpreter.run_query_from_json(query_json)

            # 3. Datos -> Respuesta Final en lenguaje natural
            final_answer = interpreter.generate_final_response(user_question, query_results)
            
            return JsonResponse({'answer': final_answer})

        except Exception as e:
            print(f"Error en la vista ask_question: {e}")
            return JsonResponse({'error': f'Hubo un error inesperado en el servidor: {e}'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

