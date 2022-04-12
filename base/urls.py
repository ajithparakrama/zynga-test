from django.urls import path
from . import views


urlpatterns = [
    path('', views.allview, name="home"),
    path('about',views.about, name="about"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser  , name="logout"),
    path('register/', views.registerUser  , name="register"),
    path('fogot/', views.fogot, name="fogot"),
    path('profile/', views.profile, name="profile"),
    path('newrecord/', views.newrecord  , name="newrecord"),
    path('editrecord/<str:pk>/', views.editrecord, name="editrecord"),
    path('approverecord/<str:pk>/', views.approverecord, name="approverecord"),
]
