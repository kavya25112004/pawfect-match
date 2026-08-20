from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Models Imports
from .models import Dog
from accounts.models import DoctorProfile
from staff_panel.models import DoctorBooking
from .forms import DogForm, DoctorBooking
from .models import Dog, CommunityGroup, GroupPost,GroupMembership
from django.contrib.auth import get_user_model


# Landing Page View
def index_view(request):
    return render(request, 'landing_page.html')


# Marketplace Main View
@login_required
def home_view(request):
    query = request.GET.get('q')
    if query:
        dogs = Dog.objects.filter(breed__icontains=query)
    else:
        dogs = Dog.objects.all()
        
    return render(request, 'customer_home.html', {'dogs': dogs})



# User Profile View
@login_required
def profile_view(request):
  user = request.user

  # Edit Profile POST Request
  if request.method == 'POST':
    user.email = request.POST.get('email', user.email)
    if hasattr(user, 'phone'):
      user.phone = request.POST.get('phone', '')
    if hasattr(user, 'address'):
      user.address = request.POST.get('address', '')
    user.save()
    messages.success(request, 'Profile updated successfully!')
    return redirect('customer:profile')

  # Fetch User's Listed Dogs
  my_dogs = Dog.objects.filter(seller=user)

  # Fetch Groups Created by User
  created_groups = CommunityGroup.objects.filter(created_by=user)

  # Fetch Groups Where User is an Approved Member
  approved_group_ids = GroupMembership.objects.filter(
      user=user, status='APPROVED'
  ).values_list('group_id', flat=True)
  joined_groups = CommunityGroup.objects.filter(id__in=approved_group_ids)

  # Combine both (without duplicates)
  my_groups = (created_groups | joined_groups).distinct()

  context = {
      'user': user,
      'my_dogs': my_dogs,
      'my_groups': my_groups,
  }
  return render(request, 'customer_profile.html', context)


# Add New Dog View
@login_required
def add_dog_view(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.seller = request.user
            dog.save()
            messages.success(request, 'Pet posted successfully!')
            return redirect('customer:home')
    else:
        form = DogForm()
    return render(request, 'customer_add_dog.html', {'form': form})


# Dog Detail View
@login_required
def dog_detail_view(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'customer_dog_detail.html', {'dog': dog})


# Doctor List View
@login_required
def doctor_list_view(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


# Book Doctor View

User = get_user_model()


@login_required
def book_doctor_view(request, doctor_id):
    doctor_user = get_object_or_404(User, id=doctor_id)

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_breed = request.POST.get('pet_breed')
        preferred_date = request.POST.get('preferred_date')
        booking_time = request.POST.get('booking_time')
        health_issue = request.POST.get('health_issue', '').strip()
        address = request.POST.get('address')

        try:
            booking = DoctorBooking()
            booking.customer = request.user
            booking.doctor = doctor_user
            booking.pet_name = pet_name

            if hasattr(booking, 'pet_breed'):
                booking.pet_breed = pet_breed
            elif hasattr(booking, 'breed'):
                booking.breed = pet_breed

            if hasattr(booking, 'booking_date'):
                booking.booking_date = preferred_date
            elif hasattr(booking, 'preferred_date'):
                booking.preferred_date = preferred_date

            if hasattr(booking, 'booking_time'):
                booking.booking_time = booking_time
            elif hasattr(booking, 'preferred_time'):
                booking.preferred_time = booking_time

            # Health Concern mapping
            if hasattr(booking, 'health_issue'):
                booking.health_issue = health_issue
            if hasattr(booking, 'health_concern'):
                booking.health_concern = health_issue
            if hasattr(booking, 'reason'):
                booking.reason = health_issue
            if hasattr(booking, 'description'):
                booking.description = health_issue
            if hasattr(booking, 'problem'):
                booking.problem = health_issue

            booking.address = address
            booking.status = 'Pending'

            booking.save()

            messages.success(request, 'Doctor consultation booked successfully!')
            return redirect('customer:my_bookings')

        except Exception as e:
            messages.error(request, f'Booking Error: {str(e)}')
            return render(request, 'book_doctor.html', {'doctor': doctor_user})

    return render(request, 'book_doctor.html', {'doctor': doctor_user})


@login_required
def my_bookings_view(request):
    bookings = DoctorBooking.objects.filter(customer=request.user).order_by('-id')
    return render(request, 'my_bookings.html', {'bookings': bookings})








# Smart Care Planner View
@login_required
def care_planner_view(request):
    pet_age = request.GET.get('age')
    care_info = None

    if pet_age:
        try:
            age_months = int(pet_age)
            if age_months <= 6:
                care_info = {
                    'stage': 'Puppy (0 - 6 Months)',
                    'diet': '4 meals/day (High Protein Puppy Food & Warm Water)',
                    'vaccines': 'DHPP (6-8 weeks), Rabies (12-16 weeks), Booster shots',
                    'exercise': '15-20 mins daily light playtime',
                    'tips': 'Focus on potty training, socialisation, and avoid intense workouts.'
                }
            elif age_months <= 24:
                care_info = {
                    'stage': 'Young Adult (7 - 24 Months)',
                    'diet': '2 meals/day (Adult Balanced Kibble / Fresh Meat & Veggies)',
                    'vaccines': 'Annual Rabies & DHPP Booster',
                    'exercise': '45-60 mins daily walks & fetch games',
                    'tips': 'Obedience training, dental care, and active physical routines.'
                }
            else:
                care_info = {
                    'stage': 'Senior Pet (2+ Years)',
                    'diet': '2 meals/day (Low Fat, High Fiber & Joint Support Food)',
                    'vaccines': 'Annual Health Checkup & Core Boosters',
                    'exercise': '30 mins gentle morning/evening walk',
                    'tips': 'Joint supplements, regular vet visits, and soft bedding.'
                }
        except ValueError:
            pass

    return render(request, 'care_planner.html', {'care_info': care_info, 'selected_age': pet_age})







#Groups Main List & Create Group
@login_required
def community_groups_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            group = CommunityGroup.objects.create(name=name, description=description, created_by=request.user)
            GroupMembership.objects.create(group=group, user=request.user, status='APPROVED')
            messages.success(request, f'Group "{name}" created successfully!')
            return redirect('customer:group_detail', group_id=group.id)

    groups = CommunityGroup.objects.all().order_by('-created_at')
    return render(request, 'community_groups.html', {'groups': groups})


#Group Detail Page (Public Info + Locked Messages)
@login_required
def group_detail_view(request, group_id):
    group = get_object_or_404(CommunityGroup, id=group_id)
    
    # Check if current user is Creator or Approved Member
    is_creator = (group.created_by == request.user)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    
    is_approved = is_creator or (membership and membership.status == 'APPROVED')
    membership_status = membership.status if membership else None

    # Posts (only fetched if approved)
    posts = group.posts.all().order_by('-created_at') if is_approved else []
    
    # Pending requests list (only visible to Creator)
    pending_requests = GroupMembership.objects.filter(group=group, status='PENDING') if is_creator else []

    # Handle Post Creation
    if request.method == 'POST' and is_approved:
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        if content or image or video:
            GroupPost.objects.create(group=group, user=request.user, content=content, image=image, video=video)
            messages.success(request, 'Post shared successfully!')
            return redirect('customer:group_detail', group_id=group.id)

    return render(request, 'group_detail.html', {
        'group': group,
        'posts': posts,
        'is_creator': is_creator,
        'is_approved': is_approved,
        'membership_status': membership_status,
        'pending_requests': pending_requests
    })


#Join Request View
@login_required
def join_group_request(request, group_id):
    group = get_object_or_404(CommunityGroup, id=group_id)
    membership, created = GroupMembership.objects.get_or_create(group=group, user=request.user)
    if created or membership.status == 'REJECTED':
        membership.status = 'PENDING'
        membership.save()
        messages.success(request, f'Join request sent to "{group.name}". Once the admin approves, you can view discussions!')
    else:
        messages.info(request, 'Your join request is already submitted.')
    return redirect('customer:group_detail', group_id=group.id)


# Manage Requests (Approve / Reject)
@login_required
def manage_join_request(request, membership_id, action):
    membership = get_object_or_404(GroupMembership, id=membership_id)
    if membership.group.created_by != request.user:
        messages.error(request, 'Only the group admin can manage join requests.')
        return redirect('customer:community_groups')
    
    if action == 'approve':
        membership.status = 'APPROVED'
        membership.save()
        messages.success(request, f'Approved {membership.user.username} into the group!')
    elif action == 'reject':
        membership.status = 'REJECTED'
        membership.save()
        messages.warning(request, f'Rejected request from {membership.user.username}.')
        
    return redirect('customer:group_detail', group_id=membership.group.id)







@login_required
def delete_dog_view(request, pk):
    dog = get_object_or_404(Dog, id=pk, seller=request.user)
    
    dog.delete()
    messages.success(request, 'Pet listing deleted successfully!')
    return redirect('customer:profile') 

@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(DoctorBooking, id=booking_id, customer=request.user)
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('customer:my_bookings')

@login_required
def complete_booking_customer_view(request, booking_id):
    booking = get_object_or_404(DoctorBooking, id=booking_id, customer=request.user)
    booking.status = 'Completed'
    booking.save()
    messages.success(request, "Consultation marked as Completed.")
    return redirect('customer:my_bookings')


@login_required
def edit_dog_view(request, pk):
    dog = get_object_or_404(Dog, id=pk, seller=request.user)
    if request.method == 'POST':
        dog.name = request.POST.get('name', dog.name)
        dog.breed = request.POST.get('breed', dog.breed)
        
        dog.price = request.POST.get('price', dog.price)
        dog.description = request.POST.get('description', dog.description)

        age_val = request.POST.get('age')
        if hasattr(dog, 'age_in_months') and age_val:
           dog.age_in_months = age_val
        elif hasattr(dog, 'age_months') and age_val:
           dog.age_months = age_val
        elif hasattr(dog, 'age') and age_val:
           dog.age = age_val

        if 'image' in request.FILES:
            dog.image = request.FILES['image']

        dog.save()
        messages.success(request, f'Pet "{dog.name}" updated successfully!')
        
    return redirect('customer:profile')

@login_required
def delete_group_view(request, group_id):
    group = get_object_or_404(CommunityGroup, id=group_id)
    if group.created_by == request.user:
        group.delete()
        messages.success(request, f'Group "{group.name}" deleted successfully.')
    else:
        messages.error(request, "Only the group admin can delete this group.")
    return redirect('customer:profile')