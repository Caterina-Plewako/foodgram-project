import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients data to database'

    def handle(self, *args, **options):
        with open('recipes/ingredients_data/ingredients.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(name=name, unit=unit)
