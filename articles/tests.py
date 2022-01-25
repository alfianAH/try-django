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
        self.number_of_articles = 500
        for i in range(self.number_of_articles):
            Article.objects.create(title='Hello world', content='something')
    

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
        """
        Test slugify instance title uniqueness
        """
        # Get the last article
        obj = Article.objects.all().last()
        new_slugs = []

        # Slugify the last article for 25 times
        for i in range(0, 25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)

        # Remove the same slug by make it to set
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    
    def test_slugify_instance_title_redux(self):
        """
        Test slugify instance title uniqueness
        """
        # Get slug list
        slug_list = Article.objects.all().values_list('slug', flat=True)
        # Remove the same slug by make it to set
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))

    
    def test_article_search_manager(self):
        """
        Test Search manager by title and content
        """
        # Search by title
        qs = Article.objects.search('hello world')
        self.assertEqual(qs.count(), self.number_of_articles)

        # Search by some words of title
        qs = Article.objects.search('hello')
        self.assertEqual(qs.count(), self.number_of_articles)
        
        # Search by content
        qs = Article.objects.search('something')
        self.assertEqual(qs.count(), self.number_of_articles)