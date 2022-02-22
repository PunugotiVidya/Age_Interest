from django import forms
from .models import InterestStorageModel


class DateInput(forms.DateInput):
    input_type = 'date'


class StorageCreationForm(forms.ModelForm):
    startDate = forms.DateField(widget=DateInput)

    class Meta:
        model = InterestStorageModel
        fields = ['takenPerson', 'startDate','amount', 'rate']
