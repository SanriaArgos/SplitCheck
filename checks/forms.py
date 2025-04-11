from django import forms
from .models import Receipt, Item, Participant
from django.forms import inlineformset_factory

class ReceiptForm(forms.ModelForm):
    participant1 = forms.CharField(
        label='Участник 1', 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Имя участника'})
    )
    participant2 = forms.CharField(
        label='Участник 2', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Имя участника'})
    )
    participant3 = forms.CharField(
        label='Участник 3', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Имя участника'})
    )
    
    class Meta:
        model = Receipt
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название чека'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

ItemFormSet = inlineformset_factory(
    Receipt, 
    Item, 
    fields=('name', 'price'), 
    extra=3,
    can_delete=False
)