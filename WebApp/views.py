from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'app/index.html')

def matematica(request):
    return render(request,'app/matematica.html')

def quimica(request):
    return render(request,'app/quimica.html')

def iniciar_sesion(request):
    return render(request,'app/iniciar_sesion.html')

def registrarse(request):
    return render(request,'app/registrarse.html')