from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
#
# from .forms import CustomUserCreateForm, CustomUserChangeForm
from .models import CustomUser

admin.site.register(CustomUser)
#
# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreateForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('complete_name', 'email', 'phone', 'is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Informações Pessoais', {'fields': ('complete_name', 'phone')}),
#         ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
#     )
