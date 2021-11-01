from django.urls import path
from .views import quimica, index, matematica, iniciar_sesion,registrarse

urlpatterns = [
    path('', iniciar_sesion, name="iniciar_sesion"),
    path('home/',index,name='home'),
    path('matematica/', matematica, name="matematica"),
    path('quimica/', quimica, name="quimica"),
    #path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('registrarse/', registrarse, name="registrarse"),
]
