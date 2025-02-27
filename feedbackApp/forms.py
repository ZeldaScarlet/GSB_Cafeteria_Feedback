from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Feedback, MealImport

# 📌 Kullanıcı Kayıt Formu
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# 📌 Kullanıcı Giriş Formu
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

# 📌 Geri Bildirim Formu
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["meal", "comment", "rating"]
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "rating": forms.Select(attrs={"class": "form-control"}),
        }

# 📌 Excel Dosyası ile Yemek Yükleme Formu
class MealImportForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = MealImport
        fields = ["file_path"]
