from django.contrib import admin

from WebApp.models import PreguntasMate

class PreguntasMateAdmin(admin.ModelAdmin):
    list_display = ("siglas","dificultad","contenido")
    search_fields = ("siglas","contenido")
    list_filter = ("siglas", "dificultad", "contenido",)

admin.site.register(PreguntasMate,PreguntasMateAdmin)