from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    resolved_questions = models.IntegerField(default=0)
    punctuation = models.IntegerField(default=0)

class problema(models.Model):
    exercise = models.TextField()
    alternative = models.TextField()
    solution = models.CharField(max_length=1)
    times_tried = models.IntegerField()
    times_result = models.IntegerField()
    points = models.IntegerField()
    difficulty = models.IntegerField()

class PreguntasMate(models.Model):

    #---Descripcion de las preguntas---
    siglas = models.CharField(max_length=7)
    dificultad = models.CharField(max_length=20)
    tema = models.CharField(max_length=200)

    #---Pregunta y un posible desarrollo---
    pregunta = models.TextField()
    posible_desarrollo = models.TextField()

    #---alternativas---
    alternativa_a = models.CharField(null=True, max_length=100)
    alternativa_b = models.CharField(null=True, max_length=100)
    alternativa_c = models.CharField(null=True, max_length=100)
    alternativa_d = models.CharField(null=True, max_length=100)
    alternativa_e = models.CharField(null=True, max_length=100)

    #---Alternativa correcta---
    alternativa_correcta = models.CharField(null=True, max_length=1)

    #---Pistas y puntos de la pregunta---
    pista = models.CharField(max_length=200)
    puntos = models.IntegerField()




#modelo prueba de pregunta
class preguntaPrueba(models.Model):
    nombre_pregunta = models.CharField(max_length=50)
    texto = models.TextField(max_length=200)
    pregunta_math = models.TextField(max_length=200)
    alternativa_a =  models.TextField(max_length=200)
    alternativa_b =  models.TextField(max_length=200)
    alternativa_c =  models.TextField(max_length=200)
    alternativa_d =  models.TextField(max_length=200)
    solucion_math = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre_pregunta


