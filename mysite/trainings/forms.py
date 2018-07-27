from django import forms
from .models import Topic,Post,Comments,Feedback
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS

class NewTopicForm(forms.ModelForm):
    name = forms.CharField(required=True,)

    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        if Topic.objects.filter(name=name).exists():
            raise forms.ValidationError('Topic already exists')
        return cleaned_data

    class Meta:
        model = Topic
        fields =['name',]

class NewPostForm(forms.ModelForm):
    
    title =forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1,
                'placeholder': 'Please add the title of your training.'}
        ),)

    description =forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Please add description of your training.'}
        ),)

    class Meta:
        model = Post
        fields =['title','description','pdf_file',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields =['message']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields =['feedback']