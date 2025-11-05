from django import forms
from .models import *

class CustomForm(forms.Form):
    message = forms.CharField()
    subject = forms.CharField()


class BMIForm(forms.Form):
    height_in_inches = forms.FloatField(label='Height (in inches)')
    weight_in_kg = forms.FloatField(label='Weight (in kgs)')