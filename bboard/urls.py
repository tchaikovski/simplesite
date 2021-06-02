from django.urls import path
from .views import index, by_rubric, BbCreateView, BbDetailView, BbAddView, BbEditView, BbDeleteView, BbIndexView
# from .views import index, BbCreateView,  BbDetailView, BbAddView, BbEditView, BbDeleteView, BbIndexView

# app_name = 'bboard'
urlpatterns = [
    # path('add/save/', add_and_save, name='add_save'),
    # path('add/', add_and_save, name='add'),
    path('', index, name='index'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/edit/', BbEditView.as_view(), name='edit'),
    path('detail/<int:pk>/delete/', BbDeleteView.as_view(), name='delete'),
    path('add/', BbAddView.as_view(), name='add'),
    # path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    # path('', BbIndexView.as_view(), name='index'),
]
