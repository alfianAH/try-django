from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Meal

# Create your views here.
@login_required
def meal_queue_toggle_view(request, recipe_id=None):
    user = request.user
    user_id = None

    if user.is_authenticated:
        user_id = user.id
    
    is_pending = Meal.objects.by_user_id(user_id).in_queue(recipe_id)
    toggle_label = 'Add to meals' if not is_pending else 'Remove from meals'

    context = {
        'recipe_id': recipe_id,
        'toggle_label': toggle_label,
        'is_pending': is_pending
    }

    return render(request, 'meals/partials/queue-toggle.html', context)