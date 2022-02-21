from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from datetime import timedelta
#from django.contrib.auth.forms import UserCreationForm
import math
import sys
import datetime
import csv

from django.db import connections
from django.db.models import Count, Min, Sum, Avg, F
from django.http import JsonResponse


from .models import Day_entry, Exercise, Work, Study, Day_entry_Location, Location, Day_entry_Person, Person, Day_entry_Project, Project, Meal, Transaction, Study_Subject, Job,Template_Day

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
        return redirect('heydayzdiary:days')


def UseTemplateDay(request):
    if request.method == 'POST':
        template_day_selected = request.POST.get('template_day_selected')
        #get this template day
        #day_template = get_object_or_404(Template_Day, id=template_day_selected)
        #day_entry = day_template.day_entry
        day_entry = get_object_or_404(Day_entry, id=template_day_selected)
        #need to create a new entry

        day_entry.day_main_text = ""
        day_entry.day_headline = day_entry.day_headline
        day_entry.day_date = datetime.date.today()
        day_entry.is_template_day = False

        old_day_entry_location = day_entry.day_entry_location_set.all()
        old_day_entry_person_set = day_entry.day_entry_person_set.all()
        old_meal_set = day_entry.meal_set.all()
        old_work_set = day_entry.work_set.all()

        day_entry.pk = None #this is what causes a NEW day to be created
        day_entry.save()
        #now add the old locations/etc to the new day
        #originaly effort here simply MOVED the old links to the new day instead of creating new (copies)
        #loop through the locations to copy, create new location each time, assinging each to the new day_entry
        for day_entry_location in old_day_entry_location:
            day_entry_location.pk = None
            day_entry_location.day_entry = day_entry
            day_entry_location.save()

        for day_entry_person in old_day_entry_person_set:
            day_entry_person.pk = None
            day_entry_person.day_entry = day_entry
            day_entry_person.save()

        for meal in old_meal_set:
            meal.pk = None
            meal.day_entry = day_entry
            meal.save()

        for work in old_work_set:
            work.pk = None
            work.day_entry = day_entry
            work.save()

        return redirect('heydayzdiary:days')
    else:
        return redirect('heydayzdiary:days')

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
        return Day_entry.objects.filter(user=self.request.user,is_template_day=False).order_by('-day_date')
    def get_context_data(self, **kwargs):
        context=super(DaysView,self).get_context_data(**kwargs)
        #context['template_days'] =  Template_Day.objects.exclude(day_entry__isnull=True)

        context['template_days'] =  Day_entry.objects.filter(is_template_day=True,user=self.request.user).order_by('-day_date')
        return context

class TotalsView(LoginRequiredMixin,TemplateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/totals/totals_main_page.html'
    def get_context_data(self, **kwargs):
        context=super(TotalsView,self).get_context_data(**kwargs)
        context['total_days'] =  Day_entry.objects.filter(user=self.request.user).count()
        #context['template_days'] =  Template_Day.objects.filter(Day_entry > 0)
        return context

class TotalsSampleD3View(LoginRequiredMixin,TemplateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    template_name = 'heydayzdiary/totals/totals_sample_d3.html'
    def get_context_data(self, **kwargs):
        context=super(TotalsSampleD3View,self).get_context_data(**kwargs)
        #context['total_days'] =  Day_entry.objects.filter(user=self.request.user).count()
        #context['template_days'] =  Template_Day.objects.filter(Day_entry > 0)
        return context

def person_count_by_day(request):
    data = Day_entry.objects.filter(user=request.user).values('day_date').annotate(num_persons=Count('day_entry_person')).order_by('day_date')
    return JsonResponse(list(data), safe=False)

def project_work_by_day(request):
    data = Day_entry.objects.filter(user=request.user).values('day_date').annotate(project_time=Sum(F('day_entry_project__end_time')-F('day_entry_project__start_time'))/60000000).order_by('day_date')
    return JsonResponse(list(data), safe=False)

def calorie_count_by_day(request):
    data = Day_entry.objects.filter(user=request.user).values('day_date').annotate(calorie_count=Sum('meal__calories')).order_by('day_date')
    return JsonResponse(list(data), safe=False)

def exercise_time_by_day(request):
    data = Day_entry.objects.filter(user=request.user).values('day_date').annotate(exercise_time=Sum(F('exercise__end_time')-F('exercise__start_time'))/60000000).order_by('day_date')
    return JsonResponse(list(data), safe=False)


class DayCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    fields=['day_headline','day_main_text','day_date','sleep_duration','sleep_quality','sleep_notes','wake_up_time','weather_sun','weather_rain','weather_wind','weather_temperature','weather_notes']
    template_name = 'heydayzdiary/day/day_entry_add_form.html'
    def form_valid(self, form):
        day = form.save(commit=False)
        day.user = self.request.user
        return super(DayCreate, self).form_valid(form)

class DayUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    form = DayEntryForm
    template_name = 'heydayzdiary/day/day_entry_form.html'
    fields=['day_headline','day_main_text','day_date','sleep_duration','sleep_quality','sleep_notes','wake_up_time','weather_sun','weather_rain','weather_wind','weather_temperature','weather_notes','is_template_day']
    def get_queryset(self):
        base_qs = super(DayUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)
    def form_invalid(self, form):
        return HttpResponse("form is invalid... " + str(form.errors))

class DayReadFormat(LoginRequiredMixin,DetailView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    template_name = 'heydayzdiary/day/day_entry_readformat_form.html'
    def get_queryset(self):
        base_qs = super(DayReadFormat, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class DayDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Day_entry
    success_url = reverse_lazy('heydayzdiary')
    template_name = 'heydayzdiary/day/day_entry_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('heydayzdiary:days')
    def get_queryset(self):
        base_qs = super(DayDelete, self).get_queryset()
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
    def get_queryset(self):
        base_qs = super(MealDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class TransactionUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Transaction
    form = TransactionForm
    template_name = 'heydayzdiary/transaction/transaction_form.html'
    fields=['transaction_time','description','transaction_type','job','amount']
    def get_queryset(self):
        base_qs = super(TransactionUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class TransactionCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Transaction
    form = TransactionForm
    template_name = 'heydayzdiary/transaction/transaction_form_add.html'
    fields=['transaction_time','description','transaction_type','job','amount']

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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
    def get_context_data(self, **kwargs):
        context=super(JobUpdate,self).get_context_data(**kwargs)
        job = get_object_or_404(Job, id=self.kwargs['pk'])
        total_job_duration  =  Work.objects.filter(job=job).aggregate(total_job_duration=Sum(F('end_time')-F('start_time'))/60000000)
        #if there are no jobs we want to set this to 0, not None.
        if total_job_duration["total_job_duration"] is None:
            total_job_duration = 0.0
            total_job_duration_hours = 0.0
        else:
            context['total_job_duration'] = total_job_duration["total_job_duration"]
            context['total_job_duration_hours'] = str(round(total_job_duration["total_job_duration"]/60,2)) + " hours. " + str(math.floor(total_job_duration["total_job_duration"]/60)) + ":" +  str((total_job_duration["total_job_duration"] % 60))
        return context
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
        return reverse_lazy('heydayzdiary:day-update',kwargs={'pk': day_entry.id})
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
    def get_context_data(self, **kwargs):
        context=super(ProjectUpdate,self).get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        total_project_duration  =  Day_entry_Project.objects.filter(project=project).aggregate(total_project_duration=Sum(F('end_time')-F('start_time'))/60000000)
        context['total_project_duration'] = total_project_duration["total_project_duration"]
        context['total_project_duration_hours'] = str(round(total_project_duration["total_project_duration"]/60,2)) + "hours. " + str(math.floor(total_project_duration["total_project_duration"]/60)) + ":" +  str((total_project_duration["total_project_duration"] % 60))
        return context

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

class AssignTemplateDay(LoginRequiredMixin,generic.ListView):
    login_url='heydayzdiary:login'
    redirect_field_name='heydayzdiary:days'
    template_name = 'heydayzdiary/template_day/make_template.html'
    queryset = Template_Day.objects.all()
    context_object_name = 'template_days'
    def get_context_data(self, **kwargs):
        context=super(AssignTemplateDay,self).get_context_data(**kwargs)
        context['d_id'] = self.kwargs['day_entry_id']
        return context
    def post(self, request, *args, **kwargs):
        #if self.form.is_valid():
        template_day_selected = request.POST.get('template_day_selected')
        day_entry_id = request.POST.get('day_entry_id')
        if (template_day_selected == '0'):
            #make sure no template day is assigned to this day
            for template_day in Template_Day.objects.filter(day_entry_id=day_entry_id):
                template_day.day_entry_id = None
                template_day.save()
        else:
            day_template = get_object_or_404(Template_Day, id=template_day_selected)
            day_entry = get_object_or_404(Day_entry, id=day_entry_id)

            day_template.day_entry = day_entry

            day_template.save()

        #return render(request, self.template_name,{day_entry_id:day_entry_id,template_day_selected:template_day_selected})
        return redirect('heydayzdiary:assign-template-day', day_entry_id=day_entry_id)


class TemplateDayView(LoginRequiredMixin,generic.ListView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Template_Day
    template_name = 'heydayzdiary/template_day/template_day_list.html'
    context_object_name = 'template_day_entries'
    def get_queryset(self):
        """Return day entries for the logged-in user."""
        return Day_entry.objects.filter(is_template_day=True,user=self.request.user).order_by('-day_date')
    def get_context_data(self, **kwargs):
        context=super(TemplateDayView,self).get_context_data(**kwargs)
        context['template_days'] =  Day_entry.objects.filter(is_template_day=True,user=self.request.user).order_by('-day_date')
        #context['template_days'] =  Template_Day.objects.filter(Day_entry > 0)
        return context

class TemplateDayCreate(LoginRequiredMixin,CreateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Template_Day
    fields=['day_entry','name','description']
    template_name = 'heydayzdiary/template_day/template_day_add_form.html'
    def form_valid(self, form):
        templateDay = form.save(commit=False)
        templateDay.user = self.request.user
        return super(TemplateDayCreate, self).form_valid(form)

class TemplateDayUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Template_Day

    template_name = 'heydayzdiary/template_day/template_day_form.html'
    fields=['day_entry','name','description']
    def get_queryset(self):
        base_qs = super(TemplateDayUpdate, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class TemplateDayDelete(LoginRequiredMixin,DeleteView):
    login_url = 'heydayzdiary:login'
    redirect_field_name = 'heydayzdiary:days'
    model = Template_Day
    template_name = 'heydayzdiary/template_day/template_day_confirm_delete.html'
    success_url = reverse_lazy('heydayzdiary:template-day-list')
    def get_queryset(self):
        base_qs = super(TemplateDayDelete, self).get_queryset()
        return base_qs.filter(user=self.request.user)

def diff_in_time(start,end):
    startdelta=timedelta(hours=start.hour,minutes=start.minute,seconds=start.second)
    enddelta=timedelta(hours=end.hour,minutes=end.minute,seconds=end.second)
    return (enddelta-startdelta).seconds/60


def WorkExportAsCSV(request, pk):
    # Create the HttpResponse object with the appropriate CSV header.
    print('export work details as CSV (export link clicked)')

    job_id = pk
    print(job_id)

    response = HttpResponse(content_type='text/csv')
    workExportfilename = "heydayzdiary_work_export_" + str(job_id) + ".csv"
    response['Content-Disposition'] = 'attachment; filename='+ workExportfilename

    writer = csv.writer(response,delimiter=',', quoting=csv.QUOTE_ALL, quotechar='"')

    writer.writerow(["work_id", "date", "start_time", "end_time","duration_minutes", "description"])


#day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
#user = models.ForeignKey(settings.AUTH_USER_MODEL)
#job = models.ForeignKey(Job, on_delete=models.SET_NULL,null=True,blank=True)
#start_time = models.TimeField()
#end_time = models.TimeField()
#description = models.TextField(blank=True)
#date_updated = models.DateTimeField('Date updated',auto_now=True)
#date_created = models.DateTimeField('Date Created',auto_now_add=True)


    for work in Work.objects.filter(user=request.user,job_id=job_id).order_by('-day_entry__day_date', '-end_time'):
        writer.writerow([work.id, work.day_entry.day_date.strftime("%Y-%m-%d"), work.start_time, work.end_time, diff_in_time(work.start_time, work.end_time), work.description.replace('\r\n', '\\n')])
    print('CSV job work export ready to be returned')
    return response
