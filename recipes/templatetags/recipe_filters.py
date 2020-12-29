from django import template
from ..models import FavoriteRecipes

register = template.Library()

@register.filter(name='is_favorite')
def is_favorite(recipe_id, user_id):
    return FavoriteRecipes.objects.filter(
        user_id=user_id, recipe_id=recipe_id).exists()


@register.filter
def formatting_tags(request, tag):
    if 'tags' in request.GET:

        tags = request.GET.get('tags')
        tags = tags.split(',')  

        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
        if '' in tags:
            tags.remove('')

        result = ','.join(tags)
        return result

    return tag