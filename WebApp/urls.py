from django.urls import path
from .views import crearPregunta, index, matematica, iniciar_sesion,registrarse,logout_view, foro1, mi_perfil, certamen, guardarPregunta, certamen

urlpatterns = [
    path('', iniciar_sesion, name="iniciar_sesion"),
    path('home/',index,name='home'),
    path('MAT021/', matematica, name="MAT021"),
    path('crearPregunta/', crearPregunta, name="crearPregunta"),
    path('logout/', logout_view, name="logout"),
    path('registrarse/', registrarse, name="registrarse"),
    path('foro/', foro1, name="foro1"),
    path('mi_perfil/', mi_perfil, name="mi_perfil"),
    path('certamen/', certamen, name="certamen"),
    #prueba
    path('guardarPregunta/', guardarPregunta),
    path('certame/',certamen)
]
