from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'superadmin/home.html', context)


def alta_cliente(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'superadmin/altacliente.html', context)


def alta_pisos(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'superadmin/altapisos.html', context)


def errores(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'superadmin/errores.html', context)


def bdowners(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'superadmin/historial.html', context)


def historial(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'superadmin/altacliente.html', context)


def logout(request):
    user = request.session['user']
    context = {
        'msg': user
    }
    return render(request, 'ownerlog.html', context)
