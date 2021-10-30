from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def matematica(request):
    return render(request,'Matematica.html')

def quimica(request):
    return render(request,'Quimica.html')

def iniciar_secion(request):
    return render(request,'iniciar_sesion.html')

def registrarse(request):
    return render(request,'registrarse.html')