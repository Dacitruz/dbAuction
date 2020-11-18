from django.urls import path
from .views import sign_up, sign_in, sign_out, edit_profile


urlpatterns = [
    path('sign_up', sign_up),
    path('sign_in', sign_in),
    path('sign_out', sign_out),
    path('profile', edit_profile),
]