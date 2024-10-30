from django import forms
from .models import SerialKey, Subscription

class SerialKeyForm(forms.ModelForm):
    class Meta:
        model = SerialKey
        fields = []  # No fields since SerialKey is auto-generated


class SubscriptionForm(forms.ModelForm):
    serial_key = forms.CharField(max_length=100)  # Change this to CharField

    class Meta:
        model = Subscription
        fields = ['start_date', 'end_date']
