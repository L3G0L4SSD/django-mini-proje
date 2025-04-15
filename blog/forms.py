from django import forms
from django.contrib.auth.models import User



class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")

    class Meta:
        model=User
        fields ={"username","email"}

    def clean(self):
        cleaned_data =super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2","Passwords do not match! ")  

        return cleaned_data

class KullaniciProfiliGuncelleForm(forms.ModelForm):
    class Meta:
        model= User
        fields=  ['first_name', 'last_name', 'email'] #sadece bu alanlar görünecek