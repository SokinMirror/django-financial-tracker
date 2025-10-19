from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    # When a user visits the app's root, use the transaction_list view
    path('', views.transaction_list, name='transaction-list'),
]