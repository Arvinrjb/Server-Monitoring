# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

# Test form for practice
from .models import Server
from django.forms import ModelForm


class InfServer(ModelForm):
    class Meta:
        model = Server
        fields = '__all__'

