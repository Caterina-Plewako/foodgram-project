from taggit.models import Tag

from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientForRecipe


def get_tags(request):
    tags_from_get = []
    if 'tags' in request.GET:
        tags_from_get = request.GET.get('tags')
        _ = tags_from_get.split(',')
        tags_qs = Tag.objects.filter(slug__in=_).values('slug')
    else:
        tags_qs = False
    return [tags_qs, tags_from_get]


def get_ingredients(data):
    ingredient_numbers = set()
    ingredients = []
    for key in data:
        if key.startswith('nameIngredient_'):
            _, number = key.split('_')
            ingredient_numbers.add(number)
    for number in ingredient_numbers:
        ingredients.append(
            {
                'name': data[f'nameIngredient_{number}'],
                'unit': data[f'unitsIngredient_{number}'],
                'amount': float(data[f'valueIngredient_{number}']),
            }
        )
        print(ingredients)
    return ingredients


def save_recipe(recipe, ingredients, request):
    recipe.author = request.user
    recipe.save()
    recipe_ingredients = []

    # for name, amount in ingredients.items():
    #     ingredient = get_object_or_404(Ingredient, name=name)
    #     rec_ingredient = IngredientForRecipe(
    #         amount=amount, ingredient=ingredient, recipe=recipe
    #     )
    #     recipe_ingredients.append(rec_ingredient)

    # IngredientForRecipe.objects.bulk_create(recipe_ingredients)

    for item in ingredients:
        recipe_ing = IngredientForRecipe(
            amount=item.get('amount'),
            ingredient=Ingredient.objects.get(name=item.get('name')),
            recipe=recipe)
        recipe_ing.save()
