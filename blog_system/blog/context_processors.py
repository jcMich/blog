from blog_system.settings import (
    SITE_DESCRIPTION,
    SITE_LOCALE,
    SITE_TYPE,
    SITE_TITLE,
    SITE_URL,
    SITE_IMAGE,
)
from blog.models import Categorias
from blog_system.settings import TEMA


def tema():
    if TEMA == 'principal':
        return 'base.html'
    else:
        return 'base2.html'


def blog_context_processor(request):
    context = {
        "Locale": SITE_LOCALE,
        "Type": SITE_TYPE,
        "Title": SITE_TITLE,
        "Descripcion": SITE_DESCRIPTION,
        "Url": SITE_URL,
        "Image": SITE_IMAGE,
        "categorias": Categorias.objects.all(),
        "base": tema()
    }
    return context
