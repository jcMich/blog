# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import Blog, comentarios, Tags, Categorias
from django.shortcuts import render_to_response, render
from forms import ComentarioForm, ContactForm, LoginForm, addpostForm, categoria_form
from django.template import RequestContext
from django.utils.text import slugify
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


class Home(ListView):
    model = Blog
    context_object_name = 'blogs'
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
            self.queryset = Blog.objects.filter(categoria__nombre=c).order_by('-time')
        else:
            self.queryset = Blog.objects.order_by('-time')
        return super(Home, self).get(request, *args, **kwargs)


class AddPost(CreateView):
    form_class = addpostForm
    template_name = 'newpost.html'
    success_url = '/'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        ctx = super(AddPost, self).get_context_data(**kwargs)
        ctx['categoria'] = categoria_form
        return ctx

    def post(self, request, *args, **kwargs):
        cform = categoria_form(request.POST)
        form = addpostForm(request.POST, request.FILES)
        if cform.is_valid():
            nombre = cform.cleaned_data['nombre']
            descripcion = cform.cleaned_data['descripcion']
            cate = Categorias.objects.get_or_create(nombre=nombre, descripcion=descripcion)
            cate.save()
        if form.is_valid():
            pass

def month(request, year, month):
    def month_names(month):
        return {
            "Enero":1, "Febrero":2, "Marzo":3, "Abril":4, "Mayo":5, "Junio":6,
            "Julio":7, "Agosto":8,"Septiembre":9, "Octubre":10, "Noviembre":11, "Diciembre":12
            }[month]
    posts = Blog.objects.filter(time__year=int(year), time__month=month_names(month)).order_by('-time')
    return render(request, "index.html", {"blogs":posts})


def addpost(request, template_name='newpost.html'):
    # strics in a POST or rendes empty form
    cform = categoria_form(request.POST or None)
    form = addpostForm(request.POST or None, request.FILES or None)
    if cform.is_valid():
        nombre = cform.cleaned_data['nombre']
        descripcion = cform.cleaned_data['descripcion']
        cate = Categorias.objects.get_or_create(nombre=nombre, descripcion=descripcion)
        cate.save()
        return HttpResponseRedirect('')
    if form.is_valid():
        blog = form.save(commit=False)
        tags = unicode(form.cleaned_data['tags'])
        tags = tags.split(',')
        lst_tgs = []
        for tag in tags:
            t = Tags.objects.get_or_create(nombre=tag)
            lst_tgs.append(t[0])
        slg = slugify(form.cleaned_data['title'])
        blog.slug = slg
        blog.save()
        blog.tags = lst_tgs
        blog.save()
        if request.POST.get("save_exit"):
            return HttpResponseRedirect('/')
        elif request.POST.get("save_continue"):
            form.clean()
            return HttpResponseRedirect('')
    return render(request, template_name, {'form':form, 'cform': cform})




# BORRAR Y AGREGAR AL FORMULARIO LA VIEW ADDPOST
def addCategoria(request, template_name='tagsandcate.html'):
    form = categoria_form(request.POST or None)
    if form.is_valid():
        form.save()
        if request.POST.get("save_exit"):
            return HttpResponseRedirect('/')
        elif request.POST.get("save_continue"):
            form.clean()
            return HttpResponseRedirect('')
    return render(request, template_name, {'form':form})


class BlogDetail(DetailView):
    model = Blog
    template_name = 'article.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        ctx = super(BlogDetail, self).get_context_data(**kwargs)
        ctx['comentarios'] = comentarios.objects.filter(Blog__slug=self.kwargs['slug']).order_by('-fecha_pub')
        ctx['comentariosForm'] = ComentarioForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.Blog = Blog.objects.get(pk=self.kwargs['pk'])
            comentario.nombre = form.cleaned_data['nombre']
            comentario.cuerpo = form.cleaned_data['cuerpo']
            comentario.save()
            return HttpResponseRedirect('/blog/%s' % self.kwargs['pk'])
        else:
            return HttpResponseRedirect('/blog/%s' % self.kwargs['pk'])


def contacto_view(request):
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]
    cate = Blog.categoria
    info_enviado = False  # definir si se envio la informacion
    email = ""
    titulo = ""
    texto = ""

    if request.method == "POST":
        formulario = ContactForm(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['Email']
            titulo = formulario.cleaned_data['Titulo']
            texto = formulario.cleaned_data['Texto']

            # enviando gmail
            to_admin = 'jc.fie.umich@gmail.com'
            html_content = "Informacion recibida <br><br><br>***Mensaje**<br><br>%s<br><br>Responde a: %s" % (texto, email)
            msg = EmailMultiAlternatives('Correo de contacto blog', html_content, 'from@server.com', [to_admin])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    else:
        formulario = ContactForm()
    ctx = {'form': formulario, 'email': email, 'titulo': titulo, 'texto': texto, 'info_enviado': info_enviado,
           'blogsRecientes': blogsRecientes, 'cate': cate}
    return render_to_response('contacto.html', ctx, context_instance=RequestContext(request))


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


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def about(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            titulo = form.cleaned_data['Titulo']
            texto = form.cleaned_data['Texto']

            to_admin = 'jc.fie.umich@gmail.com'
            html_context = "Informacion recibida <br><br><br>***Mensaje**<br><br>%s<br><br>Responde a: %s" % (texto, email)
            msg = EmailMultiAlternatives('Coreo de contacto bog', html_context, 'from@server.com', [to_admin])
            msg.attach_alternative(html_context, "text/html")
            msg.send()
            return HttpResponseRedirect('/')
        return render_to_response('about.html', {'form': form}, context_instance= RequestContext(request))
    return render_to_response('about.html', {'form': ContactForm()}, context_instance=RequestContext(request))
