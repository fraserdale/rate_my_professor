from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rango.models import *
from rango.forms import *

# Create your views here.
def index(request):
	recent_reviews = Reviews.objects.order_by('-date')[:5]
	top_professors = Professor.objects.order_by('-rating')[:5]

	response = render(request, 'rango/index.html', context = {'recent_reviews' : recent_reviews, 'top_professors' : top_professors})
	return response


def register(request):

	registered = False


	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('rango:index'))
			else:
				return HttpResponse("Your account is disabled.")
		else:

			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def recent(request):
	recent_reviews = Reviews.objects.order_by('date')[:7]
	print(recent_reviews)
	response = render(request, 'rango/recent.html', context = {'recent_list': recent_reviews})
	return response


def leaderboard(request):
	leaderboard_list = Professor.objects.order_by('-rating')[:7]
	print(leaderboard_list)
	response = render(request, 'rango/leaderboard.html', context = {'leaderboard_list': leaderboard_list})
	return response


def professors(request):
	professors_list = Professor.objects.all()

	response = render(request, 'rango/professors.html', context = {'professors_list': professors_list})
	return response

def show_professor(request, professor_name_slug):
	context_dict = {}
	# Create a context dictionary which we can pass # to the template rendering engine. context_dict = {}
	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# The .get() method returns one model instance or raises an exception. 
		professor = Professor.objects.get(slug=professor_name_slug)
		# Retrieve all of the associated pages.
		# The filter() will return a list of page objects or an empty list. 
		reviews = Reviews.objects.filter(professor=professor)
		# Adds our results list to the template context under name pages.
		context_dict['reviews'] = reviews
		# We also add the category object from
		# the database to the context dictionary.
		# We'll use this in the template to verify that the category exists. 
		context_dict['professor'] = professor
	except Professor.DoesNotExist:
		# We get here if we didn't find # Don't do anything -
		# the template will display the 
		context_dict['professor'] = None 
		context_dict['reviews'] = None
		# Go render the response and return
		#the specified category.
		#"no category" message for us.
		#qit to the client.
	return render(request, 'rango/professor.html', context=context_dict)


# url: professor/slug
# def professor_view(request):
#

# url: professor/slug/review
# def professor_review(request):
#
