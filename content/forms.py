from django import forms
from content.models import News, Project, Tag

class NewsMonitorUpdateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title','categories','projects','expert_level','tags','status','sentiment']
        widgets = {'sentiment': forms.HiddenInput(),
                   'categories': forms.SelectMultiple(attrs={'hidden': ''}),
                   'expert_level': forms.Select(attrs={'hidden': ''})}


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','symbol','description','homepage','status']