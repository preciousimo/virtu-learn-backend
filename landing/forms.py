from django import forms
from django.contrib.auth.forms import UserCreationForm
from landing.models import User

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class":"form-control rounded-input", 'placeholder':'Username'}))
	email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={"class":"form-control rounded-input", 'placeholder':'Email'})) 
	password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={"class":"form-control rounded-input", 'placeholder':'Password'}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class":"form-control rounded-input", 'placeholder':'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]
		
	