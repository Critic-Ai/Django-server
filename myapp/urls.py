from django.urls import path
from .views import get_records
from .views import register

urlpatterns = [
    path('api/records/', get_records, name='get_records'),
    path('api/register/', register, name='register'),
]
