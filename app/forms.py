from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'email','first_name','last_name']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(user.password) # set password properly before commit
        if commit:
            user.save()
        return user  