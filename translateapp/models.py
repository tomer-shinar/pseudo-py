from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
import math
from abc import ABC, abstractmethod
import json

from django.utils import timezone


class VerificationCode(models.Model):
    """class of verification code sent to users"""
    code = models.CharField(max_length=32)
    expiration = models.DateTimeField()

    def is_valid(self):
        """
        :return: true if not expired
        """
        return self.expiration > datetime.datetime.now(tz=timezone.utc)


class AppUser(AbstractUser):
    """
    class to represent a user of the website.
    only users can suggest new translations and vote over translations.
    """
    UNVERIFIED = "unverified"
    APPROVED = "approved"
    BLOCKED = "blocked"
    STATUS = [
        (UNVERIFIED, 'not verified yet'),
        (APPROVED, 'approved for any action'),
        (BLOCKED, 'the user is blocked and unable to vote'),
    ]
    email = models.EmailField(name="email", unique=True)
    status = models.CharField(max_length=32, choices=STATUS, default="unverified", name="status")
    verification_code = models.OneToOneField(VerificationCode, on_delete=models.CASCADE, blank=True)

    def block_if_needed(self):
        """
        check if the user need to be blocked due to bad suggestions, and if so blocks him
        """
        raise NotImplemented()  # todo add user blocking


class AbstractSuggestion(models.Model):
    """
    class for any kind of suggestion
    """
    suggester = models.ForeignKey(AppUser, related_name="suggester", on_delete=models.SET_NULL, null=True)
    up_voters = models.ManyToManyField(AppUser, related_name="up_voters")
    down_voters = models.ManyToManyField(AppUser, related_name="down_voters")

    def rating(self):
        """
        calculate the rating by the number of up votes and down votes
        :return: number from 0 to 1 representing the the part of all votes that are positive
        """
        up_count = len(self.get_up_votes())
        down_count = len(self.get_down_votes())
        return (up_count + 1) / (up_count + down_count + 2)  # the +1 help to centering when there are few votes

    def impact(self):
        """
        calculate how much this sample should impact
        :return: positive integer
        """
        votes = len(self.get_down_votes()) + len(self.get_up_votes())
        return self.rating() * math.log2(votes)

    def to_consider(self):
        """
        determines if to consider this sample based on its rating
        :return: true if should be considered
        """
        return self.rating() >= 0.4

    def get_up_votes(self):
        """
        :return: up votes of approved users
        """
        return self.up_voters.filter(status=AppUser.APPROVED)

    def get_down_votes(self):
        """
        :return: down votes of approved users
        """
        return self.down_voters.filter(status=AppUser.APPROVED)

    @abstractmethod
    def get_sample(self):
        """
        :return: sample for the learning algorithm
        """
        pass

    def do_up_vote(self, voter):
        """
        add voter to up voters
        :param voter: the user voting
        """
        if self.suggester.username == voter.username or self.up_voters.filter(username=voter.username):
            # user suggested or already up voted
            return
        if self.down_voters.filter(username=voter.username):
            # undoing the down voting
            self.down_voters.remove(voter)
        self.up_voters.add(voter)
        self.save()

    def do_down_vote(self, voter):
        """
        add voter to up voters
        :param voter: the user voting
        """
        if self.down_voters.filter(username=voter.username):
            # user already down voted
            return
        if self.up_voters.filter(username=voter.username):
            # undoing the up voting
            self.up_voters.remove(voter)
        self.down_voters.add(voter)
        self.save()


class G2GSuggestion(AbstractSuggestion):
    """
    represent a generic to generic translation suggestion
    """
    gen_pseudo = models.CharField(max_length=200, name="gen_pseudo")
    gen_python = models.CharField(max_length=200, name="gen_python")

    def get_sample(self):
        return self.gen_pseudo, self.gen_python, self.impact()

    def __eq__(self, other):
        return self.gen_pseudo == other.gen_pseudo and self.gen_python == other.gen_python


class PosSuggestion(AbstractSuggestion):
    data = models.CharField(max_length=500)  # json string of list of tuples of strings

    def get_sample(self):
        return json.loads(self.data), self.impact()







