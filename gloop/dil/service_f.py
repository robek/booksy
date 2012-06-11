from django import forms

class ServiceForm(forms.Form):
    service_action = forms.CharField(max_length=40, widget=forms.HiddenInput, initial='new')
    service_name = forms.CharField(max_length=30)
    service_prize = forms.CharField(max_length=10)
    service_duration = forms.CharField(max_length=10)
