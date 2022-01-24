from django.utils.text import slugify
import random


def slugify_instance_title(instance, save=False, new_slug=None):
    """
    Slugify title
    """
    
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    # Query the slug
    Klass = instance.__class__  # Get the class
    query = Klass.objects.filter(slug=slug).exclude(id=instance.id)

    if query.exists():
        # Randomize int to prevent bad slug
        random_int = random.randint(100_000, 25_000_000)
        # Auto generate new slug
        slug = '{}-{}'.format(slug, random_int)

        # Recursion until there is no query
        return slugify_instance_title(instance, save=save, new_slug=slug)

    instance.slug = slug  # Set the slug

    if save: 
        instance.save()
    return instance