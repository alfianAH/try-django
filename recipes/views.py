from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory  # model form for queryset
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse
from django.urls import reverse
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientImageForm
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
    hx_url = reverse('recipes:hx-detail', kwargs={'id': id})
    context = {
        'hx_url': hx_url
    }

    return render(request, "recipes/detail.html", context)


@login_required
def recipe_delete_view(request, id=None):
    """
    Recipe delete view
    @param: request
    @param: id: Recipe id
    """
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    
    if obj is None:
        if request.htmx:
            return HttpResponse("Not found")
        raise Http404

    if request.method == 'POST':
        obj.delete()
        success_url = reverse('recipes:list')

        if request.htmx:
            headers = {
                'hx-redirect': success_url
            }

            return HttpResponse("Success", headers=headers)

        return redirect(success_url)
    
    context = {
        'object': obj
    }

    return render(request, "recipes/delete.html", context)


@login_required
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    """
    Recipe ingredient delete view
    @param: request
    @param: parent_id: Recipe id
    @param: id: Recipe Ingredient id
    """
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id, id=id, recipe__user=request.user)
    except:
        obj = None
    
    if obj is None:
        if request.htmx:
            return HttpResponse("Not found")
        raise Http404

    if request.method == 'POST':
        name = obj.name
        obj.delete()
        success_url = reverse('recipes:detail', kwargs={'id': parent_id})

        if request.htmx:
            return render(request, "recipes/partials/ingredient-inline-delete-response.html", {
                'name': name
            })

        return redirect(success_url)
    
    context = {
        'object': obj
    }

    return render(request, "recipes/delete.html", context)


@login_required
def recipe_detail_hx_view(request, id=None):
    """
    Recipe detail view
    @param: request
    @param: id: Recipe id
    """

    # If user inputs '/hx/' (for HTMX) in url, give 404
    if not request.htmx:
        raise Http404
    
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None

    if obj is None:
        return HttpResponse('Not found')

    new_ingredient_url = reverse('recipes:hx-ingredient-create', kwargs={'parent_id': obj.id})
    
    context = {
        'object': obj,
        'new_ingredient_url': new_ingredient_url
    }

    return render(request, "recipes/partials/detail.html", context)


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

        # If request is HTMX, redirect it to absolute URL via hx-redirect
        if request.htmx:
            headers = {
                'hx-redirect': obj.get_absolute_url()
            }
            return HttpResponse('Created', headers=headers)
        
        # Normal redirect
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
    new_ingredient_url = reverse('recipes:hx-ingredient-create', kwargs={'parent_id': obj.id})

    context = {
        'form': form,
        'object': obj,
        'new_ingredient_url': new_ingredient_url
    }
    
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'

    if request.htmx:
        return render(request, 'recipes/partials/forms.html', context)
    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    """
    Recipe ingredient detail view
    @param: request
    @param: id: Recipe id
    """

    # If user inputs '/hx/' (for HTMX) in url, give 404
    if not request.htmx:
        raise Http404
    
    # Get the recipe
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse('Not found')
    
    # Get the recipe ingredient
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None

    # Create new ingredient
    url = parent_obj.get_create_ingredient_hx_url()

    # If user wants to edit ingredient (If there is an instance), ..
    if instance:
        url = instance.get_hx_edit_url()
    
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    
    context = {
        'url': url,
        'object': instance,
        'form': form,
    }

    # If form is valid, save the obj and render the line again
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "recipes/partials/ingredient-inline.html", context)

    # Render form
    return render(request, "recipes/partials/ingredient-form.html", context)


@login_required
def recipe_ingredient_image_upload_view(request, parent_id=None):
    """Recipe ingredient image upload view

    Args:
        request (): 
        parent_id (int, optional): Recipe's id. Defaults to None.

    Raises:
        Http404: 404 page

    Returns:
        any: Render image-form.html
    """
    template_name = 'recipes/image-upload.html'

    if request.htmx:
        template_name = 'recipes/partials/image-upload-form.html'

    # Get the recipe
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    
    if parent_obj is None:
        raise Http404

    form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        obj.save()

        success_url = parent_obj.get_edit_url()
        if request.htmx:
            headers = {
                'hx-redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    
    context = {
        'form': form
    }
    return render(request, template_name, context)