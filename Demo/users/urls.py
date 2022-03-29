from django.urls import path
from .views import user_login, user_signup, user_logout, UserUpdateView

app_name = 'Users'

urlpatterns = [
    path('login/', user_login, name='user-login-view'),
    path('signup/', user_signup, name='user-signup-view'),
    path('update/<int:id>', UserUpdateView.as_view(), name='user-update-view'),
    path('logout/', user_logout, name='user-logout-view'),
]
