from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    username = request.POST["email"]
    owner_object = User.objects.get(username__icontains=username)
    context = {
        'msg': owner_object
    }
    return render(request, 'superadmin/home.html', context)
