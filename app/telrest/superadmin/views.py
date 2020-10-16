from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request):
    context = {}
    return render(request, 'superadmin/home.html', context)


@login_required
def alta_cliente(request):
    context = {}
    return render(request, 'superadmin/altacliente.html', context)


@login_required
def alta_pisos(request):
    context = {}
    return render(request, 'superadmin/altapisos.html', context)


@login_required
def errores(request):
    context = {}
    return render(request, 'superadmin/errores.html', context)


@login_required
def bdowners(request):
    context = {}
    return render(request, 'superadmin/historial.html', context)


@login_required
def historial(request):
    context = {}
    return render(request, 'superadmin/altacliente.html', context)


@login_required
def logout_view(request):
    context = {}
    logout(request)
    return render(request, 'superadmin/logout.html', context)
