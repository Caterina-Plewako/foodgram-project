import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from taggit.models import Tag
from .models import Recipe, User, FavoriteRecipes
from .forms import RecipeForm


def index(request):
    recipes = Recipe.objects.all()
    tags_from_get = []
    if 'tags' in request.GET:
        tags_from_get = request.GET.get('tags')
        _ = tags_from_get.split(',')
        tags_qs = Tag.objects.filter(slug__in=_).values('slug')
    else:
        tags_qs = False
    if tags_qs:
        recipes = Recipe.objects.filter(tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, 1)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/index.html',
        {'recipes': recipes, 'paginator': paginator,
         'page': page, 'tags': tags_from_get}
    )


def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'recipes/formRecipe.html', {'form': form})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author=author, id=recipe_id)
    ingredients = recipe.recipeingredient.all()
    return render(request, 'recipes/singlePageNotAuth.html', {'author': author, 'recipe': recipe, 
                                                              'ingredients': ingredients})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.all()
    # recipes_number = recipes.count()
    # paginator = Paginator(posts, 10)

    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)
    return render(request, 'recipes/authorRecipe.html', {'author': author, 'recipes': recipes})


def follow_index(request):
    recipe_list = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(recipe_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/myFollow.html', {'page': page, 'paginator': paginator})


def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author).exists()
    if author != request.user:
        if not follow:
            Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author)
    if author != request.user:
        if follow.exists():
            follow.delete()
    return redirect('profile', username=username)

@csrf_exempt
@require_http_methods(['POST'])
def add_favorites(request):
    recipe_id = json.loads(request.body).get('id')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    obj, created = FavoriteRecipes.objects.get_or_create(
        user=request.user, recipe=recipe
    )
    if not created:
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    removed = FavoriteRecipes.objects.filter(
        user=request.user, recipe=recipe
    ).delete
    if removed:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
