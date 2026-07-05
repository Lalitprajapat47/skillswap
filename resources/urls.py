from django.urls import path
from . import views

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('upload/', views.upload_resource, name='upload_resource'),
    path('delete/<int:resource_id>/', views.delete_resource, name='delete_resource'),
]