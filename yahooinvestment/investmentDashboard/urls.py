from django.urls import path
from . import views

app_name = 'TestApp'
urlpatterns = [
    path('', views.investments_view, name='index'),
    path('schwab/', views.schwab_view, name='schwab'),
    path('fidelity/', views.fidelity_view, name='fidelity'),
]
