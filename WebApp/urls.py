from django.urls import path
from .views import quimica, index, matematica, iniciar_sesion,registrarse,logout_view

urlpatterns = [
    path('', iniciar_sesion, name="iniciar_sesion"),
    path('home/',index,name='home'),
    path('matematica/', matematica, name="matematica"),
    path('quimica/', quimica, name="quimica"),
    path('logout/', logout_view, name="logout"),
    path('registrarse/', registrarse, name="registrarse"),
]
