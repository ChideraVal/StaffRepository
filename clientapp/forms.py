from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Loan, Staff, StaffFile
from django import forms

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields["username"].widget.attrs['autocomplete'] = 'off'


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields["username"].widget.attrs['autocomplete'] = 'off'
        self.fields["first_name"].widget.attrs['autocomplete'] = 'off'
        self.fields["last_name"].widget.attrs['autocomplete'] = 'off'
        self.fields["email"].widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'})
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # self.fields["username"].widget.attrs['autocomplete'] = 'off'
    
    # class Meta:
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'email']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        exclude = ['owner', 'approval_status', 'payment_status', 'create_time']
    
    def save(self, owner, commit = False):
        self.instance.owner = owner
        self.instance.save()
        return super().save(commit)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['created_at', 'updated_at']
    
    def clean_profile_picture(self):
        if not self.cleaned_data['profile_picture']:
           raise forms.ValidationError('Staff profile picture is required.')
        return self.cleaned_data['profile_picture']


class EditStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['created_at', 'updated_at']
    
    def clean_profile_picture(self):
        if not self.cleaned_data['profile_picture']:
           raise forms.ValidationError('Staff profile picture is required.')
        return self.cleaned_data['profile_picture']
    

class StaffFileForm(forms.ModelForm):
    class Meta:
        model = StaffFile
        exclude = ['staff', 'uploaded_at']
    
    def clean_file(self):
        if not self.cleaned_data['file']:
           raise forms.ValidationError('Staff file is required.')
        return self.cleaned_data['file']

    def save(self, staff, commit = False):
        self.instance.staff = staff
        self.instance.save()
        return super().save(commit)


class EditStaffFileForm(forms.ModelForm):
    class Meta:
        model = StaffFile
        exclude = ['staff', 'uploaded_at']
    
    def clean_file(self):
        if not self.cleaned_data['file']:
           raise forms.ValidationError('Staff file is required.')
        return self.cleaned_data['file']
