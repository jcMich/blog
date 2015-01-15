# -*- coding: utf-8 -*-
from django.db import models
from taggit_autosuggest.managers import TaggableManager
from taggit.models import TaggedItemBase, TagBase, GenericTaggedItemBase

STATUS_CHOICES = (
    (u'D', (u'Draft')),
    (u'P', (u'Public')),
    (u'H', (u'Hidden')),
)

class Categorias(models.Model):
    nombre  = models.CharField(max_length=30)
    descripcion = models.TextField()
    class Meta:
        verbose_name_plural = "stories"
    def __unicode__(self):
        return "%s" % (self.nombre)

class Tags(models.Model):
    nombre = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = 'Tags'
    def __unicode__(self):
        return "%s" % (self.nombre)

class Blog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    perex = models.TextField(unique=True)
    content = models.TextField()
    imagen = models.ImageField(upload_to='photos')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    categoria = models.ForeignKey(Categorias)
    comentar = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    tags.help_text=None

    @models.permalink
    def get_absolute_url(self):
        return ('blog', (self.slug))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-time']


class comentarios(models.Model):
    Blog = models.ForeignKey(Blog)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    cuerpo = models.TextField(verbose_name="Comentario", max_length=80)
    fecha_pub = models.DateTimeField(auto_now_add=True, editable=False)


class rating(models.Model):
    Blog = models.ForeignKey(Blog)
    calificacion = models.IntegerField(default=0)
