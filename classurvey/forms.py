from django import forms
from .models import SoundAnswer, UserDetailsModel, ClassChoice


class SoundAnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        test_choices = ClassChoice.objects.values_list('class_key', 'class_name')
        self.fields['chosen_class'].widget = forms.RadioSelect(choices=tuple(test_choices))

    class Meta:
        model = SoundAnswer
        fields = ('chosen_class', 'confidence','comment')
        labels = {
            'chosen_class': 'Which is the most suitable category for this sound?',
            'confidence': 'How confident are you about your answer?',
            'comment': 'Anything to add?'
        }
        widgets = {
            'confidence': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'class': 'textarea-comment'}),
        }


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = UserDetailsModel
        fields = ('user_name',)
        labels = {
            'user_name': 'Username:'
        }
        widgets = {
            'user_name': forms.Textarea(attrs={'class': 'textarea-username'}),
        }
