from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .custom_forms import OwnerForm, JuridicaForm, FlatForm
from django.contrib import messages
from .models import OwnersData
from telapi.models import Flat


# Create your views here.

@login_required
def home(request):
    context = {}
    return render(request, 'superadmin/home.html', context)


@login_required
def alta_cliente(request):
    """New owner registration. The method alters both
    auth_user and owner_data tables in order to generate
    new user credentials and save the owner's data"""

    context = {}
    if request.method == 'POST':
        if request.POST.get('name') is not None:
            form = OwnerForm(request.POST)
            persona = True
        else:
            form = JuridicaForm(request.POST)
            persona = False

        if form.is_valid():
            # creo los objetos de auth user y owners data
            username = form.cleaned_data.get('email')
            password = User.objects.make_random_password()

            # enviar pass por email o algo
            print('la password es: ' + password)

            # guardo el objeto de auth user
            new_user = User.objects.create_user(username, username, password)
            new_user.save()

            # registro los datos del owner en owners_data
            owner = OwnersData(
                person_type=persona,
                name=form.cleaned_data.get('name'),
                last_name=form.cleaned_data.get('lastname'),
                denomination=form.cleaned_data.get('denominacion'),
                manager=form.cleaned_data.get('responsable'),
                cif=form.cleaned_data.get('cif'),
                email=form.cleaned_data.get('email'),
                owner_user=new_user,
                address=form.cleaned_data.get('direccion'),
                floor=form.cleaned_data.get('piso'),
                door=form.cleaned_data.get('puerta'),
                city=form.cleaned_data.get('ciudad'),
                postal_code=form.cleaned_data.get('cp'),
                phone=form.cleaned_data.get('tlf')
            )

            # guardo el objeto owner data en la bbdd y redirijo
            owner.save()

            messages.success(request, 'Usuario registrado')
            return redirect('/superadmin/')
    else:
        context = {
            'personas': {
                'fisica': {'form': OwnerForm},
                'juridica': {'form': JuridicaForm}
            }
        }
    return render(request, 'superadmin/altacliente.html', context)


@login_required
def alta_pisos(request):
    """New flat registration. The method alters the
    telapi.flat table in orther to add information about
    a new flag using an id from owners_data"""

    context = {}
    if request.method == 'POST':
        form = FlatForm(request.POST)
        if form.is_valid():
            # obtengo el owners_data object atraves del email y creo el objeto flat
            owner_object = OwnersData.objects.get(email=request.POST['owners'])

            flat_object = Flat(
                name=form.cleaned_data.get('name'),
                address=form.cleaned_data.get('address'),
                floor=form.cleaned_data.get('floor'),
                door=form.cleaned_data.get('door'),
                city=form.cleaned_data.get('city'),
                postal_code=form.cleaned_data.get('postal_code'),
                guests=form.cleaned_data.get('guests'),
                rooms=form.cleaned_data.get('rooms'),
                baths=form.cleaned_data.get('baths'),
                reference=form.cleaned_data.get('reference'),
                meters=form.cleaned_data.get('meters'),
                owners_data=owner_object,
            )

            # guardo objeto flat en la bbdd y redirijo
            flat_object.save()

            messages.success(request, 'Piso registrado')
            return redirect('/superadmin/')
    else:
        owners_email = OwnersData.objects.values_list('email', flat=True)
        flat_form = FlatForm()
        context = {
            'owners': owners_email,
            'form': flat_form,
        }
        print(owners_email)
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
