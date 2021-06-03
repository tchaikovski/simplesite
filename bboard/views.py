from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
# StreamingHttpResponse
# from django.template import loader
from django.views.generic.dates import ArchiveIndexView
from django.template.response import TemplateResponse
# from django.template.loader import get_template, render_to_string
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
# from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.views.decorators.gzip import gzip_page
from .forms import BbFrom
from .models import Bb, Rubric


class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwargs = 'rubric_id'

    # Добавляем запись
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    def get_queryset(self):
        return self.object.bb_set.all()

    # Конец записи а нижний код закоменчен
    # context_object_name = 'bbs'

    # def get_queryset(self):
    #     return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
    #     context['rubrics'] = Rubric.objects.all()
    #     context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
    #     return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = super(BbDetailView, self).get_context_data()
        context['rubrics'] = Rubric.objects.all()
        return context


class BbAddView(FormView):
    template_name = 'bboard/create_add.html'
    form_class = BbFrom
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbEditView(UpdateView):
    model = Bb
    form_class = BbFrom
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# Форма создания объявления
class BbCreateView(CreateView):
    template_name = 'bboard/create.html'  # путь шаблона
    form_class = BbFrom  # ссылка на модель формы
    success_url = reverse_lazy('index')  # перенаправление после создания объявления

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# # Вывод главной страницы
# @gzip_page
# def index(request):
#     rubrics = Rubric.objects.all()
#     bbs = Bb.objects.all()
#
#     paginator = Paginator(bbs, 2)
#     if 'page' in request.GET:
#         page_num = request.GET['page']
#     else:
#         page_num = 1
#     page = paginator.get_page(page_num)
#     context = {'bbs': bbs, 'page': page, 'rubrics': rubrics}
#     # template = get_template('bboard/index.html')
#     return TemplateResponse(request, 'bboard/index.html', context=context)
#
#     # return render(request, '/bboard/index.html', context)


def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
    return render(request, 'bboard/index.html', context)

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
#
#
# def add_and_save(request):
#     if request.method == 'POST':
#         bbf = BbFrom(request.POST)
#         if bbf.is_valid():
#             bbf.save()
#             return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
#         else:
#             context = {'form': bbf}
#             return render(request, 'bboard/create_add.html', context)
#     else:
#         bbf = BbFrom()
#         context = {'form': bbf}
#         return render(request, 'bboard/create_add.html', context)

#
# Функция обработки категорий
@gzip_page  # сжатие страницы
def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


# Низкоуровневый ответ
# def index(request):
#     resp = HttpResponse("Здесь будет", content_type='text/plain; charset=utf-8')
#     resp.write(' главная')
#     resp.writelines((' страница', ' сайта'))
#     resp['keywords'] = 'Python, Django'
#     return resp

# def detail(request, bb_id):
#     try:
#         bb = Bb.objects.get(pk=bb_id)
#     except Bb.DoesNotExist:
#         raise Http404('Такое объявление не существует')
#     return HttpResponse(...)
