"""
To render HTML web page
"""

import random
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from articles.models import Article


def home_view(request):
    """
    Make home view
    @param request: Django's request
    @return: Returns HTML as a response
    """

    random_id = random.randint(1, 3)
    article_obj = Article.objects.get(id=random_id)
    # Get all objects from database
    article_queryset = Article.objects.all()

    context = {
        "object_list": article_queryset,
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content
    }

    # Django templates
    html_fn = "home-view.html"

    # Another way to render the HTML file
    # template = get_template(html_fn)
    # template_str = template.render(context=context)

    html_string = render_to_string(html_fn, context=context)

    return HttpResponse(html_string)
