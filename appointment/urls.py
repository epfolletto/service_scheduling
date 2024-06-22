from django.urls import path

from .views import AppointmentAPIView

urlpatterns = [
    path('appointments/', AppointmentAPIView.as_view()),
    path('appointments/<int:pk>/', AppointmentAPIView.as_view()),
]
