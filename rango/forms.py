# could put in models.py -> but tidier
from django import forms
from rango.models import Page, Category

# hidden - HTTP stateless protocol (certain parts of web apps difficult to implement)
# -> pass important infor to client in a HTML form
# sent back to originating server when user submits

# csrf token required by django framework

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # set to 0 to avoid not null error
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False) # model populates
    
    # provide additional info on form
    # -> inline class
    class Meta:
        # provide association between ModelForm and a model
        model = Category
        fields = ('name',)
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    # max len supplied identical to to max len in underlying data models
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    # override
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # if not empty and doesn't start with http://
        # prepend
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
            
        return cleaned_data
            
    
    class Meta:
        model = Page
        
        # what fields to include?
        # do not need every field in the model present
        # null vals?
        # here, hide foreign key
        exclude = ('category',)
        # or specify the fields to include
        
        
        
    
    