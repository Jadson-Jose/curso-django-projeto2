from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
from django.contrib.auth.models import User



        
class RecipeSearchViewTest(RecipeTestBase):
          
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
 
    def test_recipe_search_loads_correct_template(self):
        reponse = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(reponse, 'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn('Search for &quot;Teste&quot;', response.content.decode('utf-8'))
        
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is a recipe one'
        title2 = 'This is a recipe two'
        
        user1 = User.objects.create_user(username='one')
        user2 = User.objects.create_user(username='two')
        
        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author=user1
        )
        
        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author=user2
        )
        
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')
        
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
        
        