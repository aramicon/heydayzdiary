from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm
import math
import sys


from .models import Day_entry, Exercise, Work, Study, Day_entry_Location, Location, Day_entry_Person, Person, Day_entry_Project, Project, Meal, Transaction, Study_Subject, Job

from heydayzdiary.forms import UserCreationForm, DayEntryForm, ExerciseForm, WorkForm,DayEntryLocationForm, LocationForm, PersonForm, DayEntryPersonForm, ProjectForm, DayEntryProjectForm, MealForm, TransactionForm, StudySubjectForm, StudyForm, JobForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('heydayzdiary:home')
    else:
        form = UserCreationForm()
    return render(request, 'heydayzdiary/signup.html', {'form': form})

class HomeView(generic.TemplateView):
    template_name = 'heydayzdiary/home.html'
       
    def get_queryset(self):
        """Return the most recent 10 day entries."""
        return Day_entry.objects.filter(day_date__lte=timezone.now()).order_by('-day_date')[:10]        
 
class DaysView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/day/days.html'
    context_object_name = 'latest_day_entries'
    
    def get_queryset(self):
        """Return day entries for the logged-in user."""
        return Day_entry.objects.filter(day_date__lte=timezone.now(),user=self.request.user).order_by('-day_date')       
    
class DetailCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    fields=['day_headline','day_main_text','day_date','sleep_duration','sleep_quality','sleep_notes','wake_up_time','weather_sun','weather_rain','weather_wind','weather_temperature','weather_notes']
    template_name = 'heydayzdiary/day/day_entry_add_form.html'
    def form_valid(self, form):
        day = form.save(commit=False)
        day.user = self.request.user   
        return super(DetailCreate, self).form_valid(form)    
    
class DetailUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    form = DayEntryForm
    template_name = 'heydayzdiary/day/day_entry_form.html'
    fields=['day_headline','day_main_text','day_date','sleep_duration','sleep_quality','sleep_notes','wake_up_time','weather_sun','weather_rain','weather_wind','weather_temperature','weather_notes']
    def get_queryset(self):
        base_qs = super(DetailUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)    

class DetailReadFormat(LoginRequiredMixin,DetailView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    template_name = 'heydayzdiary/day/day_entry_readformat_form.html'
    def get_queryset(self):
        base_qs = super(DetailReadFormat, self).get_queryset()
        return base_qs.filter(user=self.request.user)    
    
class DetailDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    success_url = reverse_lazy('heydayzdiary')
    def get_queryset(self):
        base_qs = super(DetailDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    
class ExerciseUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Exercise
    form = ExerciseForm
    template_name = 'heydayzdiary/exercise/exercise_form.html'
    fields=['start_time','end_time','description','exercise_type','web_tracking_system_url','distance','intensity']
    def get_queryset(self):
        base_qs = super(ExerciseUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class ExerciseCreate(LoginRequiredMixin, CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Exercise
    form = ExerciseForm
    template_name = 'heydayzdiary/exercise/exercise_form_add.html'
    fields=['start_time','end_time','description','exercise_type','web_tracking_system_url','distance','intensity']
        
    def form_valid(self, form):
        exercise = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)        
        exercise.day_entry = day_entry
        exercise.user = self.request.user
        return super(ExerciseCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(ExerciseCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class ExerciseDelete(LoginRequiredMixin,DeleteView):
    template_name = 'heydayzdiary/exercise/exercise_confirm_delete.html'
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Exercise       
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(ExerciseDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)
        
class MealUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/meal/meal_form.html'
    model = Meal
    form = MealForm
    fields=['meal_time','description','meal_type','calories']
    def get_queryset(self):
        base_qs = super(MealUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class MealCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Meal
    form = MealForm
    template_name = 'heydayzdiary/meal/meal_form_add.html'
    fields=['meal_time','description','meal_type','calories']
  
    def form_valid(self, form):
        meal = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        meal.day_entry = day_entry
        meal.user = self.request.user
        return super(MealCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(MealCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class MealDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/meal/meal_confirm_delete.html'
    model = Meal    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id}) 
    def get_queryset(self):
        base_qs = super(MealDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)        
        
class TransactionUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Transaction
    form = TransactionForm
    template_name = 'heydayzdiary/transaction/transaction_form.html'
    fields=['transaction_time','description','transaction_type','amount']
    def get_queryset(self):
        base_qs = super(TransactionUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class TransactionCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Transaction
    form = TransactionForm
    template_name = 'heydayzdiary/transaction/transaction_form_add.html'
    fields=['transaction_time','description','transaction_type','amount']
  
    def form_valid(self, form):
        transaction = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        transaction.day_entry = day_entry
        transaction.user = self.request.user
        return super(TransactionCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(TransactionCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class TransactionDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Transaction    
    template_name = 'heydayzdiary/transaction/transaction_confirm_delete.html'
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})   
    def get_queryset(self):
        base_qs = super(TransactionDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)        
        
class WorkUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Work
    form = WorkForm
    template_name = 'heydayzdiary/work/work_form.html'
    fields=['job','start_time','end_time','description']
    def get_queryset(self):
        base_qs = super(WorkUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class WorkCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Work
    form = WorkForm
    template_name = 'heydayzdiary/work/work_form_add.html'
    fields=['job','start_time','end_time','description']
    
    def form_valid(self, form):
        work = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        work.day_entry = day_entry
        work.user = self.request.user        
        return super(WorkCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(WorkCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class WorkDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Work   
    template_name = 'heydayzdiary/work/work_confirm_delete.html'
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(WorkDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class StudyUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study
    form = StudyForm
    template_name = 'heydayzdiary/study/study_form.html'
    fields=['study_subject','start_time','end_time','description']    
    def get_queryset(self):
        base_qs = super(StudyUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context=super(StudyUpdate,self).get_context_data(**kwargs)
        context['form'].fields['study_subject'].queryset = Study_Subject.objects.filter(user=self.request.user)
        return context
    
class StudyCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study
    #form = StudyForm(user = 1)
    template_name = 'heydayzdiary/study/study_form_add.html'
    fields=['study_subject','start_time','end_time','description']
  
    def form_valid(self, form):
        study = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        study.day_entry = day_entry
        study.user = self.request.user
        return super(StudyCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(StudyCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        context['form'].fields['study_subject'].queryset = Study_Subject.objects.filter(user=self.request.user)
        return context

class StudyDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study    
    template_name = 'heydayzdiary/study/study_confirm_delete.html'
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(StudyDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)
		
class JobView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Job
    template_name = 'heydayzdiary/work/job_list.html'
    def get_queryset(self):
        """Return jobs for the logged-in user."""
        return Job.objects.filter(user=self.request.user).order_by('name')  

class JobCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Job
    form = JobForm
    fields=['name','description','start_date','end_date']
    template_name = 'heydayzdiary/work/job_add_form.html'
    def form_valid(self, form):
        job = form.save(commit=False)        
        job.user = self.request.user        
        return super(JobCreate, self).form_valid(form)

class JobUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Job
    form = JobForm
    template_name = 'heydayzdiary/work/job_form.html'
    fields=['name','description','start_date','end_date']
    def get_queryset(self):
        base_qs = super(JobUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class JobDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Job
    template_name = 'heydayzdiary/work/job_confirm_delete.html'
    success_url = reverse_lazy('heydayzdiary:job-list')
    def get_queryset(self):
        base_qs = super(JobDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)
		
class StudySubjectView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study_Subject
    template_name = 'heydayzdiary/study/study_subject_list.html'
    def get_queryset(self):
        """Return subjects for the logged-in user."""
        return Study_Subject.objects.filter(user=self.request.user).order_by('name')  

class StudySubjectCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study_Subject
    form = StudySubjectForm
    fields=['name','description']
    template_name = 'heydayzdiary/study/study_subject_add_form.html'
    def form_valid(self, form):
        study_subject = form.save(commit=False)        
        study_subject.user = self.request.user        
        return super(StudySubjectCreate, self).form_valid(form)

class StudySubjectUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study_Subject
    form = StudySubjectForm
    template_name = 'heydayzdiary/study/study_subject_form.html'
    fields=['name','description']
    def get_queryset(self):
        base_qs = super(StudySubjectUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class StudySubjectDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Study_Subject
    template_name = 'heydayzdiary/study/study_subject_confirm_delete.html'
    success_url = reverse_lazy('heydayzdiary:study_subject')
    def get_queryset(self):
        base_qs = super(StudySubjectDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class DayEntryLocationUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry_Location
    form = DayEntryLocationForm
    template_name = 'heydayzdiary/location/day_entry_location_form.html'
    fields=['location','mode_of_travel','travel_distance','travel_time']
    def get_queryset(self):
        base_qs = super(DayEntryLocationUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context=super(DayEntryLocationUpdate,self).get_context_data(**kwargs)
        context['form'].fields['location'].queryset = Location.objects.filter(user=self.request.user)
        return context
    
class DayEntryLocationDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry_Location    
    template_name = 'heydayzdiary/location/day_entry_location_confirm_delete.html'
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(DayEntryLocationDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class DayEntryLocationCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/location/day_entry_location_form_add.html'
    model = Day_entry_Location
    form = DayEntryLocationForm
    all_locations = Location.objects.all()
    fields=['location','mode_of_travel','travel_distance','travel_time']
    def form_valid(self, form):
        day_entry_location = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        day_entry_location.day_entry = day_entry
        day_entry_location.user = self.request.user
        return super(DayEntryLocationCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(DayEntryLocationCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        context['form'].fields['location'].queryset = Location.objects.filter(user=self.request.user)
        return context

class LocationView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Location
    template_name = 'heydayzdiary/location/location_list.html'
    def get_queryset(self):
        base_qs = super(LocationView, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class LocationCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Location
    form = LocationForm
    fields=['location_name']
    template_name = 'heydayzdiary/location/location_add_form.html'
    def form_valid(self, form):
        location = form.save(commit=False)       
        location.user = self.request.user
        return super(LocationCreate, self).form_valid(form)    

class LocationUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Location
    form = LocationForm
    template_name = 'heydayzdiary/location/location_form.html'
    fields=['location_name']
    def get_queryset(self):
        base_qs = super(LocationUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class LocationDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Location
    template_name = 'heydayzdiary/location/location_confirm_delete.html'
    success_url = reverse_lazy('heydayzdiary:location')
    def get_queryset(self):
        base_qs = super(LocationDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

# Person and DayEntryPerson
class DayEntryPersonUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry_Person
    form = DayEntryPersonForm
    template_name = 'heydayzdiary/person/day_entry_person_form.html'
    fields=['person','start_time','end_time']
    def get_queryset(self):
        base_qs = super(DayEntryPersonUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context=super(DayEntryPersonUpdate,self).get_context_data(**kwargs)
        context['form'].fields['person'].queryset = Person.objects.filter(user=self.request.user)
        return context
    
class DayEntryPersonDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry_Person
    template_name = 'heydayzdiary/person/day_entry_person_confirm_delete.html'
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(DayEntryPersonDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)   

class DayEntryPersonCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/person/day_entry_person_form_add.html'
    model = Day_entry_Person
    form = DayEntryPersonForm
    all_persons = Person.objects.all()
    fields=['person','start_time','end_time']
    def form_valid(self, form):
        day_entry_person = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        day_entry_person.day_entry = day_entry
        day_entry_person.user = self.request.user
        return super(DayEntryPersonCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(DayEntryPersonCreate,self).get_context_data(**kwargs)
        context['form'].fields['person'].queryset = Person.objects.filter(user=self.request.user)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class PersonView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Person
    template_name = 'heydayzdiary/person/person_list.html'
    def get_queryset(self):
        """Return persons for the logged-in user."""
        return Person.objects.filter(user=self.request.user).order_by('name')  

class PersonCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Person
    form = PersonForm
    template_name = 'heydayzdiary/person/person_add_form.html'
    fields=['name','date_of_birth','description','address','phone_number_1','phone_number_2','email_1','email_2','website_1','website_2','social_media_1','social_media_2','social_media_3','social_media_4']
    def form_valid(self, form):
        person = form.save(commit=False)
        person.user = self.request.user
        return super(PersonCreate, self).form_valid(form)
   
class PersonUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Person
    form = PersonForm
    template_name = 'heydayzdiary/person/person_form.html'
    fields=['name','date_of_birth','description','address','phone_number_1','phone_number_2','email_1','email_2','website_1','website_2','social_media_1','social_media_2','social_media_3','social_media_4']
    def get_queryset(self):
        base_qs = super(PersonUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class PersonDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Person
    template_name = 'heydayzdiary/person/person_confirm_delete.html'
    success_url = reverse_lazy('heydayzdiary:person-list')
    def get_queryset(self):
        base_qs = super(PersonDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    
# Project and DayEntryProject

class DayEntryProjectUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry_Project
    form = DayEntryProjectForm
    template_name = 'heydayzdiary/project/day_entry_project_form.html'
    fields=['project','start_time','end_time','description']
    def get_queryset(self):
        base_qs = super(DayEntryProjectUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    
class DayEntryProjectDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry_Project
    template_name = 'heydayzdiary/project/day_entry_project_confirm_delete.html'
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(DayEntryProjectDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class DayEntryProjectCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'    
    model = Day_entry_Project
    form = DayEntryProjectForm
    template_name = 'heydayzdiary/project/day_entry_project_form_add.html'
    all_projects = Project.objects.all()
    fields=['project','start_time','end_time','description']
    def form_valid(self, form):
        day_entry_project = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        day_entry_project.day_entry = day_entry
        day_entry_project.user = self.request.user
        return super(DayEntryProjectCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(DayEntryProjectCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class ProjectView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Project
    template_name = 'heydayzdiary/project/project_list.html'
    def get_queryset(self):
        """Return Projects for the logged-in user."""
        return Project.objects.filter(user=self.request.user).order_by('name')  

class ProjectCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Project
    form = ProjectForm
    template_name = 'heydayzdiary/project/project_add_form.html'
    fields=['name','start_date','end_date','description']   
    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)

class ProjectUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Project
    form = ProjectForm
    template_name = 'heydayzdiary/project/project_form.html'
    fields=['name','start_date','end_date','description']
    def get_queryset(self):
        base_qs = super(ProjectUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class ProjectDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Project
    template_name = 'heydayzdiary/project/project_confirm_delete.html'
    success_url = reverse_lazy('heydayzdiary:project-list')
    def get_queryset(self):
        base_qs = super(ProjectDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)