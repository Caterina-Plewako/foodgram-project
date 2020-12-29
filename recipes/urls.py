from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.index, name='index_by_tag'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorites', views.add_favorites, name='add_favorites'),
    path('favorites/<int:id>/', views.delete_favorites, name='delete_favorites'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('<str:username>/unfollow/',
         views.profile_unfollow, name='profile_unfollow'),
]