from django.conf.urls import patterns, include, url
from blog_system import settings
from blog.feeds import EntradasFeed
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from blog.views import LoginView, Home, BlogDetail, AddPost

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'login/$', LoginView.as_view(), name='login'),
                       url(r'logout/$', 'blog.views.log_out', name='logout'),
                       url(r'about/$', 'blog.views.about', name='about'),
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^blog/(?P<slug>.*)/$', BlogDetail.as_view(), name='blog'),
                       url(r'^contacto/$', 'blog.views.contacto_view', name='vista_contacto'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       url(r'^feeds/$', EntradasFeed()),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^addpost/$', 'blog.views.addpost', name='nuevo_post'),
                       # url(r'^addpost/$', AddPost.as_view(), name='nuevo_post'),
                       url(r'^addcategoria/$', 'blog.views.addCategoria', name='addCategoria'),
                       url(r'^month/(?P<year>\d+)/(?P<month>\w+)/$', 'blog.views.month', name='month'),
                       url(r'^editposts/$','blog.views.editposts', name='editposts')
)
