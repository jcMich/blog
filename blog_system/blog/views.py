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
from endless_pagination.views import AjaxListView, AjaxMultipleObjectTemplateResponseMixin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
import json


MONTHS_DIC = {
    _('January'): 1, _('February'): 2, _('March'): 3, _('April'): 4, _('May'): 5, _('June'): 6,
    _('July'): 7, _('Agoust'): 8, _('September'): 9, _('October'): 10, _('November'): 11, _('December'): 12
}


class Home(ListView, AjaxMultipleObjectTemplateResponseMixin):
    model = BlogEntry
    context_object_name = 'posts'
    paginate_by = 6
    page_kwarg = 'page'
    template_name = 'blog/index.html'
    page_template = 'blog/archive_entries.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        if self.request.GET.get('category'):
            ctx['category'] = self.request.GET.get('category')
        if self.request.GET.get('year') and self.request.GET.get('month'):
            ctx['endlesspagination'] = True
        return ctx

    def get_queryset(self):
        c = self.request.GET.get('category')
        y = self.request.GET.get('year')
        m = self.request.GET.get('month')
        if c:
            return BlogEntry.objects.filter(category__name=c).filter(status='U').order_by('-created_at')
        elif y and m:
            self.paginate_by = None
            return BlogEntry.objects.filter(created_at__year=int(y), created_at__month=MONTHS_DIC[m])
        return BlogEntry.objects.filter(status='U').order_by('-created_at')


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
            return BlogEntry.objects.all()  # agregar filtro para solo mostrar estado published


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


class BaseBlogEntry(FormView):
    form_class = PostForm
    template_name = 'blog/edit_entry.html'
    success_url = reverse_lazy('edit_entries')

    def get_context_data(self, **kwargs):
        context = super(BaseBlogEntry, self).get_context_data(**kwargs)
        context['category_form'] = CategoryForm()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        tags = unicode(form.cleaned_data['tags']).split(',')
        lst_tgs = []
        for tag in tags:
            lst_tgs.append(Tags.objects.get_or_create(name=tag)[0])
        post.slug = slugify(form.cleaned_data['title'])
        post.save()
        post.tags = lst_tgs
        return super(BaseBlogEntry, self).form_valid(form)


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
        user = form.cleaned_data['username']
        passw = form.cleaned_data['password']

        user = authenticate(username=user, password=passw)

        if user is not None and user.is_active:
            login(self.request, user)
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
            comentario.save()
            return HttpResponseRedirect(reverse('post', kwargs={'slug': self.kwargs['slug']}))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


home = Home.as_view()
month = Month.as_view()
admin_entries = login_required(AdminEntries.as_view())
blog_entry_detail = BlogEntryDetail.as_view()
create_blog_entry = login_required(CreateBlogEntry.as_view())
update_blog_entry = login_required(UpdateBlogEntry.as_view())
create_category = login_required(CreateCategory.as_view())
admin_categories = login_required(AdminCategories.as_view())
