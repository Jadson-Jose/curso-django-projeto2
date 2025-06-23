from collections import defaultdict
from django import forms
from utils.django_forms import add_attr
from recipes.models import Recipe
from django.core.exceptions import ValidationError

from utils.strings import is_positve_number

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.my_errors = defaultdict(list)
        # self.my_errors['bla'].append('legal')
        
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')
    
    
    class Meta:
        model = Recipe
        fields = [
            'title', 
            'description', 
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }
        
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        
            
        if title and description and title == description:
            self.my_errors['title'].append('Cannot be equal to description.')
            self.my_errors['description'].append('Cannot be equal to title.')
            
        if self.my_errors:
            raise ValidationError(self.my_errors)
        
        return super_clean
    
    def clean_field(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            self.my_errors['title'].append('Title must have at least 5 chars.')
        return title
    
    def clean_preparation_tiem(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        if not is_positve_number(field_value):
            self.my_errors[field_name].append('Must be a positive number.')        
        return field_value
    
    