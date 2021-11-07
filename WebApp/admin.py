from django.contrib import admin

from WebApp.models import PreguntasMate, preguntaPrueba

class PreguntasMateAdmin(admin.ModelAdmin):
    list_display = ("siglas","dificultad","tema")
    search_fields = ("siglas","contenido")
    list_filter = ("siglas", "dificultad", "tema",)

admin.site.register(PreguntasMate,PreguntasMateAdmin)


#prueba de preguntas
admin.site.register(preguntaPrueba)