from turtle import title
from django.test import TestCase
from django.utils.text import slugify
from .models import Article
from .utils import slugify_instance_title

# Create your tests here.
class ArticleTestCase(TestCase):
    def setUp(self):
        """
        Setup article database for testing
        """
        self.number_of_articles = 5
        for i in range(self.number_of_articles):
            Article.objects.create(title='Hello world', content='Hello')
    

    def test_queryset_exists(self):
        """
        Test if article query exists
        """
        qs = Article.objects.all()
        self.assertTrue(qs.exists())
    

    def test_queryset_count(self):
        """
        Test if the number of current articles is the same as created one
        """
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    
    def test_hello_world_slug(self):
        """
        Test if slugified title of the first Article object is the same as it should be
        """
        # Get first article
        obj = Article.objects.all().order_by('id').first()
        slugified_title = slugify(obj.title)
        self.assertEqual(obj.slug, slugified_title)


    def test_hello_world_unique_slug(self):
        """
        Test if the remaining titles of the rest Article object is not the same as its title
        Because there is already the first one that take that slug
        """
        # Exclude first article
        qs = Article.objects.exclude(slug__iexact='hello-world')
        
        for obj in qs:
            slugified_title = slugify(obj.title)
            self.assertNotEqual(obj.slug, slugified_title)

    
    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []

        for i in range(0, 5):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)

        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))