from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """Formulario para enviar mensajes en un chat"""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu mensaje...',
                'required': True
            }),
        }
        labels = {
            'content': ''
        }
