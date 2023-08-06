from django.urls import path, include
from rest_framework import routers

from . import views
from .views import UserTokenVerifyView

app_name = 'user'

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('role', views.RoleViewSet)
router.register('org/registration', views.OrganisationViewSet)
router.register('org/check', views.ValidateOrganisationViewSet)
router.register('device_token', views.DeviceTokenAPIView)
router.register('billing_detail', views.BillingDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/invite/<str:token>/', views.InviteUserViewSet.as_view()),
    path('login/', views.UserAuthenticationView.as_view()),
    path('token/verify/', UserTokenVerifyView.as_view()),
    path('otp/verify/', views.UserActivateView.as_view()),
    path('otp/request/', views.NewOtpView.as_view()),
    path('token/refresh/', views.CustomTokenRefreshView.as_view()),
    path('password_reset/request/', views.ResetPasswordRequestToken.as_view()),
    path('password_reset/confirm/', views.ResetPasswordConfirm.as_view()),
    path('password_reset/validate_token/', views.ResetPasswordValidateToken.as_view()),
    # path('social/login/google/', views.GoogleLogin.as_view()),
    # path('social/login/facebook/', views.FacebookLogin.as_view())
]
