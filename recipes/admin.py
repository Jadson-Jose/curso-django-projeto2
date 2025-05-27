from django.contrib import admin

from recipes.models import Category, Recipe

class CategoryAdmin(admin.ModelAdmin):
    ...
    

@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    ...    

admin.site.register(Category, CategoryAdmin)
