from random import choice
from django.db.models.manager import EmptyManager
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'app/index.html')

def certamen(request):
    pass

def matematica(request):
    if request.method == 'POST':
        datos = request.POST
        num_preg = int(request.POST['number_of_questions'])
        time = request.POST['tiempo']
        temas = []
        for e in datos:
            if e not in ('csrfmiddlewaretoken','tiempo','number_of_questions'):
                temas.append(e)

        preg_for_tem = {}
        for tema in temas:
            if tema not in preg_for_tem:
                preg_for_tem[tema] = 0

        if num_preg == len(temas):
            for tema in preg_for_tem:
                preg_for_tem[tema] += 1
        elif num_preg%len(temas) == 0 and num_preg//len(temas) > 0:
            for tema in temas:
                preg_for_tem[tema] =  num_preg//len(temas)
        else:
            preguntas_restantes = num_preg-len(temas)*(num_preg//len(temas))
            for tema in temas:
                preg_for_tem[tema] =  num_preg//len(temas) 
            for e in range(preguntas_restantes):
                preg_for_tem[choice(temas)] +=1
        print(preg_for_tem)

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