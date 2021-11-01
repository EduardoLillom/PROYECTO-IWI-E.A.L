from django.db.models.manager import EmptyManager
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request,'app/index.html')

def matematica(request):
    return render(request,'app/matematica.html')

def quimica(request):
    return render(request,'app/quimica.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contrasena = request.POST['contraseña']
        user = authenticate(username=correo, password=contrasena)
        print(user)
        if user is not None:
            return redirect('home')
    return render(request,'app/iniciar_sesion.html')

def registrarse(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        user = User.objects.create_user(username=correo,password=contraseña,email=correo,last_name=apellido,first_name=nombre,)
        user.save()
        return redirect('home')
    return render(request,'app/registrarse.html')

def foro(request):
    pass

def perfil_user(request):
    pass