from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='test'),
    path('reload/', views.reload, name='reload'),
]