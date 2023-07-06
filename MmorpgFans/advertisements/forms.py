from django.forms import ModelForm
from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget #, SummernoteInplaceWidget

from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm #, PasswordField


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ['author', 'title', 'text', 'category']
        widgets = {
                    'text': SummernoteWidget(), # с рамкой
                    # 'text': SummernoteInplaceWidget(), # без рамки
                }
        labels = ['автор','заголовок','текст','категория']


class RespondForm(ModelForm):
    class Meta:
        model = Respond
        fields = ['text']


# class RespondForm(forms.Form):
#     text = forms.CharField(label="Отклик на объявление")
#     def clean_text(self):
#         self.clean()
#         # data = self.cleaned_data["text"]
#         # data = self.cleaned_data.get("text")
#         return self.text
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


class LoginForm2(LoginForm):

    error_messages = {
        "account_inactive": ("В настоящее время аккаунт неактивен."),
        "email_password_mismatch": (
            "Введенный e-mail и/или пароль не верны."
        ),
        "username_password_mismatch": (
            "Имя пользователя и/или пароль введены не верно."
        ),
    }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['login'].label="Логин"
        self.fields['login'].widget.attrs['placeholder']="имя пользователя"

        self.fields['password'].label="Пароль"
        self.fields['password'].widget.attrs['placeholder']="пароль"

        self.fields['remember'].label="Запомнить"



class SignupForm2(SignupForm):

    # error_messages = {
    #     "account_inactive": ("В настоящее время аккаунт неактивен."),
    #     "email_password_mismatch": (
    #         "Введенный e-mail и/или пароль не верны."
    #     ),
    #     "username_password_mismatch": (
    #         "Имя пользователя и/или пароль введены не верно."
    #     ),
    # }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].label="Логин"
        self.fields['username'].widget.attrs['placeholder']="имя пользователя"

        self.fields['email'].label="E-mail"
        self.fields['email'].widget.attrs['placeholder']="адрес e-mail"

        self.fields['password1'].label="Пароль"
        self.fields['password1'].widget.attrs['placeholder']="Пароль"

        self.fields['password2'].label="Пароль (повторите)"
        self.fields['password2'].widget.attrs['placeholder']="Пароль (повторите)"

