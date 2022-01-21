import os
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase


class TryDjangoConfigTest(TestCase):
    def test_secret_key_strength(self):
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        
        try:
            validate_password(SECRET_KEY)
        except Exception as e:
            message = 'Bad secret key: {}'.format(e.messages)
            self.fail(message)