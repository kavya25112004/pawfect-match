from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard_view, name='dashboard'),
    path('add-doctor/', views.add_doctor_view, name='add_doctor'),
    path('edit-doctor/<int:doctor_id>/', views.edit_doctor_view, name='edit_doctor'),
    path('delete-doctor/<int:doctor_id>/', views.delete_doctor_view, name='delete_doctor'),
    path('group/delete/<int:group_id>/', views.admin_delete_group, name='delete_group'),
    path('pet/delete/<int:pet_id>/', views.admin_delete_pet_view, name='delete_pet'),
]