from django import forms

from . import models as mdl 

class WasteLocationForm(forms.Form):
    class Meta:
        model   = mdl.WasteLocation
        fields  = ('location',)
        widgets = {
            'location':forms.TextInput(attrs={
                'placeholder': 'Location','class':'form-control','required':True,
                }),
        }

class WasteTypeForm(forms.ModelForm):
    class Meta:
        model   = mdl.WasteType
        fields  = ('title',)
        widgets = {
            'title':forms.TextInput(attrs={
                'placeholder':'Waste Type...','class':'form-control','required':True,
            }),
        }

class DustBinForm(forms.ModelForm):
    class Meta:
        model   = mdl.DustBin
        fields  = ('location','waste_type','bin_label',
                    'digital_address','gps_latitude','gps_longitude',
                    'bin_ready'
                    )
        widgets = {
            'location':forms.Select(attrs={
                'class':'form-control','required':True
            }),
            'waste_type':forms.Select(attrs={
                'class':'form-control','required':True,
            }),
            'bin_label':forms.TextInput(attrs={
                'class':'form-control','required':True,
                'placeholder':'DustBin Label ...'
            }),
            'digital_address':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Digital Address ...',
                'required':True,
            }),
            'gps_latitude':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Digital Address ...',
                'required':True,'readonly':True
            }),
            'gps_longitude':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Digital Address ...',
                'required':True,'readonly':True
            }),
            'bin_ready':forms.CheckboxInput(attrs={
                'class':'form-check-input','placeholder':'Digital Address ...',
                'required':True,
            })
        }

class WasteSettingsForm(forms.ModelForm):
    class Meta:
        model   = mdl.WasteSettings
        fields  = ('location','waste_type','settings_title'
                    ,'dues'
                )
        widgets = {
            'location':forms.Select(attrs={
                'class':'form-control','required':True,
            }),
            'waste_type':forms.Select(attrs={
                'class':'form-control','required':True,
            }),
            'settings_title':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Settings Title...',
                'required':False,
            }),
            'dues':forms.NumberInput(attrs={
                'class':'form-control','placeholder':'Amount Payable...',
                'required':True,
            })
        } 
