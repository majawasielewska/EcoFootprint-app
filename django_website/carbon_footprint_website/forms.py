from django import forms
from .models import UserFootprint


class UserFootprintForm(forms.ModelForm):
    class Meta:
        model = UserFootprint
        fields = ['energy_consumption', 'meat_consumption', 'travel_distance', 'waste_production']

# fields = ['user_name', 'energy_consumption', 'meat_consumption', 'travel_distance', 'waste_production']
