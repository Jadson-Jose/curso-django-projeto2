from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase

 
class RecipeCategoryViewTest(RecipeTestBase):
      
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)
        
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        test_category = self.make_category(name='Test Category')
        self.make_recipe(
            category=test_category,
            is_published=False
        )
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': test_category.id})
        )
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        test_category = self.make_category(name='Empty Category')
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': test_category.id})
        )
        self.assertEqual(response.status_code, 404)
        
