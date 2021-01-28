from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time',
                  'description', 'image', 'tags']

    def clean(self):
        known_ids = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)

        for id in known_ids:
            value = self.data.get(f'valueIngredient_{id}')

            if float(value) <= 0:
                raise ValidationError(
                    'Пожалуйста, добавьте хотя бы один ингредиент')
