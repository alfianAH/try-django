from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm
from .models import Recipe

# Create your views here.

@login_required
def recipe_list_view(request):
    """
    Recipe list view that user write
    """
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list': qs
    }

    return render(request, "recipes/list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    """
    Recipe detail view
    @param: request
    @param: id: Recipe id
    """
    # Use get_object_or_404 if use unique key
    # If not use other method to get object (Example: article_detail_view())
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        'object': obj
    }

    return render(request, "recipes/detail.html", context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid:
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
    
        return redirect(obj.get_absolute_url())

    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_create_view(request, id = None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    context = {
        'object': obj,
        'form': form,
    }

    if form.is_valid:
        form.save()
        context['message'] = 'Data saved.'

    return render(request, "recipes/create-update.html", context)