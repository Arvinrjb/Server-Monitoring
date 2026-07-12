# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True
    )
    bio = models.TextField(
        max_length=100,
        blank=True
    )
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True
    )
    telegram_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        permissions = [
            (
                "view_all_users",
                "Can view all users"
            ),
            (
                "manage_users",
                "Can manage users"
            )
        ]