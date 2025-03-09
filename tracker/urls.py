from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('delete-transaction/<int:id>', views.deleteTransaction, name='delete-transaction'),
]