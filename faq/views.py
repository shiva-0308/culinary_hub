from django.shortcuts import render
from .models import FAQ

def faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq/faqs.html', {'faqs': faqs})
