from django import template

from ..models import FavoriteRecipe, Subscription

register = template.Library()


@register.filter
def is_favorite(recipe_id, user_id):
    return FavoriteRecipe.objects.filter(
        user_id=user_id, recipe_id=recipe_id).exists()


@register.filter
def is_subscribed(author, user_id):
    return Subscription.objects.filter(
        user=user_id, author=author).exists()
