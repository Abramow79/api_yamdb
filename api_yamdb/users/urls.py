from api.views import SignUpApiView, TokenRegApiView
from django.urls import path

urlpatterns = [
    path("signup/", SignUpApiView.as_view(), name="signup"),
    path("token/", TokenRegApiView.as_view(), name="token_access"),
]
