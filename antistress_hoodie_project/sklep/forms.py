from django import forms
from .models import Person, Position

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'surname', 'gender', 'position']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'description']