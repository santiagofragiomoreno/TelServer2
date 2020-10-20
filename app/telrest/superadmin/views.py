from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .custom_forms import OwnerForm
from django.contrib import messages


# Create your views here.

@login_required
def home(request):
    context = {}
    return render(request, 'superadmin/home.html', context)


@login_required
def alta_cliente(request):
    context = {}
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = User.objects.make_random_password()
            new_user = User.objects.create_user(username, username, password)
            new_user.save()
            messages.success(request, 'Usuario registrado')
            return redirect('/superadmin/')
    else:
        context = {
            'owner': OwnerForm()
        }
        pass
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
    return render(request, 'superadmin/bdowners.html', context)


@login_required
def ajustes(request):
    context = {}
    return render(request, 'superadmin/ajustes.html', context)


@login_required
def alta_dispositivo(request):
    context = {}
    return render(request, 'superadmin/altadispositivo.html', context)


@login_required
def logout_view(request):
    context = {}
    logout(request)
    return render(request, 'superadmin/logout.html', context)
