from django import forms
from .models import Dog, AdoptionRequest
from staff_panel.models import DoctorBooking

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'age_in_months' ,'price', 'description', 'image']



class DoctorBookingForm(forms.ModelForm):
    class Meta:
        model = DoctorBooking
        fields = ['pet_name', 'pet_breed', 'issue_description', 'booking_date', 'booking_time', 'address']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'issue_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe health issues or vaccination requirements'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Complete home address for vet visit'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'pet_breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (e.g. Labrador, Pug)'}),
        }

