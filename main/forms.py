from django import forms

from django import forms
from .models import Faculty, Programme, Application, CustomUser


class ApplicationCreate(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'programme',
            'faculty',
            'passport_serial',
            'passport',
            'diploma_transcript',
            'diploma_copy',
            'image',
            'certificate'
        ]




class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'birthdate',
            'phone_number',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_birth_date(self):
        birthdate = self.cleaned_data['birthdate']
        return birthdate.strftime('%Y-%m-%d')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # 👈 Muhim qadam
        if commit:
            user.save()
        return user

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['passport_serial', 'status', 'programme', 'faculty']  # O'zingizga kerakli maydonlarni qo'shing
