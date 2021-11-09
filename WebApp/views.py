from random import choice
from django.contrib.contenttypes.models import ContentType
from django.db.models.manager import EmptyManager
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from WebApp.models import PreguntasMate, PostForo
from random import sample
from .forms import FormComentarios
# Create your views here.

from .models import Comentario, PostForo, preguntaPrueba # prueba

def crearPregunta(request):    
    pregunta_Prueba = preguntaPrueba.objects.all()
    data={
            'pregunta_Prueba' : pregunta_Prueba
    }
    return render(request,'app/crearPregunta.html',data)

def guardarPregunta(request):
    texto=request.POST["texto"]
    nombre_pregunta = request.POST["nombre_pregunta"]
    pregunta_math = request.POST["pregunta_math"]
    pregunta = preguntaPrueba.objects.create(texto=texto, nombre_pregunta=nombre_pregunta, pregunta_math=pregunta_math )
    return redirect('/crearPregunta/')

def index(request):
    return render(request,'app/index.html')

def certamen(request):
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

    preguntas = []
    for tema in preg_for_tem:
        preguntas_db = PreguntasMate.objects.filter(tema=tema).values()        
        preguntas.extend(sample(list(preguntas_db),preg_for_tem[tema]))

    data = {'clase':'MAT021',
    'preguntas':preguntas,
    }
    return render(request,'app/base_certamenes.html',data)

def matematica(request):
    return render(request,'app/matematica.html')

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
    
    post = PostForo.objects.all()

    contexto = {

        'post': post

    }

    return render(request, 'app/foro.html', contexto)

def Comentarios_pk(request, pk):

    instance = get_object_or_404(PostForo, pk= pk)

    inicializar_datos = {
        'content_type': instance.get_content_type,
        'object_id' : instance.id
    }

    form = FormComentarios(request.POST or None, initial=inicializar_datos)

    if form.is_valid():
        content_type = ContentType.objects.get_for_model(instance)
        obj_id = form.cleaned_data.get('object_id')
        texto_data = form.cleaned_data.get('texto')

        comentarios, created = Comentario.objects.get_or_create(
            usuario = request.user,
            content_type = content_type,
            object_id = obj_id,
            texto = texto_data
        )

        return HttpResponseRedirect(comentarios.content_object.get_absolute_url())

    ver_comentario = instance.comentarios
    context = {
        'form': form,
        'instance': instance,
        'ver_comentario': ver_comentario
    }

    return render(request, 'app/comentario.html', context)

def comentario_id(request, pk):

    instance = get_object_or_404(Comentario, pk=pk)

    contexto = {
        'comentario':instance
    }
    return render(request, 'app/instance.html', contexto)
def perfil_user(request):
    pass