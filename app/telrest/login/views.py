from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group


# ---------use for login in BBDD-------------------

def login_view(request):
    """ Custom login to redirect users to the superadmins or owners platform.
        django checks for the auth_user table from the database specified at the settings.DATABASES
        the values needed for the login saved during the session are username and password"""

    if request.method == 'POST':
        # form = AuthenticationForm(request=request, data=request.POST)
        form = request.POST
        # if form.is_valid():
        username = form.get('email')
        password = form.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:

            is_superuser = False
            is_owner = False
            for group in user.groups.all():
                if group.name == 'Owner':
                    is_owner = True
                if group.name == 'Superuser':
                    is_superuser = True

            if is_superuser:
                login(request, user)
                messages.success(request, 'Sesión iniciada')
                return redirect('/superadmin/')
            elif is_owner:
                login(request, user)
                messages.success(request, 'Sesión iniciada')
                return redirect('/owner/')
            else:
                messages.error(request, 'No tiene grupo asociado')
        else:
            messages.error(request, 'Usuario o contraseña inválidos')
        # else:
          #   messages.error(request, 'Usuario o contraseña inválidos')

    return render(request, 'ownerlog.html')

