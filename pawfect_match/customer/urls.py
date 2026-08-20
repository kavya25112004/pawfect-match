from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('marketplace/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('add-dog/', views.add_dog_view, name='add_dog'),
    path('dog/<int:pk>/', views.dog_detail_view, name='dog_detail'),
    path('delete-dog/<int:pk>/', views.delete_dog_view, name='delete_dog'),
    path('pet/edit/<int:pk>/', views.edit_dog_view, name='edit_dog'),
    
    

    
    path('doctors/', views.doctor_list_view, name='doctor_list'),
    path('book-doctor/<int:doctor_id>/', views.book_doctor_view, name='book_doctor'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('booking/<int:booking_id>/complete/', views.complete_booking_customer_view, name='complete_booking_customer'),
    
    
    path('care-planner/', views.care_planner_view, name='care_planner'),
    path('community/', views.community_groups_view, name='community_groups'),
    path('community/group/<int:group_id>/', views.group_detail_view, name='group_detail'),
    path('community/join/<int:group_id>/', views.join_group_request, name='join_group_request'),
    path('community/manage-request/<int:membership_id>/<str:action>/', views.manage_join_request, name='manage_join_request'),
    path('group/delete/<int:group_id>/', views.delete_group_view, name='delete_group'), 
]