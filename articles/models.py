from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from .utils import slugify_instance_title
# from meals.utils import generate_meal_queue_totals


User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    """
    Custom query set class
    """

    def search(self, query=None):
        # Return if query is none or empty
        if query is None or query == '':
            return self.none()
        
        # Search by title and content
        lookups = Q(title__icontains=query) | Q(content__icontains=query)

        return self.filter(lookups)


class ArticleManager(models.Manager):
    """
    Article model manager
    """
    
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)


# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True, null=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = ArticleManager()

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)


# def meal_added_receiver(sender, instance, *args, **kwargs):
#     print('Added', args, kwargs)
#     user = instance.user
#     data = generate_meal_queue_totals(user)
#     print(data)

# def meal_removed_receiver(*args, **kwargs):
#     print('Removed', args, kwargs)


# meal_added.connect(meal_added_receiver)
# meal_removed.connect(meal_removed_receiver)