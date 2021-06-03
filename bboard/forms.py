from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import modelform_factory
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core import validators
from django import forms
from .models import Bb, Rubric

# RubricFormSet = modelform_factory(Rubric, fields=('name',))
# , can_order=True, can_delete=True

class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара')  # Второй вариант назвать поле
    # title = forms.CharField(label='Название товара',
    #                         validators=[validators.RegexValidator(regex='^.[4,]$')],
    #                         error_messages={'invalid': 'Слишком короткое название товара'})
    # Поверка на короткие названия, но не работает с валидатором названий
    content = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика',
                                    help_text='Не забудьте задать рубрику',
                                    initial=0.0,
                                    widget=forms.widgets.Select(attrs={'size': 8}))  # высота поля

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Укажите не отрицательное значение цены')
        if errors:
            raise ValidationError(errors)

    # def clean_title(self):
    #     val = self.cleaned_data['title']
    #     if val == 'Прошлогодний снег':
    #         raise ValidationError('К продаже не допускается')
    #     return val

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        # labels = {'title': 'Название товара'}  # Второй вариант назвать поле


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

# class BbForm(forms.ModelForm):
#     title = forms.CharField
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'}
#         help_texts = {'rubric': 'Не забудьте выбрать рубрику!'}
#         field_classes = {'price': DecimalField}
#         widgets = {'rubric': Select(attrs={'size': 6})}  # высота поля
#

# # Модель формы первый вариант
# BbForm = modelform_factory(Bb,
#                            fields=('title', 'content', 'price', 'rubric'),
#                            labels={'title': 'Название товара'},
#                            help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
#                            field_classes={'price': DecimalField},
#                            widgets={'rubric':Select(attrs={'size': 6})}  # высота поля
#                            )


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = '__all__'
#     # fields = ('title', 'content', 'price', 'rubric')
