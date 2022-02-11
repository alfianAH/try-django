from django.urls import path

from.views import (
    recipe_create_view,
    recipe_list_view,
    recipe_update_view,
    recipe_delete_view,
    recipe_detail_view,
    recipe_detail_hx_view,
    recipe_ingredient_update_hx_view,
    recipe_ingredient_delete_view,
    recipe_ingredient_image_upload_view
)

app_name = 'recipes'
urlpatterns = [
    path('', recipe_list_view, name='list'),
    # Create recipe
    path('create/', recipe_create_view, name='create'),
    # Update ingredient
    path('hx/<int:parent_id>/ingredient/<int:id>', recipe_ingredient_update_hx_view, name='hx-ingredient-update'),
    # Create ingredient
    path('hx/<int:parent_id>/ingredient/', recipe_ingredient_update_hx_view, name='hx-ingredient-create'),
    # Recipe detail
    path('hx/<int:id>/', recipe_detail_hx_view, name='hx-detail'),
    # Ingredient delete
    path('<int:parent_id>/ingredient/<int:id>/delete/', recipe_ingredient_delete_view, name='ingredient-delete'),
    # Ingredient image
    path('<int:parent_id>/image-upload/', recipe_ingredient_image_upload_view, name='ingredient-image-upload'),
    # Recipe delete
    path('<int:id>/delete/', recipe_delete_view, name='delete'),
    # Recipe update
    path('<int:id>/edit/', recipe_update_view, name='edit'),
    # Recipe detail
    path('<int:id>/', recipe_detail_view, name='detail'),
]