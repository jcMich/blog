from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from models import comentarios, Blog, Categorias, Tags


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = comentarios
        fields = ('nombre', 'cuerpo')


class ContactForm(forms.Form):
    Email = forms.EmailField(widget=forms.TextInput())
    Titulo = forms.CharField(widget=forms.TextInput())
    Texto = forms.CharField(widget=forms.Textarea())


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))


class addpostForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='full_ckeditor'))
    perex = forms.CharField(widget=CKEditorWidget(config_name='basic_ckeditor'))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'inserta aqui los tags separados por , '}))
    comentar = forms.BooleanField()
    class Meta:
        model = Blog
        exclude ={'tags', 'slug'}
        # widgets = {'tags':forms.TextInput()}


class categoria_form(ModelForm):
    class Meta:
        model = Categorias


class tags_form(ModelForm):
    class Meta:
        model = Tags
