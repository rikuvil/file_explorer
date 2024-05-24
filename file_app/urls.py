
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('container_list/', views.container_list_view, name='container_list'),
    path('container_detail/', views.container_detail_view, name='container_detail'),
    path('file_list/', views.file_list_view, name='file_list'),
    path('file_list/<path:path>/', views.file_list_view, name='file_list'),
    path('file_detail/<path:path>/', views.file_detail_view, name='file_detail'),
]
