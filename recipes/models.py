from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=246)
    unit = models.CharField(max_length=56)

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Recipe(models.Model):
    title = models.CharField(max_length=477, blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientForRecipe', blank=False, related_name='recipes')
    description = models.TextField(blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    cooking_time = models.PositiveIntegerField(blank=False)
    slug = models.SlugField(max_length=50, blank=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=False)
    tags = TaggableManager()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class IngredientForRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipeingredient')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipeingredient')
    amount = models.CharField(max_length=20)

    def __str__(self):
        return str(self.ingredient) if self.ingredient else ''
