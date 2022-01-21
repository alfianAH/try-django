from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import slugify_instance_title


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True, null=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance)


def article_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    if created:
        slugify_instance_title(instance, save=True)


pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)