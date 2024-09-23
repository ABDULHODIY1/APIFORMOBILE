from django.urls import path
from .views import *

urlpatterns = [
    path('',Base.as_view(), name='home'),
    path('show',Show.as_view(), name='show'),
]