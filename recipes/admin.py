from django.contrib import admin

from .models import Recipe, RecipeIngredient

# Register your models here.
class RecipeIngredientInline(admin.StackedInline):
    """
    Admin view for recipe ingredient
    """

    model = RecipeIngredient
    readonly_fields = ['quantity_as_float']
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """
    Admin view for recipe
    """
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']
    inlines = [RecipeIngredientInline]


admin.site.register(Recipe, RecipeAdmin)