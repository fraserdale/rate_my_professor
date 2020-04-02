from django import forms
from django.contrib.auth.models import User
from rango.models import *


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)

class PageForm(forms.ModelForm):
	comment = forms.CharField(max_length=128,
		help_text='Please enter the review of the page.')
	rating = forms.IntegerField (max_value=5, min_value=0,
		help_text="Please enter the rating out of 5") 

	class Meta:
		model = Reviews 
		fields = ('rating','comment')

		#include (fields = ('pages')) / exclude (exclude = ('cartegory')) 

