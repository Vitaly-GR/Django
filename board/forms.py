from django.forms import ModelForm, EmailField
from .models import Bb, AdvUser

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'category')


class ChangeUserInfo(ModelForm):
    email = EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
