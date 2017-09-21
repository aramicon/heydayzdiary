from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.utils import timezone
from django.urls import reverse_lazy
import math
import sys


from .models import Day_entry, Exercise, Work, Study, Day_entry_Location, Location, Day_entry_Person, Person, Day_entry_Project, Project, Meal, Transaction, Study_Subject

from heydayzdiary.forms import DayEntryForm, ExerciseForm, WorkForm, StudyForm, DayEntryLocationForm, LocationForm, PersonForm, DayEntryPersonForm, ProjectForm, DayEntryProjectForm, MealForm, TransactionForm, StudySubjectForm

class IndexView(generic.ListView):
    template_name = 'heydayzdiary/index.html'
    context_object_name = 'latest_day_entries'
    
    def get_queryset(self):
        """Return the most recent 10 day entries."""
        return Day_entry.objects.filter(day_date__lte=timezone.now()).order_by('-day_date')[:10]        
    
class DetailCreate(CreateView):
    model = Day_entry
    fields=['day_headline','day_main_text','day_date','sleep_duration','sleep_quality','sleep_notes','wake_up_time','weather_sun','weather_rain','weather_wind','weather_temperature','weather_notes']
    template_name = 'heydayzdiary/day_entry_add_form.html'
    
    # def get_queryset(self):
        # """
        # Excludes any days that are not published yet.
        # """
        # return Day_entry.objects.filter(day_date__lte=timezone.now())    
class DetailUpdate(UpdateView):
    model = Day_entry
    form = DayEntryForm
    fields=['day_headline','day_main_text','day_date','sleep_duration','sleep_quality','sleep_notes','wake_up_time','weather_sun','weather_rain','weather_wind','weather_temperature','weather_notes']
    # def form_valid(self, form):
        # """
        # If the form is valid, save the associated model.
        # """
        # print("test 1", file=sys.stderr)
        # self.object = form.save(commit=False)
        # #need to change the displayed 1.2 format of sleep to the db intger 12
        # self.object.sleep_duration = self.object.sleep_duration + 1 # form.data['sleep_duration']
        # #print(" day_entry.sleep_duration = " + sleep_duration, file=sys.stderr)
        # #day_entry.sleep_duration = math.floor((float(sleep_duration))*10)
        # self.object = form.save()
        # return super(DetailUpdate, self).form_valid(form)

class DetailReadFormat(DetailView):
    model = Day_entry
    template_name = 'heydayzdiary/day_entry_readformat_form.html'
    
class DetailDelete(DeleteView):
    model = Day_entry
    success_url = reverse_lazy('heydayzdiary')
    
class ExerciseUpdate(UpdateView):
    model = Exercise
    form = ExerciseForm
    fields=['start_time','end_time','description','exercise_type']

class ExerciseCreate(CreateView):
    model = Exercise
    form = ExerciseForm
    template_name = 'heydayzdiary/exercise_form_add.html'
    fields=['start_time','end_time','description','exercise_type']
    # def dispatch(self, *args, **kwargs):
        # self.day_entry = get_object_or_404(Day_entry, pk=kwargs['day_entry_id'])
        # return super(ExerciseCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        exercise = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        exercise.day_entry = day_entry
        return super(ExerciseCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(ExerciseCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class ExerciseDelete(DeleteView):
    model = Exercise    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
		
class MealUpdate(UpdateView):
    model = Meal
    form = MealForm
    fields=['meal_time','description','meal_type','calories']

class MealCreate(CreateView):
    model = Meal
    form = MealForm
    template_name = 'heydayzdiary/meal_form_add.html'
    fields=['meal_time','description','meal_type','calories']
  
    def form_valid(self, form):
        meal = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        meal.day_entry = day_entry
        return super(MealCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(MealCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class MealDelete(DeleteView):
    model = Meal    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})	
		
class TransactionUpdate(UpdateView):
    model = Transaction
    form = TransactionForm
    fields=['transaction_time','description','transaction_type','amount']

class TransactionCreate(CreateView):
    model = Transaction
    form = TransactionForm
    template_name = 'heydayzdiary/transaction_form_add.html'
    fields=['transaction_time','description','transaction_type','amount']
  
    def form_valid(self, form):
        transaction = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        transaction.day_entry = day_entry
        return super(TransactionCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(TransactionCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class TransactionDelete(DeleteView):
    model = Transaction    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})			
class WorkUpdate(UpdateView):
    model = Work
    form = WorkForm
    fields=['start_time','end_time','description']

class WorkCreate(CreateView):
    model = Work
    form = WorkForm
    template_name = 'heydayzdiary/work_form_add.html'
    fields=['start_time','end_time','description']
    
    def form_valid(self, form):
        work = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        work.day_entry = day_entry
        return super(WorkCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(WorkCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class WorkDelete(DeleteView):
    model = Work    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})

class ExerciseDelete(DeleteView):
    model = Exercise    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})
		
class StudyUpdate(UpdateView):
    model = Study
    form = StudyForm
    fields=['study_subject','start_time','end_time','description']

class StudyCreate(CreateView):
    model = Study
    form = StudyForm
    template_name = 'heydayzdiary/study_form_add.html'
    fields=['study_subject','start_time','end_time','description']
    
    def form_valid(self, form):
        study = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        study.day_entry = day_entry
        return super(StudyCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(StudyCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class StudyDelete(DeleteView):
    model = Study    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})

class StudySubjectView(generic.ListView):
    model = Study_Subject

class StudySubjectCreate(CreateView):
    model = Study_Subject
    form = StudySubjectForm
    fields=['name','description']
    template_name = 'heydayzdiary/study_subject_add_form.html'

class StudySubjectUpdate(UpdateView):
    model = Study_Subject
    form = StudySubjectForm
    fields=['name','description']

class StudySubjectDelete(DeleteView):
    model = Study_Subject
    success_url = reverse_lazy('heydayzdiary:study_subject')

class DayEntryLocationUpdate(UpdateView):
    model = Day_entry_Location
    form = DayEntryLocationForm
    fields=['location']
	
class DayEntryLocationDelete(DeleteView):
    model = Day_entry_Location    
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})

class DayEntryLocationCreate(CreateView):
    template_name = 'heydayzdiary/day_entry_location_form_add.html'
    model = Day_entry_Location
    form = DayEntryLocationForm
    all_locations = Location.objects.all()
    fields=['location']
    def form_valid(self, form):
        day_entry_location = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        day_entry_location.day_entry = day_entry
        return super(DayEntryLocationCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(DayEntryLocationCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class LocationView(generic.ListView):
    model = Location
   # template_name = 'heydayzdiary/locations_list.html'

class LocationCreate(CreateView):
    model = Location
    form = LocationForm
    fields=['location_name']
    template_name = 'heydayzdiary/location_add_form.html'

class LocationUpdate(UpdateView):
    model = Location
    form = LocationForm
    fields=['location_name']

class LocationDelete(DeleteView):
    model = Location
    success_url = reverse_lazy('heydayzdiary:location')

# Person and DayEntryPerson
class DayEntryPersonUpdate(UpdateView):
    model = Day_entry_Person
    form = DayEntryPersonForm
    fields=['person','start_time','end_time']
	
class DayEntryPersonDelete(DeleteView):
    model = Day_entry_Person 
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})

class DayEntryPersonCreate(CreateView):
    template_name = 'heydayzdiary/day_entry_person_form_add.html'
    model = Day_entry_Person
    form = DayEntryPersonForm
    all_persons = Person.objects.all()
    fields=['person','start_time','end_time']
    def form_valid(self, form):
        day_entry_person = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        day_entry_person.day_entry = day_entry
        return super(DayEntryPersonCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(DayEntryPersonCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class PersonView(generic.ListView):
    model = Person

class PersonCreate(CreateView):
    model = Person
    form = PersonForm
    fields=['name','date_of_birth','description','address','phone_number_1','phone_number_2','email_1','email_2','website_1','website_2','social_media_1','social_media_2','social_media_3','social_media_4']
    template_name = 'heydayzdiary/person_add_form.html'

class PersonUpdate(UpdateView):
    model = Person
    form = PersonForm
    fields=['name','date_of_birth','description','address','phone_number_1','phone_number_2','email_1','email_2','website_1','website_2','social_media_1','social_media_2','social_media_3','social_media_4']

class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('heydayzdiary:person-list')
# Project and DayEntryProject
class DayEntryProjectUpdate(UpdateView):
    model = Day_entry_Project
    form = DayEntryProjectForm
    fields=['project','start_time','end_time','description']
	
class DayEntryProjectDelete(DeleteView):
    model = Day_entry_Project 
    def get_success_url(self):
        day_entry = self.object.day_entry 
        return reverse_lazy('heydayzdiary:detail-update',kwargs={'pk': day_entry.id})

class DayEntryProjectCreate(CreateView):
    template_name = 'heydayzdiary/day_entry_project_form_add.html'
    model = Day_entry_Project
    form = DayEntryProjectForm
    all_projects = Project.objects.all()
    fields=['project','start_time','end_time','description']
    def form_valid(self, form):
        day_entry_project = form.save(commit=False)
        day_entry_id = form.data['day_entry_id']
        day_entry = get_object_or_404(Day_entry, id=day_entry_id)
        day_entry_project.day_entry = day_entry
        return super(DayEntryProjectCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super(DayEntryProjectCreate,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context

class ProjectView(generic.ListView):
    model = Project

class ProjectCreate(CreateView):
    model = Project
    form = ProjectForm
    fields=['name','start_date','end_date','description']
    template_name = 'heydayzdiary/project_add_form.html'

class ProjectUpdate(UpdateView):
    model = Project
    form = ProjectForm
    fields=['name','start_date','end_date','description']

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('heydayzdiary:project-list')