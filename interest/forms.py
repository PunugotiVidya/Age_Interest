from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class InterestForm(forms.Form):
    amount = forms.IntegerField()
    rate = forms.FloatField()

    Start_Date = forms.DateField(widget=DateInput)
    Current_Date = forms.DateField(widget=DateInput)
