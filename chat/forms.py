from django import forms
from .models import ChatRoom

class ChatRoomCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ChatRoom
        fields = ('name','password')

class ChatRoomJoinForm(forms.Form):
    name     = forms.CharField(max_length=50, label="방 이름")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
