from django.conf.urls import url
from django.urls import path
from django.urls.conf import re_path
from .views import crearPregunta, index, matematica, iniciar_sesion,registrarse,logout_view, foro, mi_perfil, certamen, guardarPregunta, certamen, Comentarios_pk, comentario_id

urlpatterns = [
    path('', iniciar_sesion, name="iniciar_sesion"),
    path('home/',index,name='home'),
    path('MAT021/', matematica, name="MAT021"),
    path('crearPregunta/', crearPregunta, name="crearPregunta"),
    path('logout/', logout_view, name="logout"),
    path('registrarse/', registrarse, name="registrarse"),
    path('foro/', foro, name="foro1"),
    path('mi_perfil/', mi_perfil, name="mi_perfil"),
    path('certamen/', certamen, name="certamen"),
    path('post_id/<pk>/', Comentarios_pk, name='foro2'),
    path('comentario_id/<pk>/', comentario_id, name='foro3'),
    path('guardarPregunta/', guardarPregunta),
    path('certame/',certamen)
]
