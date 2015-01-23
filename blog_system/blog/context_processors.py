from blog_system import settings
from blog.models import Categorias
from blog_system.settings import TEMA
from blog.models import Blog

def tema():
    if TEMA == 'principal':
        return 'base.html'
    else:
        return 'base2.html'


def blog_context_processor(request):
    context = {
        "Locale": settings.LANGUAGE_CODE,
        "Type": settings.SITE_TYPE,
        "Title": settings.SITE_TITLE,
        "Descripcion": settings.SITE_DESCRIPTION,
        "Url": settings.SITE_URL,
        "Image": settings.SITE_IMAGE,
        "categorias": Categorias.objects.all(),
        "base": tema(),
        "archive": Blog.objects.filter(status='P').order_by('-time')
    }
    return context
