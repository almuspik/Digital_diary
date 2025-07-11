from django import forms
from .models import DiaryEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'entry_date']
        widgets = {'entry_date': forms.DateInput(attrs={'type': 'date'})}

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))   
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'phone_number', 'email', 'date_of_birth']


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'       
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'
