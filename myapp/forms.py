from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class PricePredictionForm(forms.Form):
    bedrooms = forms.IntegerField(
        label="Bedrooms",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )
    floors = forms.IntegerField(
        label="Floors",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )
    floorno = forms.IntegerField(
        label="FloorNo",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )
    sqft_living = forms.IntegerField(
        label="Sqft Living",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )
    parkings = forms.IntegerField(
        label="ParkSpace",
        min_value=1,
        max_value=4,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )
    bathrooms = forms.IntegerField(
        label="Bathrooms",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )
    balconies = forms.IntegerField(
        label="Balconies",
        min_value=1,
        max_value=4,
        widget=forms.NumberInput(attrs={"class": "custom-input-class"}),
    )


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "signup_inp",
            'type': "text",
            "placeholder": "Username",
            "required": True,
            "id": "username",
            'minlength': 3,
            'maxlength': 20,
        })
        self.fields["email"].widget.attrs.update({
            "class": "signup_inp",
            'type': "email",
            "placeholder": "Email",
            "required": True,
            "id": "email",
        })
        self.fields["password1"].widget.attrs.update({
            "class": "signup_inp",
            'type': "password",
            "placeholder": "Password",
            "required": True,
            "id": "password1",
            'minlength': 8,
            'maxlength': 20,
        })
        self.fields["password2"].widget.attrs.update({
            "class": "signup_inp",
            'type': "password",
            "placeholder": "Confirm Password",
            "required": True,
            "id": "password2",
            'minlength': 8,
            'maxlength': 20,
        })
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
