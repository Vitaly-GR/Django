
from django.forms import ModelForm, EmailField, CharField, PasswordInput, ModelChoiceField, HiddenInput
from django.forms import Form, inlineformset_factory
from .models import Bb, AdvUser, SuperCategory, SubRubric, AdditionalImage
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': HiddenInput, 'contacts': HiddenInput}
        exclude = ('slug',)


AiFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


class ChangeUserInfo(ModelForm):
    email = EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


class RegisterUserForm(ModelForm):
    email = EmailField(required=True, label='Адрес электронной почты')
    password1 = CharField(label='Пароль', widget=PasswordInput,
                          help_text=password_validation.password_validators_help_text_html())
    password2 = CharField(label='Пароль(повторно)', widget=PasswordInput,
                          help_text='Введите пароль еще раз')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
            return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')


class SubRubricForm(ModelForm):
    super_category = ModelChoiceField(queryset=SuperCategory.objects.all(), empty_label=None,
                                      label='Надкатегория', required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(Form):
    keyword = CharField(required=False, max_length=40, label='')
