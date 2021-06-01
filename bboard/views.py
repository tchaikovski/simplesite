from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.template.loader import get_template, render_to_string
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.gzip import gzip_page
from .forms import BbFrom
from .models import Bb, Rubric


class BbByRubricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = super(BbDetailView, self).get_context_data()
        context['rubrics'] = Rubric.objects.all()
        return context


# Функция добавления объявления
# def add(request):
#     bbf = BbFrom()
#     context = {'form': bbf}
#     return render(request, 'bboard/create_add.html', context)
#

# def add_save(request):
#     bbf = BbFrom(request.POST)
#     if bbf.is_valid():
#         bbf.save()
#         return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
#     else:
#         context = {'form': bbf}
#         return render(request, 'bboard/create_add.html', context)


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbFrom(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create_add.html', context)
    else:
        bbf = BbFrom()
        context = {'form': bbf}
        return render(request, 'bboard/create_add.html', context)


# Форма создания объявления
class BbCreateView(CreateView):
    template_name = 'bboard/create.html'  # путь шаблона
    form_class = BbFrom  # ссылка на модель формы
    success_url = reverse_lazy('index')  # перенаправление после создания объявления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# Функция обработки категорий
@gzip_page  # сжатие страницы
def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


# Вывод главной страницы
@gzip_page
def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    # template = get_template('bboard/index.html')
    return TemplateResponse(request, 'bboard/index.html', context=context)

    # return render(request, '/bboard/index.html', context)


# Низкоуровневый ответ
# def index(request):
#     resp = HttpResponse("Здесь будет", content_type='text/plain; charset=utf-8')
#     resp.write(' главная')
#     resp.writelines((' страница', ' сайта'))
#     resp['keywords'] = 'Python, Django'
#     return resp

def detail(request, bb_id):
    try:
        bb = Bb.objects.get(pk=bb_id)
    except Bb.DoesNotExist:
        raise Http404('Такое объявление не существует')
    return HttpResponse(...)
