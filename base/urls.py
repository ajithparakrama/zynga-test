from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views #import this


urlpatterns = [
    path('', views.allview, name="home"),
    path('about',views.about, name="about"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser  , name="logout"),
    path('register/', views.registerUser  , name="register"),
    path('fogot/', views.fogot, name="fogot"),
    path('profile/', views.profile, name="profile"),
    path('user-accounts',views.user_accounts,name="user-accounts"),
    path('edit-user/<str:pk>/',views.edit_user,name="edit-user"),
    path('change-password/', views.changepass, name="change-password"),
    path('newrecord/', views.newrecord  , name="newrecord"),
    path('editrecord/<str:pk>/', views.editrecord, name="editrecord"),
    path('approverecord/<str:pk>/', views.approverecord, name="approverecord"),
    path('export/', views.export_record, name='export'),
    path('export-user-record',views.export_record_user, name='export_record_user'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset", views.password_reset_request, name="password_reset")
]
