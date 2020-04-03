#
# tests.py
# small series of unit tests to test the functionality of the web app
#
# adapted from
# tests_chapter9.py from https://github.com/maxwelld90/tango_with_django_2_code/tree/master/progress_tests
# tests_chapter9.py written and revised bby Leif Azzopardi and David Maxwell
#       with assistance from Gerardo A-C and Enzo Roiz
#
# In order to run these tests, run:
# $ python manage.py test rango.tests
#

import os
import re
import inspect
import tempfile
import rango.models
from rango import forms
from populate_rango import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_student_object():
    """
    create a user object
    """
    user = User.objects.get_or_create(username='temp_student_user',
                                      first_name='Student',
                                      last_name='User',
                                      email='student@student.gla.ac.uk')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_professor_object():
    """
    create a user object
    """
    user = User.objects.get_or_create(username='temp_professor_user',
                                      first_name='Professor',
                                      last_name='User',
                                      email='professor@glasgow.ac.uk')[0]
    user.set_password('test789xyz')
    user.save()

    return user

def create_super_user_object():
    """
    create a super user (admin) account
    """
    return User.objects.create_superuser('admin', 'admin@glasgow.ac.uk', 'testpassword')

def get_template(path_to_template):
    """
    return string representation of a template file
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str

class ModelTests(TestCase):
    """
    checks whether the UserProfile model operates as expected
    """
    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in rango.models and are all required
        attributes present?
        Assertion fails if values cannot be assigned to all required fields.
        """
        self.assertTrue('UserProfile' in dir(rango.models))

        user_profile = rango.models.UserProfile()

        expected_attributes = {

        }


class RegisterFormClassTests(TestCase):
    """
    Check whether the UserForm has been created as expected
    """
    def test_user_form(self):
        """
        Tests whether UserForm is in the correct place, and whether the correct fields have been specified for it.
        """
        self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER}The UserForm class in Rango's forms.py module. Did you create it in the right place?{FAILURE_FOOTER}")

        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}Your UserForm does not match up to the User model. Check your Meta definition of UserForm and try again.{FAILURE_FOOTER}")

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

class RegistrationTests(TestCase):
    """
    A series of tests that examine changes to views that take place in Chapter 9.
    Specifically, we look at tests related to registering a user.
    """
    def test_new_registration_view_exists(self):
        """
        Checks to see if the new registration view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('rango:register')
        except:
            pass

        self.assertEqual(url, '/rango/register/', f"{FAILURE_HEADER}Have you created the rango:register URL mapping correctly? It should point to the new register() view, and have a URL of '/rango/register/' Remember the first part of the URL (/rango/) is handled by the project's urls.py module, and the second part (register/) is handled by the Rango app's urls.py module.{FAILURE_FOOTER}")

    def test_registration_template(self):
        """
        Does the register.html template exist in the correct place?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        template_path = os.path.join(template_base_path, 'register.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'register.html' template in the 'templates/rango/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        # Rate My Professor: Registration
        full_title_pattern = r'<h1>(\s*|\n*)Rate My Professor(\s*|\n*):(\s*|\n*)Registration(\s*|\n*)</h1>'
        request = self.client.get(reverse('rango:register'))
        content = request.content.decode('utf-8')

        print('full_title_pattern: ' + str(full_title_pattern))
        print('content: ' + str(content))
        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'rango:register' is not correct. Check your register.html template, and try again.{FAILURE_FOOTER}")

    def test_registration_get_response(self):
        """
        Checks the GET response of the registration view.
        There should be a form with the correct markup.
        """
        request = self.client.get(reverse('rango:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<h1>Rate My Professor: Registration</h1>' in content, f"{FAILURE_HEADER}The '<h1>Rate My Professor: Registration</h1>' header tag could not be found in your register template.{FAILURE_FOOTER}")

    def test_bad_registration_post_response(self):
        """
        Checks the POST response of the registration view.
        """
        request = self.client.post(reverse('rango:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)

    def test_working_created_form(self):
        """
        Tests form functionality by creating a UserProfileForm and UserForm.
        If saved correctly, login should be possible with supplied info.
        """
        user_data = {'username': 'glasgowStudent', 'password': 'UofG1451', 'email': 'test@student.gla.ac.uk'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}Invalid UserForm even after entering the required data.{FAILURE_FOOTER}")
        self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}Invlaid UserProfileForm even after entering the required data.{FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()

        user_profile_object = user_profile_form.save(commit=False)
        user_profile_object.user = user_object
        user_profile_object.save()

        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}A User object should have been, but wasn't, created.{FAILURE_FOOTER}")
        self.assertEqual(len(rango.models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER}A  UserProfile object should have been, but wasn't, created.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='glasgowStudent', password='UofG1451'), f"{FAILURE_HEADER}Sample user login was unsuccessful during testing.{FAILURE_FOOTER}")

    def test_post_response_registration_success(self):
        """
        Checks the registration view POST response.
        """
        post_data = {'username': 'glasgowStudent', 'password': 'UofG1451', 'email': 'test@student.gla.ac.uk'}
        request = self.client.post(reverse('rango:register'), post_data)
        content = request.content.decode('utf-8')

        self.assertTrue(self.client.login(username='glasgowStudent', password='UofG1451'), f"{FAILURE_HEADER}Sample user login was unsuccessful during testing.{FAILURE_FOOTER}")

class LoginTests(TestCase):
    """
    Test login functionality.
    """
    def test_login_url_exists(self):
        """
        Login view existence check.
        """
        url = ''

        try:
            url = reverse('rango:login')
        except:
            pass

        self.assertEqual(url, '/rango/login/', f"{FAILURE_HEADER}Login page not linked correctly.{FAILURE_FOOTER}")

    def test_login_functionality(self):
        """
        Login functionality test.
        """
        user_object = create_user_object()
        response = self.client.post(reverse('rango:login'), {'username': 'Student', 'password': 'UofG1451'})

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Incorrect user logged in.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}Unable to login the correct user.{FAILURE_FOOTER}")


class LogoutTests(TestCase):
    """
    Test logging out functionality.
    """
    def test_bad_request(self):
        """
        Log out a user who is not logged in.
        """
        response = self.client.get(reverse('rango:logout'))
        self.assertTrue(response.status_code, 302)

    def test_good_request(self):
        """
        Log out a user who IS logged in.
        """
        user_object = create_user_object()
        self.client.login(username='Student', password='UofG1451')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Incorrect user logged in.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}Failed to log user in.{FAILURE_FOOTER}")
