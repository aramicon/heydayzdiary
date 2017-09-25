from django import forms
from .models import Location, Person, Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DayEntryForm(forms.Form):
    day_headline = forms.CharField(label='Headline', max_length=200)
    
class ExerciseForm(forms.Form):
    start_time = forms.TimeField(label='FROM')
    end_time = forms.TimeField(label='TO')
    description = forms.CharField(label='Description')
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(ExerciseForm,self).__init__(self,*args,**kwargs)

class MealForm(forms.Form):
    meal_time = forms.TimeField(label='MEAL TIME')
    description = forms.CharField(label='Description')
    calories = forms.IntegerField(label='Calories')
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(ExerciseForm,self).__init__(self,*args,**kwargs)
class TransactionForm(forms.Form):
    transaction_time = forms.TimeField(label='MEAL TIME')
    description = forms.CharField(label='Description')
    amount = forms.IntegerField(label='Calories')
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(ExerciseForm,self).__init__(self,*args,**kwargs)
        
class WorkForm(forms.Form):
    start_time = forms.TimeField(label='FROM')
    end_time = forms.TimeField(label='TO')
    description = forms.CharField(label='Description', max_length=500)
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(WorkForm,self).__init__(self,*args,**kwargs)
        
class StudyForm(forms.Form):
    start_time = forms.TimeField(label='FROM')
    end_time = forms.TimeField(label='TO')
    description = forms.CharField(label='Description', max_length=500)
    
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(StudyForm,self).__init__(self,*args,**kwargs)
        self.fields['group'].queryset = Group.objects.filter(user = self.user)

class DayEntryLocationForm(forms.Form):
    location = forms.ModelChoiceField(Location.objects.all())
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(DayEntryLocationForm,self).__init__(self,*args,**kwargs)

class StudySubjectForm(forms.Form):
    name = forms.CharField(label='Subject Name', max_length=200)
    description = forms.CharField(label='Subject Description')

class LocationForm(forms.Form):
    location_name = forms.CharField(label='Location Name', max_length=200)
   
class DayEntryPersonForm(forms.Form):
    person = forms.ModelChoiceField(Person.objects.all())
    start_time = forms.DateTimeField(label='FROM')
    end_time = forms.DateTimeField(label='TO')
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(DayEntryPersonForm,self).__init__(self,*args,**kwargs)

class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Person Name', max_length=200,widget=forms.TextInput(attrs={'class': "input-lg"}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    description = forms.CharField(label='Person Bio/Description')
    address = forms.CharField(label='Address', max_length=500)
    phone_number_1 = forms.CharField(label='Phone No. (1)', max_length=50)
    phone_number_2 = forms.CharField(label='Phone No. (2)', max_length=50)
    email_1 = forms.CharField(label='Email (1)', max_length=100)
    email_2 = forms.CharField(label='Email (2)', max_length=100)
    website_1 = forms.CharField(label='Website Link (1)', max_length=200)
    website_2 = forms.CharField(label='Website Link (2)', max_length=200)
    social_media_1 = forms.CharField(label='Social Media Link (1)', max_length=200)
    social_media_2 = forms.CharField(label='Social Media Link (2)', max_length=200)
    social_media_3 = forms.CharField(label='Social Media Link (3)', max_length=200)
    social_media_4 = forms.CharField(label='Social Media Link (4)', max_length=200)
    
class DayEntryProjectForm(forms.Form):
    project = forms.ModelChoiceField(Project.objects.all())
    start_time = forms.DateTimeField(label='FROM')
    end_time = forms.DateTimeField(label='TO')
    description = forms.CharField(label='Project Work Description')
    
    def __init__(self,*args,**kwargs):
        self.fields["day_entry_id"] = forms.CharField(widget=forms.HiddenInput())
        super(DayEntryPersonForm,self).__init__(self,*args,**kwargs)

class ProjectForm(forms.ModelForm):
    name = forms.CharField(label='Person Name', max_length=200,widget=forms.TextInput(attrs={'class': "input-lg"}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    description = forms.CharField(label='Project Description')
    
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user