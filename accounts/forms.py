from django import forms
from django.db import transaction

from . import models as mdl


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model   = mdl.User
        fields  = ('email','full_name','password')
        widgets = {
            'email':forms.EmailInput(attrs={
                'class':'form-control','placeholder':'Email Address...',
                'required':True,'autofocus':True
            }),
            'full_name':forms.TextInput(attrs={
                'class':'form-control','required':True,
                'placeholder':'Full Name ...',
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control','placeholder':'Required Password...',
                'required':True,
            }),
            # 'password2':forms.PasswordInput(attrs={
                # 'class':'form-control','placeholder':'Confirm Password required ...',
                # 'required':True,
            # })
        }
    
    @transaction.atomic
    def save(self, commit: bool = False):
        user            = super().save(commit)
        user.username   =  self.cleaned_data.get('email')
        user.full_name  = self.cleaned_data.get('full_name')
        user.password  = self.cleaned_data.get('password')
        # user.password1  = self.cleaned_data.get('password1')
        user.staff      = True
        user.save(commit=True)
        return user


class UserLoginForm(forms.Form):
    email       = forms.EmailField(max_length=255,label='Email',required=True,
                widget=forms.EmailInput(attrs={
                'class':'form-control','placeholder':'Email Address...','autofocus':True,
            })    
        )

    password       = forms.CharField(max_length=255,label='Password',required=True,
                widget=forms.PasswordInput(attrs={
                    'class':'form-control','placeholder':'Password here ..'
                })
            )

class UserProfileForm(forms.ModelForm):
    '''
    @ users are allow to update their profile here
    '''
    class Meta:
        model = mdl.UserProfile
        fields = ('user','profile_pic')
        widgets = {
            'user':forms.TextInput(attrs={
                'class':'form-control','required':True,
            }),
            'profile_pic':forms.ClearableFileInput(attrs={
                'class':'form-control','required':False,
            })
        }
