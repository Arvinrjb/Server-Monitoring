# Test form for practice
from .models import Server
from django.forms import ModelForm


class InfServer(ModelForm):
    class Meta:
        model = Server
        fields = '__all__'

