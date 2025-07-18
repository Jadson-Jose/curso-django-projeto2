from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeViwesTest(RecipeTestBase):    
    def test_recipe_home_viewsfunction_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)
        
        
    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertEqual(response.status_code, 200)
        
            
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes here!!',
            response.content.decode('utf-8')
        )
        
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
        
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        reponse_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(reponse_context_recipes), 1)
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Teste recipe is published False dont show"""
        
        # Need a recipe for the test
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        
        # Check if one recipe exists
        self.assertIn(
            'No recipes here!!',
            response.content.decode('utf-8')
        )
        
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 500000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 500000})
        )
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for the test
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        # Check if one recipe exists
        self.assertIn(needed_title, content)
        
    def test_recipe_category_template_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id})
        )
        
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_detail_view_function_is_correcta(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)
        
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 500000})
        )
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        
        # Need a recipe for the test
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        
        # Check if one recipe exists
        self.assertIn(needed_title, content)
        
    def test_recipe_detail_template_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': recipe.category.id
                }
            )
        )
        
        self.assertEqual(response.status_code, 404)
        