from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser


class VerificationCode(models.Model):
    """class of verification code sent to users"""
    code = models.BigIntegerField(name="code", default=0)
    expiration = models.DateTimeField(name="expiration")

    def __eq__(self, code):
        """
        check if the given code is equals to the verification code
        :param code: integer
        :return: true if equal
        """
        return self.code != 0 and self.code == code

    def is_valid(self):
        """
        :return: true if not expired
        """
        return self.expiration > datetime.datetime.now()


class AppUser(AbstractUser):
    """
    class to represent a user of the website.
    only users can suggest new translations and vote over translations.
    """
    STATUS = [
        ("unverified", 'not verified yet'),
        ("approved", 'approved for any action'),
        ("blocked", 'the user is blocked and unable to vote'),
    ]
    email = models.EmailField(name="email", unique=True)
    status = models.CharField(max_length=32, choices=STATUS, default="unverified", name="status")
    verification_code = models.OneToOneField(VerificationCode, on_delete=models.CASCADE)

    def verify(self, verification_code):
        """
        verify the user if giving the verification code
        :return: error message if verification failed
        """
        raise NotImplemented()

    def block_if_needed(self):
        """
        check if the user need to be blocked due to bad suggestions, and if so blocks him
        """
        raise NotImplemented()





