from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from customer.models import Dog, CommunityGroup
from accounts.models import DoctorProfile

User = get_user_model()

# Admin verification check
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

# Main Admin Dashboard View
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_dashboard_view(request):
  # Analytics Counts
  if hasattr(User, 'role'):
    total_users = (
        User.objects.filter(is_superuser=False).exclude(role='doctor').count()
    )
  else:
    total_users = User.objects.filter(is_superuser=False).count()

  total_pets = Dog.objects.count()
  total_groups = CommunityGroup.objects.count()
  total_doctors = DoctorProfile.objects.count()

  # Recent Data (for initial preview)
  recent_users = User.objects.filter(is_superuser=False).order_by('-id')[:5]
  recent_pets = Dog.objects.all().order_by('-id')[:5]
  recent_groups = CommunityGroup.objects.all().order_by('-id')[:5]
  doctors_list = DoctorProfile.objects.all().order_by('-id')

  # All Data (for "View All" Popups)
  all_pets = Dog.objects.all().order_by('-id')
  all_groups = CommunityGroup.objects.all().order_by('-id')

  context = {
      'total_users': total_users,
      'total_pets': total_pets,
      'total_groups': total_groups,
      'total_doctors': total_doctors,
      'recent_users': recent_users,
      'recent_pets': recent_pets,
      'recent_groups': recent_groups,
      'doctors_list': doctors_list,
      'all_pets': all_pets,
      'all_groups': all_groups,
  }
  return render(request, 'admin_dashboard.html', context)


# Admin Add New Doctor
@user_passes_test(is_admin, login_url='/accounts/login/')
def add_doctor_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        specialization = request.POST.get('specialization')
        qualification = request.POST.get('qualification')
        district = request.POST.get('district')
        fee = request.POST.get('consultation_fee')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'add_doctor.html')

        # Create user account with role='doctor'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='doctor',
            is_staff=True
        )
        # Create Doctor Profile linked to this user
        DoctorProfile.objects.create(
            user=user,
            specialization=specialization,
            qualification=qualification,
            district=district,
            consultation_fee=fee,
            is_available=True
        )
        messages.success(request, f'Dr. {username} added successfully!')
        return redirect('admin_panel:dashboard')

    return render(request, 'add_doctor.html')

# Admin Edit Doctor
@user_passes_test(is_admin, login_url='/accounts/login/')
def edit_doctor_view(request, doctor_id):
    doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
    if request.method == 'POST':
        doctor_profile.specialization = request.POST.get('specialization')
        doctor_profile.qualification = request.POST.get('qualification')
        doctor_profile.district = request.POST.get('district')
        doctor_profile.consultation_fee = request.POST.get('consultation_fee')
        doctor_profile.is_available = 'is_available' in request.POST
        doctor_profile.save()
        messages.success(request, f'Dr. {doctor_profile.user.username} details updated successfully!')
        return redirect('admin_panel:dashboard')

    return render(request, 'edit_doctor.html', {'doctor_profile': doctor_profile})

# Admin Delete Doctor
@user_passes_test(is_admin, login_url='/accounts/login/')
def delete_doctor_view(request, doctor_id):
    doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor_profile.user.delete()
    messages.success(request, 'Doctor removed successfully.')
    return redirect('admin_panel:dashboard')

# Admin Delete Community Group Action
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_group(request, group_id):
    group = get_object_or_404(CommunityGroup, id=group_id)
    group_name = group.name
    group.delete()
    messages.success(request, f'Group "{group_name}" deleted by Admin.')
    return redirect('admin_panel:dashboard')


from customer.models import Dog  

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_pet_view(request, pet_id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('customer:index')
        
    pet = get_object_or_404(Dog, id=pet_id)
    pet.delete()
    messages.success(request, "Pet listing removed successfully by Admin.")
    return redirect('admin_panel:dashboard')
