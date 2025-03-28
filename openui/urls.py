from django.urls import path
from .views import sample, tabulator_view

urlpatterns = [
    path('sample/', sample, name='sample'),
    path('tabulator/', tabulator_view, name='tabulator_view'),
]


