from django.urls import path
from .views import index, about, contacts


urlpatterns = [
    path('', index),
    path('index', index),
    path('about', about),
    path('contacts', contacts),

]