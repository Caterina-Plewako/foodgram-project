from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('purchases_index/', views.purchases_list, name='purchases_list'),
    path('download_txt/',
         views.download_shoplist, name='download_shoplist'),
    path('<str:username>/<int:recipe_id>/edit/',
         views.recipe_edit, name='recipe_edit'),
    path('<str:username>/<int:recipe_id>/delete/',
         views.recipe_delete, name='recipe_delete'),
    path('subscriptions/<str:username>/',
         views.subscriptions, name='subscriptions'),
    path('favorites/<str:username>/', views.favorites, name='favorites'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
]
