from urllib import request
from django.http.response import Http404
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.templates.authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required



class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
        ).first()

        if not recipe:
            raise Http404()

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return render(request, 'authors/pages/dashboard_recipe.html', { 'form': form })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Salvo com sucesso!')
        return redirect(
            reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
        )

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form,
            'form_action': reverse('authors:dashboard_recipe_new')
        }
    )
