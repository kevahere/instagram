from django import forms
from .models import Profile, Image, Comments

class UpfateProfile(forms.ModelForm):
    """Enables the user to update their bio and profile pic"""
    class Meta:
        model =Profile
        exclude = ['user']