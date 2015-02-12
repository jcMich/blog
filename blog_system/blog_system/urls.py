# from __future__ import
from django.conf.urls import patterns, include, url
from blog_system import settings
from blog.feeds import EntradasFeed
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from blog.views import LoginView


# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'login/$', LoginView.as_view(), name='login'),
                       url(r'logout/$', 'blog.views.log_out', name='logout'),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'blog/',include('blog.urls') , name='login'))