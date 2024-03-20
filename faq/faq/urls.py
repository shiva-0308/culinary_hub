from django.urls import path
from .views import faqs

urlpatterns = [
    path('', faqs, name='faqs'),
]
