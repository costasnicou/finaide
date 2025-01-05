from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('add-wallet/', views.add_wallet, name='add_wallet'),
    # path('add-transaction/<int:wallet_id>/', views.add_transaction, name='add_transaction'),
    path('signup/', views.signup, name='signup'),
  
    # path('delete-wallet/<int:wallet_id>/', views.delete_wallet, name='delete_wallet'),
]
