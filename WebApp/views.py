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
from .forms import FormComentarios, FormForo

from .models import Comentario, PostForo, preguntaPrueba # prueba

#----Funciones para los views----
def generar_id(largo):
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numeros = '0123456789'
    base = letras + numeros
    id_certamen = sample(base,largo)
    id_certamen = ''.join(id_certamen)
    return id_certamen

def generar_preguntas(num_preg,temas):
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
    return preguntas, id_preguntas

def recuperar_preguntas(id_preguntas_c):
    preguntas_db = []
    for id in id_preguntas_c:
        pregunta = PreguntasMate.objects.filter(id=id).values()
        preguntas_db.append(pregunta)

    preguntas = []
    for p in preguntas_db:
        e = {'id':'',
            'pregunta':'',
            'A':'',
            'B':'',
            'C':'',
            'D':'',
            'E':'',}

        e['id'] = p[0]['id']
        e['pregunta'] = p[0]['pregunta']
        e['a'] = p[0]['alternativa_a']
        e['b'] = p[0]['alternativa_b']
        e['c'] = p[0]['alternativa_c']
        e['d'] = p[0]['alternativa_d']
        e['e'] = p[0]['alternativa_e']
            
        preguntas.append(e)
    return preguntas
#----Views-----------------------
def crearPregunta(request):
    if request.method == 'POST':
        form = FormForo(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor_id = request.user.username
            post.save()
            messages.success(request, f"Tu pregunta se ha publicado correctamente")
            return redirect('/foro/') 
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

    form = FormForo()
    data={
            'form' : form
    }
    return render(request,'app/crearPost.html',data)

def guardarPregunta(request):
    texto=request.POST["texto"]
    nombre_pregunta = request.POST["nombre_pregunta"]
    pregunta_math = request.POST["pregunta_math"]
    preguntaPrueba.objects.create(texto=texto, nombre_pregunta=nombre_pregunta, pregunta_math=pregunta_math )
    return redirect('/crearPregunta/')

def home(request):
    puntos_usuarios = profile.objects.order_by('-punctuation')
    if len(puntos_usuarios) > 10:
        puntos_usuarios = puntos_usuarios[:10]
    nombre_usuario = request.user.first_name
    appelido_usuario = request.user.last_name
    name = nombre_usuario + " " + appelido_usuario
    top = []
    for usuario in puntos_usuarios:
        id_usuario = usuario.name_id
        puntuacion = usuario.punctuation
        nombre = User.objects.get(id=id_usuario).first_name
        apellido = User.objects.get(id=id_usuario).last_name
        nombre_completo = nombre + ' ' + apellido
        top.append((nombre_completo,puntuacion))

    data = {
        'name': name,
        'top': top,
    }

    return render(request,'app/index.html',data)

#----Generador de certamenes----
def certamen(request):
    id_certamen = request.GET.get('id')
    certamen_h = historialCertamen.objects.filter(id_certamen=id_certamen)
    if (certamen_h.exists() == False):#Si el certamen no esta creado lo crea y lo guarda en el historial 
        if request.method == 'POST':
            #----Extraer datos del POST----
            datos = request.POST
            num_preg = int(request.POST['number_of_questions'])
            time = request.POST['tiempo']
            #----Separar temas----
            temas = []
            for e in datos:
                if e not in ('csrfmiddlewaretoken','tiempo','number_of_questions'):
                    temas.append(e)
            #----Generar preguntas----
            preguntas,id_preguntas = generar_preguntas(num_preg,temas)

            #----Crear el certamen en la DB para su posterior verificacion----
            historialCertamen.objects.create(id_usuario=request.user.id ,id_preguntas=id_preguntas,estado=False,id_certamen=id_certamen)

            #----Data de html y envio al mismo----
            data = {'clase':'MAT021',
            'preguntas':preguntas,
            'tiempo':time,
            'estatus':False,
            'id':id_certamen,
            }
            return render(request,'app/base_certamenes.html',data)

    elif certamen_h.exists() and certamen_h[0].estado == False :#Si el certamen ya esta creado pero no ha sido terminado
        id_preguntas_c = certamen_h[0].id_preguntas
        id_preguntas_c = id_preguntas_c[1:-1]
        id_preguntas_c = id_preguntas_c.split(',')
        
        preguntas = recuperar_preguntas(id_preguntas_c)

        data = {'clase':'MAT021',
        'preguntas':preguntas,
        'tiempo':'',
        'estatus':False,
        'id':id_certamen,
        }
        return render(request,'app/base_certamenes.html',data)
    elif certamen_h.exists() and certamen_h[0].estado:#Si el certamen ya esta creado y ha sido terminado
        id_preguntas_c = certamen_h[0].id_preguntas
        id_preguntas_c = id_preguntas_c[1:-1]
        id_preguntas_c = id_preguntas_c.split(',')
        alternativas_marcadas = certamen_h[0].alternativa_marcadas
        alternativas_marcadas= alternativas_marcadas.split(',')

        preguntas = recuperar_preguntas(id_preguntas_c)
        for e in preguntas:
            e['marcada'] = alternativas_marcadas[preguntas.index(e)]
        data = {'clase':'MAT021',
        'preguntas':preguntas,
        'tiempo':'',
        'estatus':True,
        'id':id_certamen,
        }
        return render(request,'app/base_certamenes.html',data)

def matematica(request):
    id_certamen = generar_id(5) + str(request.user.id)
    data = {'id_certamen':id_certamen}
    return render(request,'app/matematica.html',data)

#----Resultado del certamen-----
def resultado(request):
    if request.method == 'POST':
        data = request.POST
        #---verificar si las alternativas son correctas y las guarda en formato (id,True/False,puntos)---
        correccion_preguntas = []
        alternativas_marcadas = []
        for e in data:
            if e not in ['csrfmiddlewaretoken', 'id']:
                id_pregunta = e
                data_pregunta = PreguntasMate.objects.filter(id=id_pregunta).values()
                alternativa = data[e]
                alternativas_marcadas.append(alternativa)
                alternativa_correcta = data_pregunta[0]['alternativa_correcta']
                puntos = data_pregunta[0]['puntos']
                if alternativa == alternativa_correcta:
                    correccion_preguntas.append((id_pregunta,True,puntos))
                else:
                    correccion_preguntas.append((id_pregunta,False,0))

        alternativas_marcadas = ','.join(alternativas_marcadas)
        
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

        certamen = historialCertamen.objects.get(id_certamen=data['id'])
        if certamen.estado == False:
            perfil_usuario = profile.objects.filter(name_id = request.user.id)
            puntos_usuario = perfil_usuario[0].punctuation
            perfil_usuario.update(punctuation=puntos_usuario+puntos)
            
            certamen.estado = True
            certamen.alternativa_marcadas = alternativas_marcadas
            certamen.n_preguntas = n_preguntas
            certamen.n_correctas = str(n_preguntasCorrectas)+'/'+str(n_preguntas)
            certamen.puntos = puntos
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

def registro_certamenes(request):
    certamenes = historialCertamen.objects.filter(id_usuario=request.user.id)
    
    data= {
        'puntos': profile.objects.get(name_id=request.user.id).punctuation,
        'certamenes': certamenes,
        'n_certamenes': certamenes.count(),
            
    }
    return render(request,'app/registro_certamenes.html',data)

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

        padre_obj = None

        try:
            padre_id = int(request.POST.get("padre_identificador"))
        except:
            padre_id = None

        if padre_id:
            padre_qs = Comentario.objects.filter(id=padre_id)
            if padre_qs.exists() and padre_qs.count() == 1:
                padre_obj = padre_qs.first()


        comentarios, created = Comentario.objects.get_or_create(
            usuario = request.user,
            content_type = content_type,
            object_id = obj_id,
            texto = texto_data,
            padre = padre_obj
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

def eliminarComentario(request, id):
    instance = get_object_or_404(Comentario, id=id)

    if instance.usuario != request.user:

        response = HttpResponse("No eres el usuario que creó este comentario")
        response.status_code = 403
        return response

    if request.method == "POST":
        padre_instance_url = instance.content_object.get_absolute_url()
        instance.delete()
        messages.success(request, "Comentario eliminado")
        return HttpResponseRedirect(padre_instance_url)

    context = {
        'instance': instance
    }

    return render(request, 'app/eliminar.html', context )

#----Banco de preguntas----
def banco_preguntas(request):
    preguntas = PreguntasMate.objects.all()
    if request.method == 'POST':
        print(request.POST['Tema'])
        preguntas = PreguntasMate.objects.filter(tema=request.POST['Tema'])
    
    data = {
        'preguntas': preguntas,
    }
    return render(request,'app/banco_preguntas.html',data)