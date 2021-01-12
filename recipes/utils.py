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


def get_ingredients_from_form(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(
                request.POST[f'valueIngredient_{_[1]}']
            )
    return ingredients
