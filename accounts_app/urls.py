from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-certificate/', views.create_certificate, name='create_certificate'),
    path('dashboard/edit-certificate/<int:pk>/', views.update_certificate, name='update_certificate'),
    path('dashboard/delete-certificate/<int:pk>/', views.delete_certificate, name='delete_certificate'),
]
