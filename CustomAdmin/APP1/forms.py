import pickle
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.utils.translation import gettext_lazy,gettext as _
from django.contrib.auth.models import User
from django.db.models import Q
from APP1.models import *
from APP1.widgets import *
from django.contrib.auth import (authenticate,get_user_model)
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import *
from APP1.widgets import *

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']



class AdminAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control',"placeholder":"Email/Username"},))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control',"placeholder":"Enter Password"},))
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            try:
                user=User.objects.filter(Q(username=username) | Q(email=username)).get()
                username=user.username
                print(user)
            except User.DoesNotExist:
                username=username

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


#Toggle Widget 
#Referenece
#https://blog.ihfazh.com/django-custom-widget-with-3-examples.html

class CustomWidgetForm(forms.Form):

    bio = forms.CharField()
    togglewidget = forms.BooleanField(required=False)
    countablewidget=forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CustomWidgetForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget=widgets.Textarea()
        self.fields['togglewidget'].widget = ToggleWidget(options={'on': 'Yep','off': 'Nope'})
        self.fields['countablewidget'].widget = CountableWidget(attrs={'data-max-count': 160,
                                                                        'data-count': 'characters',
                                                                        'data-count-direction': 'down'})



from django import forms
from django.contrib.auth.models import User


class MyWidgets(forms.Form):
    name=forms.CharField(label=_("Enter your Name"))
    def __init__(self, *args, **kwargs):
        super(MyWidgets, self).__init__(*args, **kwargs)
        self.fields['name'].widget = CountableWidget(attrs={'data-max-count': 160,
                                                                        'data-count': 'characters',
                                                                        'data-count-direction': 'down'})
        self.fields['name'].help_text = "Type up to 160 characters"
        self.helper = FormHelper()
























from datetime import date
from django import forms

class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2018, 2019, 2020]]
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)






class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput()]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        print("value is",value )
        if value:
            return pickle.loads(value)
        else:
            return ['', '']


class MultiExampleField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=31),
                       forms.fields.CharField(max_length=31)]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        ## compress list to single object                                               
        ## eg. date() >> u'31/12/2012'                                                  
        print("YOO",pickle.dumps(values))
        return pickle.dumps(values)


class FormForm(forms.Form):
    # a = forms.BooleanField()
    # b = forms.CharField(max_length=32)
    # c = forms.CharField(max_length=32, widget=forms.widgets.Textarea())
    # d = forms.CharField(max_length=32, widget=forms.widgets.SplitDateTimeWidget())
    e = forms.CharField(max_length=32)
    #f = MultiExampleField()
    g = forms.BooleanField(
        # required must be false, otherwise you will get error when the toggle is off
        # at least in chrome
        required=False,
        widget=ToggleWidget(
            options={
                'on': 'Yep',
                'off': 'Nope'
            }
        )
    )
    def __init__(self, *args, **kwargs):
        super(FormForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget =MultiWidgetBasic(attrs={'data-max-count': 160,
                                                                        'data-count': 'characters',
                                                                        'data-count-direction': 'down'})
        self.fields['shanmukh'].help_text = "Type up to 160 characters"
        self.helper = FormHelper()