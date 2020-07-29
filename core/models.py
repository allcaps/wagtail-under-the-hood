from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import Http404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from treebeard.mp_tree import MP_Node


class Site(models.Model):
    name = models.CharField(max_length=50)
    host = models.CharField(max_length=50)
    root_page = models.ForeignKey("Page", on_delete=models.PROTECT)


class Page(MP_Node):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    content_type = models.ForeignKey(ContentType, related_name="pages", on_delete=models.PROTECT)

    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        if not self.id:
            self.content_type = ContentType.objects.get_for_model(self)
        self.slug = slugify(self.title)

    def __str__(self):
        return self.title

    @property
    def specific(self):
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        return content_type.get_object_for_this_type(id=self.id)

    def get_context(self):
        return {"page": self}

    def serve(self, request):
        return render(request, f"core/{self.__class__.__name__.lower()}.html", self.get_context())

    def route(self, request, slugs):
        if slugs:
            child_slug = slugs[0]
            remaining_slugs = slugs[1:]
            try:
                sub_page = self.get_children().get(slug=child_slug)
            except Page.DoesNotExist:
                raise Http404
            return sub_page.specific.route(request, remaining_slugs)
        else:
            return self.serve(request)


class HomePage(Page):
    intro = models.TextField()

    def get_context(self):
        ctx = super(HomePage, self).get_context()
        ctx.update({"form": AuthenticationForm})
        return ctx


class ListPage(Page):
    pass


class DetailPage(Page):
    author = models.CharField(max_length=50)
    body = models.TextField()
