from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    # Adding a numeric text entry field for capturing mobile routing indicators
    mobile_number = forms.CharField(
        max_length=10, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'})
    )
    
    # Adding an image file upload field for handling profile avatar assets
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = User
        # Arranged fields order to sequence credential data before media uploads
        fields = [
            'username', 
            'email', 
            'mobile_number',
            'profile_image',
        ]