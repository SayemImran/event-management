from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import Group, Permission
from django import forms
import re
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
           'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                 'text-white placeholder-purple-300 backdrop-blur-md '
                 'focus:ring-2 focus:ring-purple-500 focus:outline-none',
        'placeholder': 'password'
        }),
        label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                 'text-white placeholder-purple-300 backdrop-blur-md '
                 'focus:ring-2 focus:ring-purple-500 focus:outline-none',
        'placeholder': 'confirm password'
        }),
        label="Confirm Password"
    )
    input_class = (
                'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                'text-white placeholder-purple-300 backdrop-blur-md '
                'focus:ring-2 focus:ring-purple-500 focus:outline-none'
        )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                 'text-white placeholder-purple-300 backdrop-blur-md '
                 'focus:ring-2 focus:ring-purple-500 focus:outline-none',
             'placeholder': 'username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                 'text-white placeholder-purple-300 backdrop-blur-md '
                 'focus:ring-2 focus:ring-purple-500 focus:outline-none',
            'placeholder': 'first name'
            }),
            'last_name': forms.TextInput(attrs={
               'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                 'text-white placeholder-purple-300 backdrop-blur-md '
                 'focus:ring-2 focus:ring-purple-500 focus:outline-none',
            'placeholder': 'last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                 'text-white placeholder-purple-300 backdrop-blur-md '
                 'focus:ring-2 focus:ring-purple-500 focus:outline-none',
            'placeholder': 'email'
            }),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        
        if email_exists:
            raise forms.ValidationError("Email Already Exists")
        return email    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")

        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*]', password):
            errors.append("Password must contain at least one special character (!@#$%^&*)")

        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Pasword did not matched")
        
        return cleaned_data
    
    def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data['password'])  # hash password
       if commit:
           user.save()
       return user


class LoginForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        input_class = (
                'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                'text-white placeholder-purple-300 backdrop-blur-md '
                'focus:ring-2 focus:ring-purple-500 focus:outline-none'
        )

        # Add classes to username
        self.fields['username'].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter Username",
        })

        # Add classes to password
        self.fields['password'].widget.attrs.update({
            "class": input_class,
            "placeholder": "Enter Password",
        })


class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role" 
    )
    
class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required=False,
        label = 'Assign permission'
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            'permissions': forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2"
            }),
        }
        labels = {
            'permissions': 'Assign Permissions'
        }


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['profile_image', 'phone_number', 'email', 'first_name', 'last_name']
#         widgets = {
#             'phone_number': forms.TextInput(attrs={
#                 'class': 'text-white w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40 focus:outline-none focus:ring-2 focus:ring-purple-500'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'text-white w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40 focus:outline-none focus:ring-2 focus:ring-purple-500'
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'class': 'text-white w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'text-white w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40'
#             }),
#         }
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'phone_number', 'email', 'first_name', 'last_name']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                        'class': 'w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40'
                          'focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-200',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40'
                          'focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-200',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40 text-gray-200'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg bg-black/40 border border-purple-500/40 text-gray-200'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'text-gray-200'
            }),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Common neon classes for all fields
        neon_class = (
            "w-full px-4 py-2 rounded-lg border-2 border-purple-600 "
            "bg-black/30 text-purple-100 placeholder-purple-400 "
            "focus:outline-none focus:border-purple-400 focus:ring-2 "
            "focus:ring-purple-500/50 transition-all duration-300"
        )

        # Apply to each field
        self.fields['old_password'].widget.attrs.update({
            "class": neon_class,
            "placeholder": "Current Password"
        })
        self.fields['new_password1'].widget.attrs.update({
            "class": neon_class,
            "placeholder": "New Password"
        })
        self.fields['new_password2'].widget.attrs.update({
            "class": neon_class,
            "placeholder": "Confirm New Password"
        })

class CustomPasswordResetForm(PasswordResetForm):
    pass
class CustomPasswordResetConfirmForm(SetPasswordForm):
    pass