from signal import raise_signal
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, ArticleModelForm
from .models import Article


def article_search_view(request):
    """
    Render article search view
    @param request:
    @return: Render search.html
    """

    # Get the input dictionary
    query_dict = request.GET

    # Parse the query dictionary
    try:
        # Search by id
        query = int(query_dict.get("q"))
    except:
        query = None

    article_obj = None

    if query is not None:
        # Get the article by id
        article_obj = Article.objects.get(id=query)

    context = {
        "object": article_obj
    }

    return render(request, "articles/search.html", context=context)


@login_required
def article_create_view(request):
    """
    Render create article
    @param request: Django's request
    @return: Render create.html
    """

    # Check if there is the request.POST,
    # else it is None, and make the form is not valid
    form = ArticleModelForm(request.POST or None)

    context = {
        "form": form,
    }

    # If the form is valid, ...
    if form.is_valid():
        # Take the form
        article_obj = form.save()

        # Print the form again
        context['form'] = ArticleModelForm()
        # context['object'] = article_obj
        # context['created'] = True

    return render(request, "articles/create.html", context=context)


def article_detail_view(request, slug=None):
    """
    Render article's detail
    @param request: Django's request
    @param slug: Article's slug
    @return: Returns detail.html as a response
    """

    article_obj = None

    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        "object": article_obj
    }

    return render(request, "articles/detail.html", context=context)
