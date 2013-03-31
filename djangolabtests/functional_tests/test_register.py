import re
import datetime

from django import forms
from django.core import mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest
from django_nose.tools import assert_contains


class RegisterTest(WebTest):

    fixtures = ['users']

    def testRegisterProcess(self):
        register = self.app.get(reverse('registration_register'))
        register.form['username'] = 'danul'
        register.form['email'] = 'danclaudiupop@gmail.com'
        register.form['password1'] = 'test123'
        register.form['password2'] = 'test123'
        response = register.form.submit('Submit').follow()
        assert_contains(
            response,
            'You are now registered. Activation email sent.',
            count=1,
            status_code=200
        )
        activation_url = re.search(
            '/accounts/activate/(.*)',
            mail.outbox[0].body
        ).group(0)
        response = self.app.get(activation_url).follow()
        assert_contains(
            response,
            'Your account is now activated.',
            count=1,
            status_code=200
        )

    def testActivationExpired(self):
        register = self.app.get(reverse('registration_register'))
        register.form['username'] = 'danul'
        register.form['email'] = 'danclaudiupop@gmail.com'
        register.form['password1'] = 'test123'
        register.form['password2'] = 'test123'
        response = register.form.submit('Submit').follow()
        user = User.objects.get(username='danul')
        user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS
        )
        user.save()
        activation_url = re.search(
            '/accounts/activate/(.*)',
            mail.outbox[0].body
        ).group(0)
        response = self.app.get(activation_url)
        assert_contains(
            response,
            'Account activation failed',
            count=1,
            status_code=200
        )

    def testUserAlreadyExists(self):
        register = self.app.get(reverse('registration_register'))
        register.form['username'] = 'danu'
        register.form['email'] = 'foo@example.com'
        register.form['password1'] = 'test123'
        register.form['password2'] = 'test123'
        response = register.form.submit('Submit')
        assert_contains(
            response,
            'A user with that username already exists.',
            count=1,
            status_code=200
        )

    def testMismatchedPasswords(self):
        invalid_data = [
            {
                'data': {'username': 'test',
                         'email': 'foo@example.com',
                         'password1': 'test123',
                         'password2': 'test321'},
                'error': "The two password fields didn&#39;t match."
            },
        ]
        register = self.app.get(reverse('registration_register'))
        for i in invalid_data:
            register.form['username'] = i['data']['username']
            register.form['email'] = i['data']['email']
            register.form['password1'] = i['data']['password1']
            register.form['password2'] = i['data']['password2']
            response = register.form.submit('Submit')

            assert_contains(
                response,
                i['error'],
                count=1,
                status_code=200
            )

    def testEmailFieldValidation(self):
        register = self.app.get(reverse('registration_register'))
        register.form['username'] = 'danu'
        register.form['email'] = 'abc'
        register.form['password1'] = 'test123'
        register.form['password2'] = 'test123'
        response = register.form.submit('Submit')
        self.assertFieldOutput(
            forms.EmailField,
            {'dan@dan.com': 'dan@dan.com'},
            {'abc': [u'Enter a valid e-mail address.']}
        )
        assert_contains(
            response,
            'Enter a valid e-mail address.',
            count=1,
            status_code=200
        )
