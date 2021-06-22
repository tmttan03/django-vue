from django.urls import path, re_path
from .api import (
    Users,
    User,
    Login,
    Logout,
    Register,
    ChangeEmail
)

urlpatterns = [

    path('', Users.as_view({
        'get': 'get',
    }), name="users"),

    path('auth/', User.as_view({
        'get': 'get',
        'post': 'update',
    }), name="user_detail"),

    path('auth-user/', User.as_view({
        'get': 'get_current',
    }), name="current-user"),

    path('auth/register/', Register.as_view(), name="register"),

    path('auth/login/', Login.as_view(), name="login"),

    path('auth/logout/', Logout.as_view(), name="logout"),

    path('auth/email/', ChangeEmail.as_view(), name="change_email"),
]
