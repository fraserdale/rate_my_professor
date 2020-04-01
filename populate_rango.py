import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')
import django
django.setup() 
from rango.models import Reviews,User

def populate():

    departments = [
        {'Computing' : { 'subjects' : comp_subjects, }},
        {'Philosophy' : { 'subjects' : phil_subjects, }},
    ]

    comp_subjects = [
        {'name' : 'ALG', },
        {'name' : 'WAD2',},
    ]

    phil_subjects = [
        {'name' : 'Phil1'},
        {'name' : 'Phil2'},
    ]

    comp_professors = [
        {'name' : 'John smith',
         'rating' : '3.5',
         'picture' : null,
        },
        {'name' : 'Abby smith',
         'rating' : '5',
         'picture' : null,
        },
    ]

    phil_professors = [
        {'name' : 'Jack Black',
         'rating' : '3.5',
         'picture' : null,
        },
        {'name' : 'Sean Bean',
         'rating' : '5',
         'picture' : null,
        },
    ]

    comp_reviews = [
        {'date': '25/11/2019',
         'rating' : '3.5',
         'comment' : 'could give better examples'},
        {'date': '29/12/2018',
         'rating' : '5',
         'comment' : 'clear lecture slides helped a lot'},
    ]

    phil_reviews = [
        {'date': '25/11/2019',
         'rating' : '3.5',
         'comment' : 'alright lectures but boring topics'},
        {'date': '29/12/2018',
         'rating' : '5',
         'comment' : 'Makes everything straightforward in lecture slides'},
    ]
	
#Startexecutionhere!
if __name__=='__main__':
	print('Starting Rango population script...') 
	populate()
	