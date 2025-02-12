from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from .models import Record

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import Assignment

#register/create a user

class CreateUserForm(UserCreationForm):
    
    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']

#login users


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Create a record

class CreateRecordForm(forms.ModelForm):

    class Meta:

        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country']


# - Update a record

class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country']



class AdminLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Accepts YYYY-MM-DD
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'attachment']  

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['attachment'].required = False  # Make file upload optional


