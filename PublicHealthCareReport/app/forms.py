from django import forms
from .models import *

class Online_Appointment(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'document', )

