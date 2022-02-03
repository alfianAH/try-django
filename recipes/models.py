import pint
from django.urls import reverse
from django.db import models
from django.conf import settings

from .utils import number_str_to_float
from.validators import validate_unit_of_measure

# Create your models here.

"""
- Global
    - Ingredients
    - Recipes
- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients
"""

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id': self.id})

    def get_absolute_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={'id': self.id})

    def get_edit_url(self):
        return reverse('recipes:edit', kwargs={'id': self.id})

    def get_ingredients(self):
        return self.recipeingredient_set.all()

    def get_create_ingredient_hx_url(self):
        return reverse('recipes:hx-ingredient-create', kwargs={'parent_id': self.id})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=10)
    quantity_as_float = models.FloatField(blank=True, null=True)
    # pounds, lbs, gram
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure])
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def get_hx_edit_url(self):
        return reverse('recipes:hx-ingredient-update', kwargs={
            'parent_id': self.recipe.id,
            'id': self.id
        })

    def convert_to_system(self, system='mks'):
        """
        Convert system in pint for measurement and combine the quantity and the unit
        """
        # Return directly if quantity as float is none
        if self.quantity_as_float is None:
            return None
        
        ureg = pint.UnitRegistry(system=system)
        # Combine the quantity and the unit
        measurement  = self.quantity_as_float * ureg[self.unit]

        return measurement


    def as_mks(self):
        """
        In mks => meter, kilogram, second
        """
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()


    def as_imperial(self):
        """
        In imperial => miles, pounds, seconds
        """
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()


    def save(self, *args, **kwargs):
        # Change quantity from string to float
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None

        super().save(*args, **kwargs)