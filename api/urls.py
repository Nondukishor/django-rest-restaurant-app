from django.urls import path
from .views import RestaurantViewSet, MenuViewSet, VoteViewSet,  SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView

app_name="api"
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('restaurants/', RestaurantViewSet.as_view(), name='restaurants'),
    path('menus/', MenuViewSet.as_view(), name='menus'),
    path('votes/', VoteViewSet.as_view(), name='votes'),
]