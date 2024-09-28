from django import forms  # Import Django forms module for creating forms
from django.contrib.auth.models import User  # Import User model for user authentication

class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    Inherits from Django's ModelForm to automatically generate fields 
    based on the User model.
    """
    password = forms.CharField(widget=forms.PasswordInput)  # Password field with input type set to password

    class Meta:
        model = User  # Specify the model to create a form for
        fields = ['username', 'email', 'password']  # Specify the fields to include in the form
