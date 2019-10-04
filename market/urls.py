from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:isbn>', views.isbn),
]