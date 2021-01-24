from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.Favorites.as_view(), name='add_favorites'),
    path('favorites/<int:recipe_id>/',
         views.Favorites.as_view(), name='delete_favorites'),
    path('subscriptions/', views.Subscriptions.as_view(), name='add_subscriprion'),
    path('subscriptions/<int:author_id>/',
         views.Subscriptions.as_view(), name='delete_subscriprion'),
    path('purchases/', views.Purchases.as_view(), name='add_prchases'),
    path('purchases/<int:recipe_id>/',
         views.Purchases.as_view(), name='delete_purchase'),
    path('ingredients/', views.get_ingredients, name='get_ingredients'),
]
