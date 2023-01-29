from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogOutView.as_view(), name='user_logout'),
    
    path('password_reset/', views.UserPasswordResetView.as_view(),
                                            name='password_reset'),

    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(),
                                            name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
                                            views.UserPasswordResetConfirmView.as_view(),
                                            name='password_reset_confirm'),

    path('password_reset/complete', views.UserPasswordResetCompleteView.as_view(),
                                            name='password_reset_complete'),
]
