from django.urls import path
from .views import home, get_records

urlpatterns = [
    path('', home, name='home'),
    path('api/records/', get_records, name='get_records'),
]
