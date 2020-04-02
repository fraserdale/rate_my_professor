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
	recent_reviews = Reviews.objects.order_by('date')[:5]
	top_professors = Professor.objects.order_by('rating')[:5]

	response = render(request, 'rango/index.html', context = {'recent_reviews' : recent_reviews, 'top_rated' : top_professors})
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

	response = render(request, 'rango/recent.html', context = {'recent_list': recent_reviews})
	return response


def leaderboard(request):
	leaderboard_list = Professor.objects.order_by('rating')[:7]

	response = render(request, 'rango/leaderboard.html', context = {'leaderboard_list': leaderboard_list})
	return response


def professors(request):
	professors_list = Professor.objects.all()

	response = render(request, 'rango/professors.html', context = {'professors_list': professors_list})
	return response

# url: professor/slug
# def professor_view(request):
#

# url: professor/slug/review
# def professor_review(request):
#
