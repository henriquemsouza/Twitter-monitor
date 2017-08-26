from django import forms

class SentimentoForm(forms.Form):
    qualidade = forms.ChoiceField(widget=forms.RadioSelect())
