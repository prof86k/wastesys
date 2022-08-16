from django import forms

from . import models as mdl


class UserRegistrationForm(forms.ModelForm):
    password1   = forms.CharField(label='Password:',max_length=255,widget=forms.PasswordInput(attrs={
            'class':'form-control','placeholder':'Required Password...',
            'required':True,
    }))
    password2   = forms.CharField(label='Confrim Password:',max_length=255,widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':'Required Password Confirmation...',
        'required':True,
    }))
    class Meta:
        model   = mdl.User
        fields  = ('email','full_name')
        widgets = {
            'email':forms.EmailInput(attrs={
                'class':'form-control','placeholder':'Email Address...',
                'required':True,'autofocus':True
            }),
            'full_name':forms.TextInput(attrs={
                'class':'form-control','required':True,
                'placeholder':'Full Name ...',
            }),
        }
    
    def cleaned_password2(self):
        password1   = self.cleaned_data.get('password1')
        password2   = self.cleaned_data.get('password2')
        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError('Passwords Do not match')
        return password2
    
    def save(self):
        user            = super(UserRegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))
        user.staff      = True
        user.save()
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
