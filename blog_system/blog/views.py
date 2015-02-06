# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from .models import Blog, comentarios, Tags, Categories, STATUS_CHOICES
from django.shortcuts import render_to_response, render
from .forms import ComentarioForm, ContactForm, LoginForm, addpostForm, categories_form, filter_form
from django.utils.text import slugify
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from endless_pagination.views import AjaxListView
from django.db.models import Q
import json

MONTHS_DIC = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}


class Home(ListView):
    model = Blog
    context_object_name = 'posts'
    paginate_by = 8
    page_kwarg = 'page'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        if self.request.GET.get('category'):
            ctx['category'] = self.request.GET.get('category')
        return ctx

    def get(self, request, *args, **kwargs):
        c = request.GET.get('category')
        if c:
            self.queryset = Blog.objects.filter(categoria__nombre=c).filter(status='P').order_by('-time')
        else:
            self.queryset = Blog.objects.filter(status='P').order_by('-time')
        return super(Home, self).get(request, *args, **kwargs)


class Month(AjaxListView):
    context_object_name = "posts"
    model = Blog

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        if year and month:
            return Blog.objects.filter(time__year=int(year), time__month=MONTHS_DIC[month]).filter(status='P').order_by('-time')
        else:
            return Blog.objects.all()

    template_name = 'archive.html'
    page_template = 'archive_page.html'


class AdminEntries(ListView):
    model = Blog
    context_object_name = 'posts'
    template_name = 'admin_entries.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminEntries, self).get_context_data(**kwargs)
        ctx['status'] = STATUS_CHOICES
        if self.request.GET.get('search') or self.request.GET.get('category') or self.request.GET.get('status'):
            ctx['form'] = filter_form({'search': self.request.GET.get('search'), 'category': self.request.GET.get('category'), 'status': self.request.GET.get('status')})
        else:
            ctx['form'] = filter_form()
        return ctx

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            postid = request.POST.get('id')
            newcate = request.POST.get('categoria')
            newstatus = request.POST.get('estado')
            coment = request.POST.get('comentario') == 'true'
            post = Blog.objects.get(pk=postid)
            post.comentar = coment
            post.categoria = Categories.objects.get(nombre=newcate)
            post.status = newstatus
            post.save()
            return HttpResponse(json.dumps({"Success": "Success"}), content_type="application/json")

    def get(self, request, *args, **kwargs):
            filter_search = request.GET.get('search')
            filter_category = request.GET.get('category')
            filter_status = request.GET.get('status')
            if filter_search:
                self.queryset = Blog.objects.filter(Q(content__icontains=filter_search) | Q(tags__nombre__icontains=filter_search)).distinct().order_by('-time')
            else:
                self.queryset = Blog.objects.all().order_by('-time')
            if filter_category:
                self.queryset = Blog.objects.all().filter(categoria=filter_category)
            if filter_status:
                self.queryset = Blog.objects.all().filter(status=filter_status)
            return super(AdminEntries, self).get(request, *args, **kwargs)


class CreateCategory(FormView):
    form_class = categories_form
    template_name = 'edit_entry.html'

    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        descripcion = form.cleaned_data['descripcion']
        cate, created = Categories.objects.get_or_create(nombre=nombre, descripcion=descripcion)
        cate.save()
        return super(CreateCategory, self).form_valid(form)


class AddPost(CreateView):
    form_class = addpostForm
    initial = {'status': 'D'}
    template_name = 'edit_entry.html'

    def get_context_data(self, **kwargs):
        ctx = super(AddPost, self).get_context_data(**kwargs)
        ctx['category_form'] = categories_form()
        return ctx

    def form_valid(self, form):
        post = form.save(commit=False)
        tags = unicode(form.cleaned_data['tags'])
        tags = tags.split(',')
        lst_tgs = []
        for tag in tags:
            t = Tags.objects.get_or_create(nombre=tag)
            lst_tgs.append(t[0])
        slg = slugify(form.cleaned_data['title'])
        post.slug = slg
        post.save()
        post.tags = lst_tgs
        post.save()
        return HttpResponseRedirect(reverse('home'))


class EditPost(UpdateView):
    form_class = addpostForm
    template_name = 'edit_entry.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = Blog.objects.get(slug=self.kwargs['slug'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(EditPost, self).get_context_data(**kwargs)
        ctx['category_form'] = categories_form()
        return ctx

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        tags = unicode(form.cleaned_data['tags'])
        tags = tags.split(',')
        lst_tgs = []
        for tag in tags:
            t = Tags.objects.get_or_create(nombre=tag)
            lst_tgs.append(t[0])
        slg = slugify(form.cleaned_data['title'])
        self.obj.slug = slg
        self.obj.save()
        self.obj.tags = lst_tgs
        self.obj.save()
        return HttpResponseRedirect(reverse('edit_entries'))


class AdminCategories(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminCategories, self).get_context_data(**kwargs)
        ctx['form'] = categories_form()
        return ctx

    def get_queryset(self):
        qs = super(AdminCategories, self).get_queryset()
        return qs.exclude(nombre="Default")

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            category = Categories.objects.get(nombre=request.POST.get('category'))
            default = Categories.objects.get_or_create(nombre="Default", descripcion="Default")
            try:
                post = Blog.objects.get(categoria=category)
                post.categoria = default[0]
                post.save()
            except:
                pass
            category.delete()
            return HttpResponse(json.dumps({"Success": "Success"}), content_type="application/json")
        else:
            form = categories_form(request.POST or None)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                cate, created = Categories.objects.get_or_create(nombre=nombre, descripcion=descripcion)
            return HttpResponseRedirect(reverse('categories'))


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        usuario = authenticate(username=usuario, password=password)
        if usuario is not None and usuario.is_active:
            login(self.request, usuario)
        return super(LoginView, self).form_valid(form)


class BlogDetail(DetailView):
    model = Blog
    template_name = 'article.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super(BlogDetail, self).get_context_data(**kwargs)
        ctx['comentarios'] = comentarios.objects.filter(Blog__slug=self.kwargs['slug']).order_by('-fecha_pub')
        ctx['comentariosForm'] = ComentarioForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.Blog = Blog.objects.get(slug=self.kwargs['slug'])
            comentario.nombre = form.cleaned_data['nombre']
            comentario.cuerpo = form.cleaned_data['cuerpo']
            comentario.save()
            return HttpResponseRedirect('/blog/%s' % self.kwargs['slug'])
        else:
            return HttpResponseRedirect('/blog/%s' % self.kwargs['slug'])


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
