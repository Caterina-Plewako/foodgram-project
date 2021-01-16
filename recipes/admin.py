from django.contrib import admin

from .models import Ingredient, IngredientForRecipe, Recipe


class IngredientForRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientForRecipeInLine,)


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientForRecipe)
