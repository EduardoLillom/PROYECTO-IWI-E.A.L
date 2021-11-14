from random import choice
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Value
from django.db.models.manager import EmptyManager
from django.forms.utils import pretty_name
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from WebApp.models import PreguntasMate, PostForo, profile, historialCertamen
from random import sample
from .forms import FormComentarios

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
    preguntaPrueba.objects.create(texto=texto, nombre_pregunta=nombre_pregunta, pregunta_math=pregunta_math )
    return redirect('/crearPregunta/')

def index(request):
    return render(request,'app/index.html')

#----Generador de certamenes----
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

        preguntaRandom = []
        for tema in preg_for_tem:
            preguntas_db = PreguntasMate.objects.filter(tema=tema).values()      
            preguntaRandom.extend(sample(list(preguntas_db),preg_for_tem[tema]))
    
        preguntas = []
        id_preguntas = []
        for p in preguntaRandom:
            e = {'id':'',
                'pregunta':'',
                'A':'',
                'B':'',
                'C':'',
                'D':'',
                'E':'',}
            e['id'] = p['id']
            id_preguntas.append(p['id'])
            e['pregunta'] = p['pregunta']
            e['a'] = p['alternativa_a']
            e['b'] = p['alternativa_b']
            e['c'] = p['alternativa_c']
            e['d'] = p['alternativa_d']
            e['e'] = p['alternativa_e']  
            preguntas.append(e)

        certamen = historialCertamen.objects.create(id_usuario=request.user.id ,id_preguntas=id_preguntas,estado=False)
        data = {'clase':'MAT021',
        'preguntas':preguntas,
        'id':certamen.id,
        }
        return render(request,'app/base_certamenes.html',data)


def matematica(request):
    return render(request,'app/matematica.html')

#----Resultado del certamen-----
def resultado(request):
    if request.method == 'POST':
        data = request.POST
        #---verificar si las alternativas son correctas y las guarda en formato (id,True/False,puntos)---
        correccion_preguntas = []
        for e in data:
            if e not in ['csrfmiddlewaretoken', 'id']:
                id_pregunta = e
                data_pregunta = PreguntasMate.objects.filter(id=id_pregunta).values()
                alternativa = data[e]
                alternativa_correcta = data_pregunta[0]['alternativa_correcta']
                puntos = data_pregunta[0]['puntos']
                if alternativa == alternativa_correcta:
                    correccion_preguntas.append((id_pregunta,True,puntos))
                else:
                    correccion_preguntas.append((id_pregunta,False,0))

        #---Estadisticas del certamen---
        n_preguntas = len(correccion_preguntas)
        n_preguntasCorrectas = 0
        preguntas_incorrectas = []
        puntos = 0
        for e in correccion_preguntas:
            if e[1]:
                n_preguntasCorrectas += 1
                puntos += e[2]
            else:#Seleciono las preguntas incorrectas y sus respectivas respuestas
                data_pregunta = PreguntasMate.objects.filter(id=e[0]).values()
                pregunta = data_pregunta[0]['pregunta']
                letra_alternativa_correcta = data_pregunta[0]['alternativa_correcta']

                if letra_alternativa_correcta == 'A':
                    correcta = data_pregunta[0]['alternativa_a']
                elif letra_alternativa_correcta == 'B':
                    correcta = data_pregunta[0]['alternativa_b']
                elif letra_alternativa_correcta == 'C':
                    correcta = data_pregunta[0]['alternativa_c']
                elif letra_alternativa_correcta == 'D':
                    correcta = data_pregunta[0]['alternativa_d']
                elif letra_alternativa_correcta == 'E':
                    correcta = data_pregunta[0]['alternativa_e']

                preguntas_incorrectas.append((pregunta,correcta))
        porcentaje_acierto = round((n_preguntasCorrectas/n_preguntas)*100,2)

        perfil_usuario = profile.objects.filter(name_id = request.user.id)
        puntos_usuario = perfil_usuario[0].punctuation
        perfil_usuario.update(punctuation=puntos_usuario+puntos)
        certamen = historialCertamen.objects.get(id=data['id'])
        certamen.estado = True
        certamen.save()
        d = {
            'n_preguntasCorrerctas':n_preguntasCorrectas,
            'n_preguntas':n_preguntas,
            'porcentaje_acierto':porcentaje_acierto,
            'preguntas_incorrectas':preguntas_incorrectas,
            'puntos': puntos,
        }

    return render(request,'app/resultadosCert.html',d)

#----Todo lo relacionado con el usuario----
def mi_perfil(request):
    correo = request.user.email
    nombre_usuario = request.user.first_name + ' ' + request.user.last_name
    id = request.user.id
    puntos = profile.objects.filter(name_id=id).values()[0]['punctuation']
    contexto = { 'UserName' : nombre_usuario
                ,'correo' : correo
                ,'puntos' : puntos}

    return render(request,'app/mi_perfil.html',contexto)

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

#----Todo lo relacionado con el foro----
def foro(request):
    
    post = PostForo.objects.all()

    contexto = {

        'post': post

    }

    return render(request, 'app/foro.html', contexto)

def foro1(request):
    return render(request,'app/foro.html')

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