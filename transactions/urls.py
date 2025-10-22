from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    # When a user visits the app's root, use the transaction_list view
    path('', views.transaction_list, name='transaction-list'),

    # DELETE URL
    # <int:pk> captures the ID from the URL and passes it as an argument named 'pk'
    path('delete/<int:pk>/', views.transaction_delete, name='transaction-delete'),

    # EDIT URL 
    path('edit/<int:pk>/', views.transaction_edit, name='transaction-edit'),

    # CSV Upload URL
    path('upload/', views.upload_csv, name='upload-csv'),

    # SUM URL
    path('summary/', views.transaction_summary, name='transaction-summary'),
]