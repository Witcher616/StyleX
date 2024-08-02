from django.urls import path

from users.views import login, UserRegistrView, UserProfileView, logout, EmailVerificationView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registr/', UserRegistrView.as_view(), name='registr'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name="verify")
]