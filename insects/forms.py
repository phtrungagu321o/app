from django import forms
from . import models



class CreateImageForm(forms.ModelForm):
    class Meta:
        model = models.Insect_Image
        fields = ['image']
