from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.AppInstall.as_view()),
    path('sso_install/', views.Installer.as_view()),
    path('exportlist/', views.Import.as_view()),
    path('export/<str:import_id>/status/', views.Import.as_view()),
    path('user/<str:user__identifier>/conf', views.PimConf.as_view()),
]