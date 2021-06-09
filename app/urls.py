from django.urls import path
from . import views


# TODO Add custom URLs under the below list and your their implemenatation in views
urlpatterns = [
    path('', views.index, name='index'),
    # path('v1/install/', views.PIMInstall.as_view()),
    path('/install/', views.Install.as_view()),
    path('uninstall/', views.Uninstall.as_view()),
    path('health/',views.Health.as_view())
]
