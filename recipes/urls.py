from django.urls import path
from .views import site
from .views import api

app_name = 'recipes'

urlpatterns = [
    path('', site.home, name="home"),
    path('recipes/search/', site.search, name="search"),
    path('recipes/category/<int:category_id>/', site.category, name="category"),
    path('recipes/<int:id>/', site.recipe, name="recipe"),
    path('recipes/api/v2/', api.recipe_api_list, name='recipe_api_v2'),
    path(
        'recipes/api/v2/<int:pk>/', 
        api.recipe_api_detail, 
        name='recipe_api_v2_detail'
    ),
]