from django.urls import path
from . import views

urlpatterns = [
  
  path('register', views.register_view, name='register'),
  path('login', views.login_view, name='login'),
  path('logout', views.logout_view, name='logout'),
  
  path('', views.index, name='index'),
  path('all-transactions', views.all_transactions, name='all-transactions'),
  path('delete-transaction/<int:id>', views.deleteTransaction, name='delete-transaction'),
]