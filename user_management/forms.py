from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    success_redirect_url = forms.CharField(required=False, widget=forms.HiddenInput)


class RegisterUserForm(forms.Form):
    # username
    username = forms.CharField(label='username', min_length=5, max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput, min_length=5, max_length=25)
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput, min_length=5,
                                       max_length=25)
    email = forms.EmailField(label='email')
    bio = forms.CharField(label='bio', max_length=150, required=False)
    profile_picture = forms.ImageField(label='profile picture', required=False)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            msg = "Passwords don't match!"
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)
