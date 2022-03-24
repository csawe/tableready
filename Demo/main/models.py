from django.db import models

from users.models import NewUser

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Waitlist(models.Model):
    checkin = models.DateTimeField()
    estimated_wait_time_given = models.IntegerField()
    party_name = models.CharField(max_length=20)
    size = models.IntegerField()
    #phone = PhoneField()
    #E164_only=False if numbers are from US only.
    phone = PhoneNumberField(region="US")
    note = models.CharField(max_length=20, null=True, blank=True)
    state = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.party_name

class Message(models.Model):
    message_number = models.IntegerField()
    message_text = models.CharField(max_length=200)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)