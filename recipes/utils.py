from taggit.models import Tag


def get_tags(request):
    tags_from_get = []
    if 'tags' in request.GET:
        tags_from_get = request.GET.get('tags')
        _ = tags_from_get.split(',')
        tags_qs = Tag.objects.filter(slug__in=_).values('slug')
    else:
        tags_qs = False
    return [tags_qs, tags_from_get]


def get_ingredients_from_form(data):
    ingredients = {}

    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = request.POST[
                f'valueIngredient_{_[1]}'
            ]

    return ingredients


def save_recipe(ingredients, recipe):
    recipe_ingredients = []

    for title, value in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        rec_ingredient = IngredientValue(
            value=value, ingredient=ingredient, recipe=recipe
        )
        recipe_ingredients.append(rec_ingredient)

    IngredientValue.objects.bulk_create(recipe_ingredients)
