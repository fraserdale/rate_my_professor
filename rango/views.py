from django.shortcuts import render

# Create your views here.
def index(request):
	response = render(request,'rango/index.html')
	return response