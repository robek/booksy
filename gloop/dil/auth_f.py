from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms

attrs_dict = { 'class': 'required' }

class CompanyRegistrationForm(forms.Form):
    is_company = forms.CharField(max_length=5, widget=forms.HiddenInput, initial='true')
    company_username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=20,
                                label=("Username"),
                                error_messages={'invalid': ("This value must contain only letters, numbers and underscores.")})
    company_password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=("Password"))    

    company_password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=("Password (again)"))    

    company_name=forms.CharField(max_length=50)

    def clean_company_username(self):
        """Checks that the username is not in use."""
        try:
            User.objects.get(username__iexact=self.cleaned_data['company_username'])
        except User.DoesNotExist:
            return self.cleaned_data['company_username']
        raise forms.ValidationError(("A username already in use."))


    def clean(self):
        """Check passwords fields. Error will be in 'non_field_errors()'"""
        # If both forms filled
        if 'company_password1' in self.cleaned_data and 'company_password2' in self.cleaned_data:
            if self.cleaned_data['company_password1'] != self.cleaned_data['company_password2']:
                raise forms.ValidationError("Passwords fields do not match.")
        return self.cleaned_data


class ClientRegistrationForm(forms.Form):
    is_client = forms.CharField(max_length=5, widget=forms.HiddenInput, initial='false')
    client_username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=20,
                                label=("Username"),
                                error_messages={'invalid': ("This value must contain only letters, numbers and underscores.")})
    client_password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=("Password"))    

    client_password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=("Password (again)"))    

    client_email=forms.CharField(max_length=50)

    def clean_client_username(self):
        """Checks that the username is not in use."""
        try:
            User.objects.get(username__iexact=self.cleaned_data['client_username'])
        except User.DoesNotExist:
            return self.cleaned_data['client_username']
        raise forms.ValidationError(("A username already in use."))


    def clean(self):
        """Check passwords fields. Error will be in 'non_field_errors()'"""
        # If both forms filled
        if 'client_password1' in self.cleaned_data and 'client_password2' in self.cleaned_data:
            if self.cleaned_data['client_password1'] != self.cleaned_data['client_password2']:
                raise forms.ValidationError("Passwords fields do not match.")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=20,
                                label=("Username"),
                                error_messages={'invalid': ("This value must contain only letters, numbers and underscores.")})

    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=("Password"))

    def clean_username(self):
        """Check that the username is in db."""
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            raise forms.ValidationError(("A username not in use."))
        return self.cleaned_data['username']

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("The provided username and password do not match.")
        return self.cleaned_data

