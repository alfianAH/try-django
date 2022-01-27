from unicodedata import name
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Recipe, RecipeIngredient
from .validators import validate_unit_of_measure

# Create your tests here.
User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('alfian', password='abc12345')


    def test_user_pw(self):
        """
        Check user's password
        """
        self.assertTrue(self.user_a.check_password('abc12345'))


class RecipeTestCase(TestCase):
    def setUp(self):
        """
        Set up case
        - User A
            - Recipe A: Ayam geprek
                - Ingredient A: Ayam
            - Recipe B: Bebek Kerenyes
                - Ingredient B: Bebek
        """
        self.user_a = User.objects.create_user('alfian', password='abc12345')
        self.recipe_a = Recipe.objects.create(
            name='Ayam Geprek',
            user=self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name='Bebek Krenyes',
            user=self.user_a
        )

        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Ayam',
            quantity='1/2',
            unit='kg'
        )

        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_b,
            name='Bebek',
            quantity='adaa',
            unit='kg'
        )

    
    def test_user_count(self):
        """
        Check user account from database
        Expected value: 1 (User A)
        """
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)


    def test_user_recipe_reverse_count(self):
        """
        Check user's recipes via user
        Expected value: 2 (Recipe A & B)
        """
        user = self.user_a
        qs = user.recipe_set.all()

        self.assertEqual(qs.count(), 2)


    def test_user_recipe_forward_count(self):
        """
        Check user's recipes via recipe database
        Expected value: 2 (Recipe A & B)
        """
        user = self.user_a
        qs = Recipe.objects.filter(user=user)

        self.assertEqual(qs.count(), 2)


    def test_recipe_ingredient_reverse_count(self):
        """
        Check recipe ingredient via recipe A
        Expected value: 1 (Ingredient A)
        """
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(), 1)

    
    def test_recipe_ingredient_forward_count(self):
        """
        Check recipe ingredient via recipe A database
        Expected value: 1 (Ingredient A)
        """
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 1)

    
    def test_user_two_level_relation(self):
        """
        Check recipe ingredient via ingredient's database
        Expected value: 2 (Ingredient A & B)
        RecipeIngredient > recipe > user
        """
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)


    def test_user_two_level_relation_reverse(self):
        """
        Check recipe ingredient via ingredient
        Expected value: 2 (Ingredient A & B)
        ids = recipe > recipe ingredient > id
        qs = recipe ingredient > id
        """
        user = self.user_a
        # Get query sets of recipe ingredients' id
        recipe_ingreedient_ids = list(user.recipe_set.all().values_list('recipeingredient__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=recipe_ingreedient_ids)
        self.assertEqual(qs.count(), 2)

    
    def test_user_two_level_relation_reverse_via_recipe(self):
        """
        Check recipe ingredient via recipe
        Expected value: 2 (Ingredient A & B)
        ids = recipe > id
        qs = recipe ingredient > recipe > id 
        """
        user = self.user_a
        # Get query sets of recipe's id
        ids = list(user.recipe_set.all().values_list('id', flat=True))
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)

    
    def test_unit_measure_validation_invalid(self):
        """
        Test unit measure validation for invalid input
        Expected value: Raise Validation Error
        """
        invalid_units = ['adfad', 'adfadf']

        # Check if it raises validation error
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredient(
                    name='Bebek', quantity='1/2', unit=unit,
                    recipe=self.recipe_b
                )

                ingredient.full_clean()

    def test_unit_measure_validation_valid(self):
        """
        Test unit measure validation for valid input
        Expected value: Success
        """
        valid_unit = 'kg'

        ingredient = RecipeIngredient(
            name='Bebek', quantity='1/2', unit=valid_unit,
            recipe=self.recipe_b
        )

        ingredient.full_clean()

    
    def test_quantity_as_float(self):
        """
        Test quantity as float is none or not
        Expected value: Ingredient A (valid): not none
            Ingredient B (invalid): none
        """
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)