# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES = (
    ('D', 'Draft'),
    ('U', 'Published'),
    ('H', 'Hidden'),
)


class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name.encode('utf-8')


class Tags(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


def set_default_cat():
        cate, created = Category.objects.get_or_create(name='Default', description='Default category on delete')
        return cate


class BlogEntry(models.Model):
    def url(self, filename):
        filename, ext = os.path.splitext(filename.lower())
        filename = "%s->%s%s" % (slugify(filename), datetime.now().strftime('%Y-%m-%d.%H-%M-%S'), ext)
        return 'photos/%s' % filename

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    slug = models.SlugField()
    abstract = models.TextField(unique=True, verbose_name=_("Abstract"))
    content = models.TextField(verbose_name=_("Content"))
    image = models.ImageField(upload_to=url, verbose_name=_("Image"))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name=_("Status"))
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.SET(set_default_cat))
    comment = models.BooleanField(default=False, verbose_name=_("Comment"))
    tags = models.ManyToManyField(Tags, help_text=None, verbose_name=_("Tags"))

    def get_absolute_url(self):
        return reverse('post', args=[str(self.slug)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class comentarios(models.Model):
    Blog = models.ForeignKey(BlogEntry)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    cuerpo = models.TextField(verbose_name="Comentario", max_length=120)
    fecha_pub = models.DateTimeField(auto_now_add=True, editable=False)
