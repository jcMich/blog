# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.core.urlresolvers import reverse
from .models import Blog, comentarios, Tags, Categories, STATUS_CHOICES
from .forms import ComentarioForm, UpdatePostForm, LoginForm, PostForm, CategoryForm, filter_form, DeleteCategory
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

    template_name = 'archive.html'
    page_template = 'archive_page.html'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        if year and month:
            return Blog.objects.filter(time__year=int(year), time__month=MONTHS_DIC[month]).filter(status='P').order_by('-time')
        else:
            return Blog.objects.all()


class AdminEntries(ListView):
    model = Blog
    context_object_name = 'posts'
    paginate_by = 8
    page_kwarg = 'page'
    template_name = 'admin_entries.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminEntries, self).get_context_data(**kwargs)
        request_get = self.request.GET.copy()
        if (request_get.has_key('page')):
            del request_get['page']
        ctx['get_query'] = request_get
        ctx['status'] = STATUS_CHOICES
        if self.request.GET.get('search') or self.request.GET.get('category') or self.request.GET.get('status'):
            ctx['form'] = filter_form({'search': self.request.GET.get('search'), 'category': self.request.GET.get('category'), 'status': self.request.GET.get('status')})
        else:
            ctx['form'] = filter_form()
        return ctx

    def post(self, request, *args, **kwargs):
        form = UpdatePostForm(request.POST)
        if self.request.is_ajax() and form.is_valid():
            postid = form.cleaned_data['post_id']
            newcate = form.cleaned_data['category']
            newstatus = form.cleaned_data['status']
            comment = form.cleaned_data['comment'] == 'true'
            post = Blog.objects.get(pk=postid)
            post.comentar = comment
            post.categoria = Categories.objects.get(nombre=newcate)
            post.status = newstatus
            post.save()
            return HttpResponse(json.dumps({"Success": "Success"}), content_type="application/json")

    def get(self, request, *args, **kwargs):
            filter_search = request.GET.get('search')
            filter_category = request.GET.get('category')
            filter_status = request.GET.get('status')
            if filter_search:
                self.queryset = Blog.objects.filter(Q(title__icontains=filter_search) | Q(tags__nombre__icontains=filter_search)).distinct().order_by('-time')
            else:
                self.queryset = Blog.objects.all().order_by('-time')
            if filter_category:
                self.queryset = self.queryset.filter(categoria=filter_category)
            if filter_status:
                self.queryset = self.queryset.filter(status=filter_status)
            return super(AdminEntries, self).get(request, *args, **kwargs)


class Post(View):
    form_class = PostForm
    template_name = 'edit_entry.html'

    def get_context_data(self, **kwargs):
        ctx = super(Post, self).get_context_data(**kwargs)
        ctx['category_form'] = CategoryForm()
        return ctx

    def get_object(self, queryset=None):
        post = Blog.objects.all()
        return post

    def form_valid(self, form):
        self.post = form.save(commit=False)
        tags = unicode(form.cleaned_data['tags'])
        tags = tags.split(',')
        lst_tgs = []
        for tag in tags:
            t = Tags.objects.get_or_create(nombre=tag)
            lst_tgs.append(t[0])
        slg = slugify(form.cleaned_data['title'])
        self.post.slug = slg
        self.post.save()
        self.post.tags = lst_tgs
        self.post.save()
        return HttpResponseRedirect(reverse('edit_entries'))


class AddPost(Post, CreateView):
    initial = {'status': 'D'}


class EditPost(Post, UpdateView):
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = Blog.objects.get(slug=self.kwargs['slug'])
        return post


class AdminCategories(ListView):
    model = Categories
    context_object_name = 'model'
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminCategories, self).get_context_data(**kwargs)
        ctx['form'] = CategoryForm()
        ctx['js_functions'] = 'category_template()'
        return ctx

    def get_queryset(self):
        qs = super(AdminCategories, self).get_queryset()
        return qs.exclude(nombre="Default")

    def post(self, request, *args, **kwargs):
        form = DeleteCategory(request.POST)
        if self.request.is_ajax() and form.is_valid():
            category = Categories.objects.get(nombre=form.cleaned_data['category_name'])
            default = Categories.objects.get_or_create(nombre="Default", descripcion="Default")
            try:
                post = Blog.objects.get(categoria=category)
                post.categoria = default[0]
                post.save()
            except:
                pass
            category.delete()
            return HttpResponse(json.dumps({"Success": "Success"}), content_type="application/json")


class CreateCategory(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse('home'))
        return super(CreateCategory, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if self.request.is_ajax() and form.is_valid():
            name = form.cleaned_data['nombre']
            description = form.cleaned_data['descripcion']
            cate, created = Categories.objects.get_or_create(nombre=name, descripcion=description)
            cate.save()
            return HttpResponse(json.dumps({"Nombre": name, "Descripcion": description}), content_type="application/json")


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
            return HttpResponseRedirect(reverse('post/detail/', kwargs={'slug': self.kwargs['slug']}))


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
