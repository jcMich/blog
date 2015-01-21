# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.db import models
from django.utils.text import slugify

STATUS_CHOICES = (
    (u'D', (u'Draft')),
    (u'P', (u'Public')),
    (u'H', (u'Hidden')),
)


class Categorias(models.Model):
    nombre  = models.CharField(max_length=30, primary_key=True, unique=True)
    descripcion = models.TextField()
    class Meta:
        verbose_name_plural = "Categorias"
    def __unicode__(self):
        return "%s" % (self.nombre)


class Tags(models.Model):
    nombre = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = 'Tags'
    def __unicode__(self):
        return "%s" % (self.nombre)


class Blog(models.Model):
    def url(self, filename):
        filename, ext = os.path.splitext(filename.lower())
        filename = "%s->%s%s" % (slugify(filename), datetime.now().strftime('%Y-%m-%d.%H-%M-%S'), ext)
        return 'photos/%s' % filename

    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    perex = models.TextField(unique=True)
    content = models.TextField()
    imagen = models.ImageField(upload_to=url)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    categoria = models.ForeignKey(Categorias)
    comentar = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    tags.help_text = None

    def get_absolute_url(self):
        return '/blog/%s' % self.slug

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-time']


class comentarios(models.Model):
    Blog = models.ForeignKey(Blog)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    cuerpo = models.TextField(verbose_name="Comentario", max_length=120)
    fecha_pub = models.DateTimeField(auto_now_add=True, editable=False)
