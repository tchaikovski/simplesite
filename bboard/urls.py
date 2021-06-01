from django.urls import path
from .views import index, by_rubric, BbCreateView, add_and_save
# app_name = 'bboard'
urlpatterns = [
    # path('add/save/', add_and_save, name='add_save'),
    # path('add/', add_and_save, name='add'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
]
