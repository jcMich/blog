# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.core.urlresolvers import reverse, reverse_lazy
from .models import BlogEntry, comentarios, Tags, Category, STATUS_CHOICES
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
    model = BlogEntry
    context_object_name = 'posts'
    paginate_by = 2
    page_kwarg = 'page'
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        if self.request.GET.get('category'):
            ctx['category'] = self.request.GET.get('category')
        return ctx

    def get(self, request, *args, **kwargs):
        c = request.GET.get('category')
        if c:
            self.queryset = BlogEntry.objects.filter(category__name=c).filter(status='U').order_by('-created_at')
        else:
            self.queryset = BlogEntry.objects.filter(status='U').order_by('-created_at')
        return super(Home, self).get(request, *args, **kwargs)


class Month(AjaxListView):
    context_object_name = 'posts'
    model = BlogEntry
    template_name = 'blog/archive.html'
    page_template = 'blog/archive_page.html'

    def get_queryset(self):
        y = self.kwargs['year']
        m = self.kwargs['month']
        if y and m:
            archive_filter = BlogEntry.objects.filter(created_at__year=int(y), created_at__month=MONTHS_DIC[m])
            return archive_filter.filter(status='U').order_by('-created_at')
        else:
            return BlogEntry.objects.all()


class AdminEntries(ListView):
    model = BlogEntry
    context_object_name = 'posts'
    paginate_by = 8
    page_kwarg = 'page'
    template_name = 'blog/admin_entries.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminEntries, self).get_context_data(**kwargs)
        request_get = self.request.GET.copy()
        if 'page' in request_get:
            del request_get['page']
        ctx['get_query'] = request_get
        ctx['status'] = STATUS_CHOICES
        if self.request.GET.get('search') or self.request.GET.get('category') or self.request.GET.get('status'):
            ctx['form'] = filter_form({'search': self.request.GET.get('search'),
                                       'category': self.request.GET.get('category'),
                                       'status': self.request.GET.get('status')})
        else:
            ctx['form'] = filter_form()
        return ctx

    def post(self, request):
        form = UpdatePostForm(request.POST)
        if self.request.is_ajax() and form.is_valid():
            postid = form.cleaned_data['post_id']
            newcate = form.cleaned_data['category']
            newstatus = form.cleaned_data['status']
            comment = form.cleaned_data['comment'] == 'true'
            post = get_object_or_404(BlogEntry, pk=postid)
            post.comment = comment
            post.category = get_object_or_404(Category, name=newcate)
            post.status = newstatus
            post.save()
            return HttpResponse(json.dumps({'Success': 'Success'}), content_type='application/json')

    def get(self, request, *args, **kwargs):
        filter_search = request.GET.get('search')
        filter_category = request.GET.get('category')
        filter_status = request.GET.get('status')
        if filter_search:
            self.queryset = BlogEntry.objects.filter(Q(title__icontains=filter_search) |
                                                     Q(tags__name__icontains=filter_search)).distinct().order_by('-created_at')
        else:
            self.queryset = BlogEntry.objects.all().order_by('-created_at')
        if filter_category:
            self.queryset = self.queryset.filter(category=filter_category)
        if filter_status:
            self.queryset = self.queryset.filter(status=filter_status)
        return super(AdminEntries, self).get(request, *args, **kwargs)


class BaseBlogEntry(View):
    form_class = PostForm
    template_name = 'blog/edit_entry.html'

    def get_context_data(self, **kwargs):
        context = super(BaseBlogEntry, self).get_context_data(**kwargs)
        context['category_form'] = CategoryForm()
        return context

    def get_object(self, queryset=None):
        post = BlogEntry.objects.all()
        return post

    def form_valid(self, form):
        self.post = form.save(commit=False)
        tags = unicode(form.cleaned_data['tags'])
        tags = tags.split(',')
        lst_tgs = []
        for tag in tags:
            t = Tags.objects.get_or_create(name=tag)
            lst_tgs.append(t[0])
        slg = slugify(form.cleaned_data['title'])
        self.post.slug = slg
        self.post.save()
        self.post.tags = lst_tgs
        self.post.save()
        return HttpResponseRedirect(reverse('edit_entries'))


class CreateBlogEntry(BaseBlogEntry, CreateView):
    initial = {'status': 'D'}


class UpdateBlogEntry(BaseBlogEntry, UpdateView):
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(BlogEntry, slug=self.kwargs['slug'])
        return post


class AdminCategories(ListView):
    model = Category
    context_object_name = 'model'
    template_name = 'blog/categories.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminCategories, self).get_context_data(**kwargs)
        ctx['form'] = CategoryForm()
        ctx['template_title'] = self.model._meta.object_name
        ctx['js_functions'] = 'category_template()'
        return ctx

    def get_queryset(self):
        qs = super(AdminCategories, self).get_queryset()
        return qs.exclude(name="Default")

    def post(self, request, *args, **kwargs):
        form = DeleteCategory(request.POST)
        if self.request.is_ajax() and form.is_valid():
            category = get_object_or_404(Category, name=form.cleaned_data['category_name'])
            default = Category.objects.get_or_create(name='Default', description='Default')
            try:
                post = get_object_or_404(BlogEntry, category=category)
                post.category = default[0]
                post.save()
            except:
                pass
            category.delete()
            return HttpResponse(json.dumps({'Success': 'Success'}), content_type='application/json')


class CreateCategory(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse('home'))
        return super(CreateCategory, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cate, created = Category.objects.get_or_create(name=name, description=description)
            return HttpResponse(json.dumps({'name': cate.name, 'created': created}), content_type='application/json')
        return HttpResponse(json.dumps({'created': False}), content_type='application/json')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        usuario = authenticate(username=usuario, password=password)
        if usuario is not None and usuario.is_active:
            login(self.request, usuario)
        return super(LoginView, self).form_valid(form)


class BlogEntryDetail(DetailView):
    model = BlogEntry
    template_name = 'blog/article.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super(BlogEntryDetail, self).get_context_data(**kwargs)
        ctx['comentarios'] = comentarios.objects.filter(Blog__slug=self.kwargs['slug']).order_by('-fecha_pub')
        ctx['comentariosForm'] = ComentarioForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.Blog = get_object_or_404(BlogEntry, slug=self.kwargs['slug'])
            comentario.nombre = form.cleaned_data['nombre']
            comentario.cuerpo = form.cleaned_data['cuerpo']
            comentario.save()
            return HttpResponseRedirect(reverse('post/detail/', kwargs={'slug': self.kwargs['slug']}))


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


home = Home.as_view()
month = Month.as_view()
admin_entries = login_required(AdminEntries.as_view())
blog_entry_detail = BlogEntryDetail.as_view()
create_blog_entry = login_required(CreateBlogEntry.as_view())
update_blog_entry = login_required(UpdateBlogEntry.as_view())
create_category = login_required(CreateCategory.as_view())
admin_categories = login_required(AdminCategories.as_view())
