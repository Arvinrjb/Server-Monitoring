from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "email", 
            "first_name", 
            "phone_number", 
            "telegram_id", 
            "last_name", 
            "password1", 
            "password2"
        ]
        