# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

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
        