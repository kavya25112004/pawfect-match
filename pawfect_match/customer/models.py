from django.db import models

# Create your models here.

from django.conf import settings

class Dog(models.Model):
    LISTING_TYPES = (
        ('free', 'Free Adoption'),
        ('sell', 'For Sale'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    AVAILABILITY_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold / Adopted'),
    )

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listed_dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age_in_months = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES, default='free')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    district = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='dogs/')
    
    
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.breed} ({self.listing_type})"


class AdoptionRequest(models.Model):
    REQUEST_STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='requests')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_requests')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.buyer.username} for {self.dog.name}"






from django.contrib.auth.models import User 
# 1. Community Group Model
class CommunityGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2. Group Membership / Join Request Model
class GroupMembership(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_memberships')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.status})"

# 3. Posts & Media Model
class GroupPost(models.Model):
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='community_posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='community_posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
