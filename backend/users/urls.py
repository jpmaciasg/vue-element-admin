from django.urls import path
from .views import CreateUserAPIView, AuthUserAPIView, UserRetrieveUpdateAPIView, UserListingAPIView , UserSingleAPIView, UserPromotorAPIView,RoleAPIView,UserInfoAPIView, Logout
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
 
urlpatterns = [
    path('create', CreateUserAPIView.as_view()),
    path('update/<int:id>', UserRetrieveUpdateAPIView.as_view()),
    path('login', obtain_jwt_token),
    path('logout', Logout.as_view()),
    path('auth-refresh', refresh_jwt_token),
    path('list', CreateUserAPIView.as_view()),
    path('<int:id>',UserSingleAPIView.as_view()),
    path('promotors', UserPromotorAPIView.as_view({'get': 'list'})),
    path('roles', RoleAPIView.as_view({'get': 'list'})),
    path('info',UserInfoAPIView.as_view()),
]
