import os
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe, Category
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
from django.shortcuts import render


PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def home(request):
    recipes = Recipe.objects.filter(
        is_published=True    
    ).order_by('-id')
    
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })
    
def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category=category,
            is_published=True  
        ).order_by('-id')
    )
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    
    return render(request, 'recipes/pages/category.html', {
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{category.name} - Category | '
    })
    

def recipe(request,id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })
    
def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term),
        ),
        is_published = True
    ).order_by("-id")
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    
    return render(request, 'recipes/pages/search.html', 
                  {'page_title': f'Search for "{search_term}" | ',
                   'search_term': search_term,
                   'recipes': page_obj,
                   'pagination_range': pagination_range,
                   'additional_url_query': f'&q={search_term}',
                   })
