# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from blog_system import settings
from blog.models import Category
from blog.models import BlogEntry


def blog_context_processor(request):
    context = {
        "Locale": settings.LANGUAGE_CODE,
        "Type": settings.SITE_TYPE,
        "Title": settings.SITE_TITLE,
        "Descripcion": settings.SITE_DESCRIPTION,
        "Url": settings.SITE_URL,
        "Image": settings.SITE_IMAGE,
        "categorias": Category.objects.all(),
        "archive": BlogEntry.objects.filter(status='U').order_by('-created_at')
    }
    return context
