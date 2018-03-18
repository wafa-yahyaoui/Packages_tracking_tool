from django import forms
from django.forms import ModelForm
from ..accounts.models import Store
from models import ContentEmail



class ContentEmailForm(ModelForm):
    """This class represents the Content Email form"""


    class Meta:
        model = ContentEmail
        fields = ['template_email', 'text_body', 'text_footer']
        widgets = {
            'template_email' : forms.Select(attrs={'class':'form-control'}),
            'text_body': forms.Textarea(attrs={'class':'form-control','rows':'3','cols':'5'}),
            'text_footer': forms.Textarea(attrs={'class':'form-control','rows':'3','cols':'5'}),
        }


class ContentEmailForm(ModelForm):
    """This class represents the Content Email form"""

    class Meta:
        model = ContentEmail
        fields = ['template_email', 'text_body', 'text_footer']
        widgets = {

            'template_email': forms.Select(attrs={'class': 'form-control'}),
            'text_body': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '5'}),
            'text_footer': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '5'}),
        }
class ConfigEmailForm(ModelForm):
    """This class represents the Content Email form"""

    class Meta:
        model = Store
        fields = ['font', 'color_menu', 'color_call_to_action', 'allignment', 'size', ]
        widgets = {
            'allignment': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'font': forms.Select(attrs={'class': 'form-control', 'id': 'list_fonts'}),
            'color_call_to_action': forms.TextInput(attrs={'class': 'form-control'}),
            'color_menu': forms.TextInput(attrs={'class': 'form-control'}),
        }
