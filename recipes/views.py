from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory  # model form for queryset
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient

# Create your views here.

@login_required
def recipe_list_view(request):
    """
    Recipe list view that user write
    @param: request
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
    """Recipe create view

    Args:
        request (Any): 

    Returns:
        Any: Render for create-update.html
    """
    form = RecipeForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
    
        return redirect(obj.get_absolute_url())

    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_update_view(request, id=None):
    """
    Recipe update view
    @param: request
    @param: id: Recipe's id
    """
    
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    # Make formset for recipe ingredient
    RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
    
    qs = obj.recipeingredient_set.all()
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)

    context = {
        'form': form,
        'formset': formset,
        'object': obj,
    }

    # If all forms are valid
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()

        # Check all ingredient form in formset
        for ingredient_form in formset:
            child = ingredient_form.save(commit=False)
            if not hasattr(child, 'recipe'):
                child.recipe = parent
            child.save()
        
        context['message'] = 'Data saved.'

    return render(request, "recipes/create-update.html", context)