from django.conf.urls import patterns, include, url
from blog_system import settings
from blog.feeds import EntradasFeed
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from blog.views import LoginView

admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^$', 'django.contrib.auth.views.login',{'template_name':'login.html',name='login'}),
                       # url(r'^cerrar/$', 'django.contrib.auth.views.logout',{'template_name':'login.html',name='login'}),
                       # url de inicio antes de implementar el loggin
                       url(r'login/$', LoginView.as_view(), name='login'),
                       url(r'logout/$', 'blog.views.log_out', name='logout'),
                       url(r'^$', 'blog.views.home', name='home'),
                       # url(r'^blogs/(?P<pagina>\d+)/$', 'blog.views.blogs', name='blogs'),
                       # url(r'^categorias/$', 'blog.views.categorias', name='categorias'),
                       url(r'^base/$', 'blog.views.base', name='base'),
                       url(r'^demo/$', 'blog.views.demo', name='demo'),
                       # url(r'^blog/(?P<slug>[-\w]+)/$', 'blog.views.blog', name='blog'),
                       url(r'^blog/(?P<id_blog>\d+)/$', 'blog.views.blog', name='blog'),
                       url(r'^busqueda/$', 'blog.views.busqueda', name='busqueda'),
                       #url(r'^comentar/(?P<id_blog>\d+)/$', 'blog.views.comentar', name='comentar'),
                       url(r'^contacto/$', 'blog.views.contacto_view', name='vista_contacto'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       url(r'^feeds/$', EntradasFeed()),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       #---------------------
                       url(r'^categoria/(?P<nombre_categoria>\w+)/$', 'blog.views.categoria', name='categoria'),
                       url(r'^addpost/$', 'blog.views.addpost', name='nuevo_post'),
                       url(r'^addcategoria/$', 'blog.views.addCategoria', name='addCategoria'),
                       url(r'^addtags/$', 'blog.views.addtags', name='addtags')
)
