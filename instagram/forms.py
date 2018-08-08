from .models import Article, Profile
from django import forms


class NewsLetterForm(forms.Form):
    your_name=forms.CharField(label='First Name',max_length=30)
    email=forms.EmailField(label='Email')

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['editor', 'pub_date']
        widgets = {
            # 'tags': forms.CheckboxSelectMultiple(),
        }


class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
