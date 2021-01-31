from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from taggit.models import Tag

from api.models import Purchase, Subscription
from foodgram.settings import ITEMS_FOR_PAGINATOR

from .forms import RecipeForm
from .models import IngredientForRecipe, Recipe, User
from .utils import get_tags, save_recipe, get_ingredients


def index(request):
    recipes = Recipe.objects.all()
    tags_qs, tags_from_get = get_tags(request)

    if tags_qs:
        recipes = Recipe.objects.filter(tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/index.html',
        {'recipes': recipes, 'paginator': paginator,
         'page': page, 'tags': tags_from_get}
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    tags = Tag.objects.all()

    if form.is_valid():
        recipe = form.save(commit=False)
        ingredients = get_ingredients(request.POST)
        save_recipe(recipe, ingredients, request)
        form.save_m2m()
        return redirect('index')
    return render(request, 'recipes/formRecipe.html', {'form': form, 'tags': tags})


@login_required
def recipe_edit(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    ing = IngredientForRecipe.objects.filter(recipe=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    tags = Tag.objects.all()
    context = {'form': form, 'recipe': recipe,
               'ingredients': ing, 'tags': tags}

    if recipe.author == request.user:
        ingredients = get_ingredients(request.POST)

        if form.is_valid():
            ing.delete()
            recipe = form.save(commit=False)
            save_recipe(recipe, ingredients, request)
            form.save_m2m()
            return redirect('recipe', username=request.user.username,
                            recipe_id=recipe.id)

        return render(request, 'recipes/formRecipe.html', context)
    else:
        return redirect('recipe', username=request.user.username,
                        recipe_id=recipe.id)


@login_required
def recipe_delete(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)

    if request.user != recipe.author:
        return redirect(
            'recipe_view',
            username=username,
            recipe_id=recipe_id
        )

    recipe.delete()
    return redirect('index')


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    ingredients = recipe.recipeingredient.all()
    return render(request, 'recipes/recipe_view.html', {'recipe': recipe,
                                                        'ingredients': ingredients})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)
    tags_qs, tags_from_get = get_tags(request)

    if tags_qs:
        recipes = Recipe.objects.filter(
            author=author,
            tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html',
                  {'author': author, 'page': page,
                   'paginator': paginator, 'tags': tags_from_get}
                  )


@login_required
def subscriptions(request, username):
    user = get_object_or_404(User, username=username)
    subscriptions = User.objects.prefetch_related('recipes').filter(
        following__user=user.id)
    paginator = Paginator(subscriptions, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/myFollow.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def favorites(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(favourites__user=request.user)
    tags_qs, tags_from_get = get_tags(request)

    if tags_qs:
        recipes = Recipe.objects.filter(favourites__user=request.user,
                                        tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html', {
        'recipes': recipes, 'paginator': paginator, 'page': page,
        'username': user, 'tags': tags_from_get
    })


@login_required
def purchases_list(request):
    recipes_list = Purchase.purchase.get_purchases_list(request.user)
    return render(request,
                  'recipes/shopList.html',
                  {'recipes_list': recipes_list}
                  )


@login_required
def download_shoplist(request):
    user = request.user
    filename = f'{user.username}_list.txt'
    recipes = Purchase.purchase.get_purchases_list(user).values(
        'ingredients__name', 'ingredients__unit'
    )
    ingredients = recipes.annotate(Sum('recipeingredient__amount')).order_by()
    products = [
        (f'{i["ingredients__name"]} -'
         f' {i["recipeingredient__amount__sum"]} {i["ingredients__unit"]}')
        for i in ingredients]
    content = '\n'.join(products)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
