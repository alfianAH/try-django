from django.shortcuts import render

from .models import Article


def article_detail_view(request, id=None):
    """
    Render article's detail
    @param request: Django's request
    @param id: Article's ID
    @return: Returns detail.html as a response
    """

    article_obj = None

    if id is not None:
        article_obj = Article.objects.get(id=id)

    context = {
        "object": article_obj
    }

    return render(request, "articles/detail.html", context=context)
