from django.shortcuts import render

from .models import Article


def article_search_view(request):
    """
    Render article search view
    @param request:
    @return:
    """

    # Get the input dictionary
    query_dict = request.GET

    # Parse the query dictionary
    try:
        # Search by id
        query = int(query_dict.get("q"))
    except ValueError:
        query = None

    article_obj = None

    if query is not None:
        # Get the article by id
        article_obj = Article.objects.get(id=query)

    context = {
        "object": article_obj
    }

    return render(request, "articles/search.html", context=context)


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
