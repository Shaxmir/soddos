from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-comtrol', 'id': 'message-input', 'style': 'width: 96%; margin: 0;'}),
        }
        labels = {
            'message': 'Сообщение',
        }
