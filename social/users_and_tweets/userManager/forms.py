from django import forms
from .models import SimpleUser
class UserSignUP(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserSignUP, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['favorites'].required = False

    class Meta:
        model = SimpleUser

        fields = [
            'userName',
            'password',
            'email',
            'favorites',

        ]
        widgets = {
            'userName' :    forms.Textarea(attrs={'cols': 20, 'rows': 1, 'style':'resize:none;'}),
            'password' :     forms.Textarea(attrs={'cols': 20, 'rows': 1, 'style':'resize:none;'}),
            'email'    :    forms.Textarea(attrs={'cols': 20, 'rows': 1, 'style':'resize:none;'}),
            'favorites':    forms.Textarea(attrs={'cols': 20, 'rows': 1, 'style':'resize:none;'}),
        }
