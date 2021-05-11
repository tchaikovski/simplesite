from django.forms import ModelForm

from .models import Bb


class BbFrom(ModelForm):
    model = Bb
    fields = ('title', 'content', 'price', 'rubric')
