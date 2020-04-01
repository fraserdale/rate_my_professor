import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')
import django
django.setup() 
from rango.models import Reviews,User
def populate():
	# First, we will create lists of dictionaries containing the pages
	# we want to add into each category.
	# Then we will create a dictionary of dictionaries for our categories. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.
	reviews = [
		{'comment': 'Test reviews'] 

	# If you want to add more categories or pages, # add them to the dictionaries above.
	# The code below goes through the cats dictionary, then adds each category, # and then adds all the associated pages for that category.
	for cat, cat_data in cats.items():
		c = add_cat(cat, cat_data['views'], cat_data['likes'])
		for p in cat_data['pages']:
			add_page(c, p['title'], p['url'], p['views'])
			# Print out the categories we have added.
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print(f'- {c}: {p}')

def add_review(comment):
	p = Reviews.objects.get_or_create(comment=comment)[0] 
	p.url=url
	p.views=views
	p.save()
	return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

#Startexecutionhere!
if __name__=='__main__':
	print('Starting Rango population script...') 
	populate()
	