from django import forms
from .models import Newsletter
class SubscriberForm(forms.Form):
    email = forms.EmailField(label='Your email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

class NewsForm(forms.ModelForm):
    class Meta:
        model =Newsletter
        fields="__all__"
