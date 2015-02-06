from django.db import models
from django import forms
# from mongoengine import *

choice = (
    ('ward','wardrobe'),
    ('sofa','sofa'),
    ('chair','chair'),
    ('entertainment','entertainment unit'),
    ('dining','dining table'),
    ('children','children room'),
    ('bed','bed room'),
    ('all','all')
)

class CustomerDetails(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField()
    floor_plan = forms.FileField(required=False)
    address = forms.CharField()
    style = forms.CharField(required=False)
    require = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple,choices = choice)
    others = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}),required=False)


class Details(models.Model):
    name = models.CharField()
    address = models.CharField()
    mail_id = models.EmailField()
    phone = models.CharField()
    requirements = models.CharField()
    floor = models.FileField(upload_to='user_uploads/')
