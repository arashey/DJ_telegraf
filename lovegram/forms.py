from django import forms
from .models import Chat, Message
from .models import Profile
from lovegram.models import User  # مدل سفارشی شما



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }


class ChatForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)


    class Meta:
        model = Chat
        fields = ['name', 'participants']  # در صورتی که فیلد دیگری دارید، آن را نیز اضافه کنید

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text','file']  
