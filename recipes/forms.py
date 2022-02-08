from django import forms
from .models import Recipe, RecipeIngredient, RecipeIngredientImage


class RecipeForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholder and class in form (CSS)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({
                'placeholder': 'Recipe {}'.format(str(field)),
                'class': 'form-control'
            })

        self.fields['name'].help_text = 'This is your help <a href="/contact">Contact us</a>'

        self.fields['description'].widget.attrs.update({
            'rows': 2,
        })

        self.fields['directions'].widget.attrs.update({
            'rows': 3,
        })


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']


class RecipeIngredientImageForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredientImage
        fields = ['image']
