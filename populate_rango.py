import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','rate_my_professor.settings')
import django
django.setup() 
from rango.models import *
from django.contrib.auth.models import User

def populate():

 

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
         'rating' : '3',
         'picture' : 'null',
         'subject' : 'ALG'
        },
        {'name' : 'Abby smith',
         'rating' : '5',
         'picture' : 'null',
         'subject' : 'WAD2'
        },
    ]

    phil_professors = [
        {'name' : 'Jack Black',
         'rating' : '3',
         'picture' : 'null',
         'subject' : 'Phil1'
        },
        {'name' : 'Sean Bean',
         'rating' : '5',
         'picture' : 'null',
         'subject' : 'Phil2'
        },
    ]

    comp_reviews = [
        {'prof':'John smith', 
         'createdby' : 'bmaguire530',
         'date': '2017-11-06 11:06:21.131900',
         'rating' : '3',
         'comment' : 'could give better examples'},
        {'prof':'Abby smith', 
         'createdby' : 'fdale530',
         'date': '2017-11-06 11:06:21.131900',
         'rating' : '5',
         'comment' : 'clear lecture slides helped a lot'},
    ]

    phil_reviews = [
        {'prof':'Jack Black', 
         'createdby' : 'bmaguire530',
         'date': '2017-11-06 11:06:21.131900',
         'rating' : '3',
         'comment' : 'alright lectures but boring topics'},
        {'prof':'Sean Bean', 
         'createdby' : 'fdale530',
         'date': '2017-11-06 11:06:21.131900',
         'rating' : '5',
         'comment' : 'Makes everything straightforward in lecture slides'},
    ]

    users = [
        {'username':'bmaguire530',
          'email': 'bmaguire530@rate.com',
          'password': 'groupproject'},
        {'username':'fdale530',
          'email': 'fdale@rate.com',
          'password': 'groupproject2'}
    ]
    


    

    departments = {
        'Computing' : { 'subjects' : comp_subjects, 'professors':comp_professors, 'reviews':comp_reviews},
        'Philosophy' : { 'subjects' : phil_subjects, 'professors':phil_professors, 'reviews':phil_reviews},
    }

    def add_department(name):
        d = Department.objects.get_or_create(name=name)[0]
        d.save()
        return d
    
    def add_subject(deptName, subName):
        s = Subject.objects.get_or_create(dept=deptName, name=subName)[0]
        s.save()
        return s
    
    def add_prof(name, rating, picture, subject):
        p = Professor.objects.get_or_create(name=name, rating=rating, picture=picture, subject=subject)[0]
        p.save()
        return p

    def add_review(prof, createdby, date, rating, comment):
        r = Reviews.objects.get_or_create(date=date, createdby=createdby, prof=prof, rating=rating, comment=comment)
        return r
    
    def add_user(username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return user

    
        

    for dept, dept_data in departments.items():
        a = add_department(dept)

        for s in dept_data['subjects']:
            b = add_subject(a, s['name'])

            for p in dept_data['professors']:
                if p['subject'] == s['name']:
                    c = add_prof(p['name'], p['rating'], p['picture'], b)

                    for r in dept_data['reviews']:
                        if r['prof'] == p['name']:
                            #for u in dept_data['users']:
                                #d = add_user(u['username'], u['email'], u['password'])
                                #if u['username'] == r['createdby']:
                                    add_review(c, r['createdby'], r['date'], r['rating'], r['comment'])
                

        
	
#Startexecutionhere!
if __name__=='__main__':
	print('Starting Rango population script...') 
	populate()
	