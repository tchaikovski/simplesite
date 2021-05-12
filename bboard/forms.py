from django.forms import ModelForm

from .models import Bb


class BbFrom(ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
    # fields = ('title', 'content', 'price', 'rubric')
