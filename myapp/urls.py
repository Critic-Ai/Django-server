from django.urls import path
from .views import get_records

urlpatterns = [
    path('api/records/', get_records, name='get_records'),
]
