from django.db.models.manager import EmptyManager
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'app/index.html')

def matematica(request):
    return render(request,'app/matematica.html')

def quimica(request):
    return render(request,'app/quimica.html')

def foro1(request):
    return render(request,'app/foro.html')

def mi_perfil(request):
    return render(request,'app/mi_perfil.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        #---recibir datos del formulario---
        correo = request.POST['correo']
        contrasena = request.POST['contraseña']
        #---validar datos---
        user = authenticate(username=correo, password=contrasena)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request,'app/iniciar_sesion.html')

def registrarse(request):
    if request.method == 'POST':
        #---recibir datos del formulario---
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        password = request.POST['contraseña']
        #---Crea Usuario---
        if User.objects.filter(username=correo).exists():
            messages.error(request, 'El usuario ya existe.')
            return render(request,'app/registrarse.html')
        user = User.objects.create_user(username=correo,password=password,email=correo,last_name=apellido,first_name=nombre,)
        user.save()
        user = authenticate(username=correo, password=password)
        login(request, user)
        return redirect('home')
    return render(request,'app/registrarse.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def foro(request):
    pass

def perfil_user(request):
    pass