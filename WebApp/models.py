from typing import TextIO
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.fields import CharField, IntegerField
from django.db.models.signals import pre_save, post_save
from django.shortcuts import render
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse


#----------------- Choices para modelos ---------------------------------- 

siglas = [
    ('MAT021', 'Mat-021'),
    ('MAT022', 'Mat-022'),
    ('MAT023', 'Mat-023'),
    ('MAT024', 'Mat-024'),
]

temas = [
    ('numeros_reales', 'Números Reales'),
    ('funciones', 'Funciones'),
    ('limite', 'Límites'),
    ('continuidad', 'Continuidad'),
    ('calculo_diferencial', 'Cálculo Diferencial'),
    ('logica_proposicional', 'Lógica Proposicional'),
    ('conjunto', 'Conjuntos'),
    ('relaciones', 'Relaciones'),
    ('trigonometria', 'Trigonometría'),
    ('exponencial_logaritmo', 'Exponencial y Logaritmo'),
    ('geometria_analitica', 'Geometría Analítica'),
    ('induccion', 'Inducción'),
    ('sumatoria_productoria', 'Sumatoria y Productoria'),
    ('numeros_complejos', 'Números Complejos'),
    ('polinomios', 'Polinomios'),
]

dificultad = [
    ('FACIL', 'Fácil'),
    ('MEDIA', 'Media'),
    ('DIFICIL', 'Difícil'),
]

alt_correcta = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
]

#----------------------------- modelo perfil de usuario -------------------
class profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    resolved_questions = models.IntegerField(default=0)
    punctuation = models.IntegerField(default=0)

def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile.objects.create(name=instance)
post_save.connect(create_profile, sender=User)

class problema(models.Model):
    exercise = models.TextField()
    alternative = models.TextField()
    solution = models.CharField(max_length=1)
    times_tried = models.IntegerField()
    times_result = models.IntegerField()
    points = models.IntegerField()
    difficulty = models.IntegerField()

#-------------------------------- Modelos Para Foro -------------------------------------------

class PostForo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sigla = models.CharField(max_length=7, choices=siglas)
    texto = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    tiempo = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('foro2', kwargs={'pk': self.pk})

    def comentarios(self):
        instance = self
        qs = Comentario.objects.filtro_por_instancia(instance)
        return qs

    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(PostForo)
        return content_type

    class Meta:
        ordering = ['-tiempo']

def nueva_url(instance, url=None):
    
    slug = slugify(instance.texto)

    if url is not None:
        slug = url
    
    qs =  PostForo.objects.filter(slug=slug).order_by("-id")

    if qs.exists():
        nueva_url_1 = '%s-%s'%(slug, qs.first().id)
        return nueva_url(instance, url= nueva_url_1)

    return slug

def url_creada(sender, instance, *args, **kwargs):

    if not instance.slug:

        instance.slug = nueva_url(instance)

pre_save.connect(url_creada, sender = PostForo)

class ComentarioManager(models.Manager):

    def filtro_por_instancia(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ComentarioManager, self).filter(content_type= content_type, object_id = obj_id)
        return qs

class Comentario(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default=1)
    texto = models.TextField(verbose_name="Comentario")
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    tiempo = models.DateTimeField(auto_now_add=True)

    objects = ComentarioManager()

    def get_absolute_url(self):
        return reverse("foro3", kwargs={"pk": self.pk})

    def __str__(self):
        return self.texto[:20]
        

    class Meta:
        ordering = ['-tiempo']

#-------------------------- Modelo Preguntas Mate -------------------------
class PreguntasMate(models.Model):

    #---Descripcion de las preguntas---
    siglas = models.CharField(max_length=7, choices=siglas)
    dificultad = models.CharField(max_length=20, choices=dificultad)
    tema = models.CharField(max_length=100, choices=temas)

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
    alternativa_correcta = models.CharField(null=True, max_length=1, choices=alt_correcta)

    #---Pistas y puntos de la pregunta---
    pista = models.CharField(max_length=200)
    puntos = models.IntegerField()

#-------------------------- modelo prueba de pregunta ---------------------
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

#-------------------------- modelo historial de certamenes ---------------------
class historialCertamen(models.Model):
    id_usuario = models.IntegerField()
    id_preguntas = models.CharField(max_length=50)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    id_certamen = models.CharField(max_length=20, default="")