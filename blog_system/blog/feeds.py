from django.contrib.syndication.views import Feed
from blog.models import BlogEntry


class EntradasFeed(Feed):
    title = "Entradas"
    link = "/archive/"
    description = "Entradas al blog"

    def items(self):
        return BlogEntry.objects.order_by('-created_at')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "item.content"

    def item_link(self, item):
        return '/archive/'