from django import forms
from .models import Hall

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'capacity', 'location', 'description', 'amenities', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
        }
