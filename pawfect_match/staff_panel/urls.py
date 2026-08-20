from django.urls import path
from . import views

app_name = 'staff_panel'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard_view, name='dashboard'),
    path('booking/<int:booking_id>/<str:status>/', views.update_booking_status_view, name='update_status'),
]