"""
To render HTML web page
"""

from django.http import HttpResponse
from random import randint

from articles.models import Article


def home_view(request):
    """
    Make home view
    @param request: Django's request
    @return: Returns HTML as a response
    """

    random_id = randint(1, 3)
    article_obj = Article.objects.get(id=2)

    h1_string = """
    <h1>{}</h1>
    """.format(article_obj.title)

    p_string = """
    <p>{}</p>
    """.format(article_obj.title)

    html_string = h1_string + p_string

    return HttpResponse(html_string)
