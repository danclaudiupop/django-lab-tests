from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest
from django_nose.tools import assert_equals, assert_contains


class LoginTest(WebTest):

    def setUp(self):
        User.objects.create_user(
            username='danu',
            password='test123',
        )

    def testLogin(self):
        response = self.app.get('/', user='foo')
        assert_equals('200 OK', response.status)
        assert_contains(response, 'Welcome foo :]', count=1, status_code=200)

    def testLoginProcess(self):
        login = self.app.get(reverse('auth_login'))
        login.form['username'] = 'danu'
        login.form['password'] = 'test123'
        response = login.form.submit('Log in').follow()
        assert_equals('200 OK', response.status)
        assert_contains(response, 'Welcome danu :]', count=1, status_code=200)

    def testLoginWithInvalidCredentials(self):
        login = self.app.get(reverse('auth_login'))
        login.form['username'] = 'foo'
        login.form['password'] = 'bar'
        response = login.form.submit('Log in')
        assert_contains(
            response,
            'Please enter a correct username and password. '
            'Note that both fields are case-sensitive.',
            count=1,
            status_code=200
        )

    def testSubmitWithEmptyCredentials(self):
        login = self.app.get(reverse('auth_login'))
        login.form['username'] = ''
        login.form['password'] = ''
        response = login.form.submit('Log in')
        assert_contains(
            response,
            'This field is required.',
            count=2,
            status_code=200
        )
