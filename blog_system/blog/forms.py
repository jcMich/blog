# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from ckeditor.widgets import CKEditorWidget
from .models import comentarios, BlogEntry, Category, Tags
# from crispy_forms.bootstrap import AppendedText, PrependedText, AppendedPrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML, Div, Button
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = comentarios
        fields = ('nombre', 'cuerpo')


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Porfavor ingrese un %(username)s y password correctos. "
                           "Nota: Los campos son sensibles a mayusculas y minusculas"),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'new-cate'
        self.helper.form_action = reverse('create_category')
        self.helper.layout = Layout(
            Div(
                Field('username'),
                Field('password'),
                Submit('submit', _("Log in"), css_id='save_data'),
                Button('cancel', _("Cancel"), css_class='btn btn-default', css_id='cancel-cate'),
            ),
        )


class DeleteCategory(forms.Form):
    category_name = forms.CharField()


class UpdatePostForm(forms.Form):
    post_id = forms.CharField()
    comment = forms.CharField()
    category = forms.CharField()
    status = forms.CharField()


class PostForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='full_ckeditor'))
    abstract = forms.CharField(widget=CKEditorWidget(config_name='basic_ckeditor'))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'inserta aqui los tags separados por , '}))
    comment = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            HTML('{{ form.media }}'),
            Div(
                Field('title'),
            ),
            Div(
                Div(
                    HTML('<label class="control-label col-lg-2">{{ form.abstract.label }}</label>'),  # In the end of the Form a js code erese a class.
                ),
                Div(
                    HTML('{{ form.abstract }}'),
                    css_class='col-lg-8'
                ),
                css_class='form-group',
            ),
            Div(
                Div(
                    HTML('<label class="control-label col-lg-2">{{ form.content.label }}</label>'),
                ),
                Div(
                    HTML('{{ form.content }}'),
                    css_class='col-lg-8'
                ),
                css_class='form-group',
            ),
            Div(
                Field('image'),
            ),
            Div(
                Field('status'),
            ),
            Div(
                Field('category'),
            ),
            Div(
                Field('comment'),
            ),
            Div(
                Field('tags'),
            ),
            Div(
                Submit('submit', _("Save and exit")),
                Button('Cancel', _("Cancel"), css_class='btn btn-danger'),
                css_class='col-lg-9 col-lg-offset-1'
            ),
        )

    class Meta:
        model = BlogEntry
        exclude = {'tags', 'slug'}
        # widgets = {'tags':forms.TextInput()}


class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'new-cate'
        self.helper.form_action = reverse('create_category')
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('description'),
                Submit('submit', _("Add"), css_id='save_data'),
                Button('Cancel', _("Cancel"), css_class='btn btn-default', css_id='cancel-cate'),
            ),
        )

    class Meta:
        model = Category


class tags_form(ModelForm):
    class Meta:
        model = Tags


class filter_form(forms.Form):
    STATUS = (
        ('', '-------'),
        ('D', 'Draft'),
        ('U', 'Published'),
        ('H', 'Hidden'),
    )
    search = forms.CharField(required=False)
    category = forms.ModelChoiceField(Category.objects.all(), required=False)
    status = forms.ChoiceField(choices=STATUS, required=False)

    helper = FormHelper()
    helper.form_method = "GET"
    helper.disable_csrf = True
    helper.form_show_labels = False
    helper.layout = Layout(
        Div(
            Div(
                Field('search', placeholder=_("Search..."), css_class='form-control'),
                css_class="col-xs-4"
            ),
            Div(
                Field('category', css_class='form-control'),
                css_class="col-xs-4"
            ),
            Div(
                Field('status', css_class='form-control'),
                css_class="col-xs-2"
            ),
            Div(
                Submit('submit', _("Filter"), css_class="col-md-12"),
                css_class="col-xs-2"
            ),
            css_class="col-md-8 col-md-offset-4"
        )
    )
