from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


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
            request.session['user'] = user.username
            request.session['userid'] = user.id
            login(request, user)
            messages.success(request, 'Sesión iniciada')
            if user.is_superuser:
                return redirect('/superadmin/')
            else:
                return redirect('/owner/')
        else:
            messages.error(request, 'Usuario o contraseña inválidos')
        # else:
          #   messages.error(request, 'Usuario o contraseña inválidos')

    return render(request, 'ownerlog.html')

