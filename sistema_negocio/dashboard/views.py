# dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    # Esta vista simplemente muestra la página de bienvenida.
    return render(request, 'dashboard/main.html')