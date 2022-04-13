from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    company_name = forms.CharField(label="Company Name", required=False)
    email = forms.CharField(
        label="Email", widget=forms.EmailInput(attrs={"class": "email"})
    )
    message = forms.CharField(
        label="Please tell us which of our services you would like to learn more about",
        widget=forms.Textarea(attrs={"class": "message"}),
    )
    captcha = ReCaptchaField(label="Protected by reCAPTCHA v3", widget=ReCaptchaV3)
