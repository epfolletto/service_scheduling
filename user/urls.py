from django.urls import path
from .views import CustomUserView

urlpatterns = [
    path('users/', CustomUserView.as_view()),
    path('users/<int:pk>/', CustomUserView.as_view()),
]
