from rest_framework import serializers
from .models import Recipe, Category



class RecipeSerializer(serializers.ModelSerializer):
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    class Meta:
        model = Recipe
        fields = [
            'id', 
            'title', 
            'description', 
            'public', 
            'preparation',
            'category', 
        ]
        
    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
    
    