from django.forms import ModelForm
from django import forms
from .models import Station
from .models import Feedback

class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ["station_name"]

class FeedbackForm(ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.Select()
    )
    class Meta:
        model = Feedback
        fields = ["message","rating"]