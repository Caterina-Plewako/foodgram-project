import pymorphy2
from django import template
from api.models import Purchase

register = template.Library()

morph = pymorphy2.MorphAnalyzer()


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


@register.filter(name='plural_recipes')
def plural_recipe(number):
    word = morph.parse('рецепт')[0]
    return word.make_agree_with_number(number).word


@register.filter(name='purchase_list')
def purchase_list(user_id):
    return Purchase.purchase.get_purchases_list(user_id)