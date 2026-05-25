# Test form for practice
from .models import Server
from django.forms import ModelForm


class CreateServer(ModelForm):
    class Meta:
        model = Server
        fields = '__all__'


class GetServer(ModelForm):
    class Meta:
        model = Server
        fields = '__all__'
