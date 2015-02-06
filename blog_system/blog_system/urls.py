# from __future__ import
from django.conf.urls import patterns, include, url
from blog_system import settings
from blog.feeds import EntradasFeed
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from blog.views import LoginView, Home, BlogDetail, AdminEntries, AddPost, EditPost, AdminCategories, Month, CreateCategory

# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'login/$', LoginView.as_view(), name='login'),
                       url(r'logout/$', 'blog.views.log_out', name='logout'),
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^post/detail/(?P<slug>.*)/$', BlogDetail.as_view(), name='post'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^feeds/$', EntradasFeed()),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^post/add/$', AddPost.as_view(), name='new_post'),
                       url(r'^entries/$', AdminEntries.as_view(), name='edit_entries'),
                       url(r'^categories/$', AdminCategories.as_view(), name='categories'),
                       url(r'^category/add/$', CreateCategory.as_view(), name='create_category'),
                       url(r'^month/(?P<year>\d+)/(?P<month>\w+)/$', Month.as_view(), name='month'),
                       url(r'^post/edit/(?P<slug>.*)/$', EditPost.as_view(), name='edit'),
)