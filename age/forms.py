from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class AgeForm(forms.Form):
    Born_DOB = forms.DateField(widget=DateInput)
    Today_Date = forms.DateField(widget=DateInput)
