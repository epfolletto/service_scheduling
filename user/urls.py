    # from django.urls import path
#
# # from .views import UserAPIView
# from .views import CreateSuperUserView
#
# # urlpatterns = [
# #     path('users/', UserAPIView.as_view(), name='users'),
# #     path('register/', UserAPIView.as_view(), name='register')
# # ]
#

from django.urls import path
from .views import CustomUserView

# urlpatterns = [
#     path('', CustomUserView.as_view(), name='all'),
#     path('register/', CustomUserView.as_view(), name='register'),
#     path('register/<int:pk>/', CustomUserView.as_view(), name='update'),
#     path('register/delete/<int:pk>/', CustomUserView.as_view(), name='delete'),
# ]

urlpatterns = [
    path('users/', CustomUserView.as_view()),
    path('users/<int:pk>/', CustomUserView.as_view()),
]
