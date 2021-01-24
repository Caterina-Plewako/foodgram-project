import json
from urllib.parse import unquote

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import Ingredient, Recipe, User

from .models import FavoriteRecipe, Purchase, Subscription


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        if recipe_id is not None:
            obj, created = FavoriteRecipe.objects.get_or_create(
                recipe_id=recipe_id, user=request.user)
            return JsonResponse({'success': created})
        return JsonResponse({'success': False})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FavoriteRecipe, recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({'success': True})


class Subscriptions(LoginRequiredMixin, View):
    def post(self, request):
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, pk=author_id)
        if author != request.user:
            obj, created = Subscription.objects.get_or_create(
                author=author, user=request.user)
            return JsonResponse({'success': created})
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        if author != request.user:
            subscription = get_object_or_404(
                Subscription, author=author_id, user=request.user)
            subscription.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class Purchases(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = Purchase.purchase.get_or_create_purchase(
            user=request.user)

        if not purchase.recipes.filter(id=recipe_id).exists():
            purchase.recipes.add(recipe)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = Purchase.purchase.get(user=request.user)
        if not purchase.recipes.remove(recipe):
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Ingredient.objects.filter(
        name__icontains=query).values('name', 'unit'))
    return JsonResponse(data, safe=False)
