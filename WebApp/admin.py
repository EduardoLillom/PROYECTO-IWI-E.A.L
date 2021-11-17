from django.contrib import admin
from WebApp.models import PreguntasMate, preguntaPrueba, PostForo, Comentario, profile

class PreguntasMateAdmin(admin.ModelAdmin):
    list_display = ("siglas","dificultad","tema")
    search_fields = ("siglas","contenido")
    list_filter = ("siglas", "dificultad", "tema",)

class PostForoAdmin(admin.ModelAdmin):
    search_fields = ('usuario','sigla','tiempo')
    list_filter = ('sigla','tiempo',)
    list_display = ('usuario','sigla','tiempo')

admin.site.register(PreguntasMate,PreguntasMateAdmin)
admin.site.register(PostForo, PostForoAdmin)
admin.site.register(Comentario)
admin.site.register(profile)
#prueba de preguntas
admin.site.register(preguntaPrueba)