from django import forms
from .models import PostForo

class FormComentarios(forms.Form):

    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    texto = forms.CharField(widget=forms.Textarea)

class FormForo(forms.ModelForm):
    class Meta:
        model = PostForo
        fields = ('sigla', 'texto', 'usuario',)

