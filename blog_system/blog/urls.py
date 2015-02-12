from django.conf.urls import patterns, url, include
from blog.feeds import EntradasFeed
from blog.views import LoginView
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', settings.BLOG_ENTRIES_HOME_VIEW, name='home'),
                       url(r'^post/detail/(?P<slug>.*)/$', settings.BLOG_ENTRIES_ENTRY_DETAIL_VIEW, name='post'),
                       url(r'^feeds/$', EntradasFeed()),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^post/add/$', settings.BLOG_ENTRIES_ENTRY_CREATE_VIEW, name='new_post'),
                       url(r'^entries/$', settings.BLOG_ENTRIES_ENTRIES_ADMIN_VIEW, name='edit_entries'),
                       url(r'^categories/$', settings.BLOG_ENTRIES_CATEGORIES_ADMIN_VIEW, name='categories'),
                       url(r'^category/add/$', settings.BLOG_ENTRIES_CREATE_CATEGORY_VIEW, name='create_category'),
                       url(r'^month/(?P<year>\d+)/(?P<month>\w+)/$', settings.BLOG_ENTRIES_MONTH_VIEW, name='month'),
                       url(r'^post/edit/(?P<slug>.*)/$', settings.BLOG_ENTRIES_ENTRY_UPDATE_VIEW, name='edit'))