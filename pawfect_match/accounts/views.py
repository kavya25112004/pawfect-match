from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('customer:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken! Please choose another one.')
            return render(request, 'register.html')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists!')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            if hasattr(user, 'address'):
                user.address = address
            
            user.save()

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('accounts:login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        elif getattr(request.user, 'is_doctor', False) or getattr(request.user, 'role', '') == 'doctor':
            return redirect('staff_panel:dashboard')
        return redirect('customer:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel:dashboard')
            elif getattr(user, 'is_doctor', False) or getattr(user, 'role', '') == 'doctor':
                return redirect('staff_panel:dashboard')
            else:
                return redirect('customer:index')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')