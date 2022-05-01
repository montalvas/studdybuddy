from django import forms
from .models import Room

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('__all__')
        exclude = ['host', 'participants']
        
def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError((f"{value} is taken."),params = {'value':value})
        
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', validators = [validate_email])

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']