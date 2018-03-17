from django import forms
from ..user_app.models import User
from .models import Message, Comment

class CreateMessageForm(forms.Form):
    content=forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder':'Write a message!'}), label='')

class CreateMessage_Form(forms.ModelForm):
    class Meta: 
        model=Message
        fields=['content','author','receiver']
    def clean(self):
        cleaned_data=super(CreateMessage_Form, self).clean()
        return cleaned_data      

class CreateCommentForm(forms.Form):
    content = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder':'Write a comment!'}), label='')

class CreateComment_Form(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content', 'author', 'message']
    def clean(self):
        cleaned_data = super(CreateComment_Form, self).clean()
        return cleaned_data
        