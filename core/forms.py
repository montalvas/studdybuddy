from django import forms
from .models import Room, User

from django.contrib.auth.forms import UserCreationForm


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('__all__')
        exclude = ['host', 'participants']
        
        
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

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
        fields = ['bio', 'avatar']