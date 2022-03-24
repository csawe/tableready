from django import forms
from .models import Waitlist, Message

class WaitlistModelForm(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = ['estimated_wait_time_given', 'party_name', 'size', 'phone', 'note']

class MessageModelForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_text']