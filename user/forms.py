# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#
# from .models import CustomUser
#
#
# class CustomUserCreateForm(UserCreationForm):
#
#     class Meta:
#         model = CustomUser
#         fields = ('complete_name', 'phone')
#         labels = {'email': 'Username/E-mail'}
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user
#
#
# class CustomUserChangeForm(UserChangeForm):
#
#     class Meta:
#         model = CustomUser
#         fields = ('complete_name', 'phone')
