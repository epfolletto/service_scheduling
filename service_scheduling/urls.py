# from django.contrib import admin
# from django.urls import path, include
# from user.views import UserViewSet
# from rest_framework import routers?


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

# urlpatterns = [
#     path('api/', include('user.urls')),
#     path('api/', include('appointment.urls')),
#     path('', include(router.urls)),
#     path("admin/", admin.site.urls),
#     path('api-auth/', include('rest_framework.urls'))
# ]


from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import PasswordResetView, PasswordResetConfirmView

# from rest_framework import routers
# from user.views import CustomUserView

# router = routers.DefaultRouter()
# router.register(r'users', CustomUserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('appointment.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
