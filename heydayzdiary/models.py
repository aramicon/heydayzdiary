from django.db import models
from django.urls import reverse
from django.conf import settings

class Day_entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    day_headline = models.CharField(max_length=200)
    day_date = models.DateTimeField()
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    day_main_text = models.TextField()
    sleep_duration = models.DecimalField(blank=True,max_digits=3, decimal_places=1)
    sleep_quality = models.IntegerField(blank=True, null=True)
    wake_up_time = models.TimeField(blank=True, null=True)
    sleep_notes = models.TextField(blank=True)
    weather_rain = models.IntegerField(blank=True, null=True)
    weather_sun = models.IntegerField(blank=True, null=True)
    weather_wind = models.IntegerField(blank=True, null=True)
    weather_temperature = models.IntegerField(blank=True, null=True)
    weather_notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.day_headline
    def is_today(self):
        return self.day_date >= timezone.now() - datetime.timedelta(days=1) 
    def get_absolute_url(self):
        return reverse('heydayzdiary:detail-update', kwargs={'pk': self.pk})

class Exercise_type(models.Model):
    exercise_type_description = models.CharField(max_length=200)
    def __str__(self):
        return self.exercise_type_description
    def get_absolute_url(self):
        return reverse('heydayzdiary:exercise_type-update',kwargs={'pk':self.pk})

class Exercise(models.Model):    
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    exercise_type = models.ForeignKey(Exercise_type, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    intensity = models.IntegerField(blank=True, null=True)
    distance = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    web_tracking_system_url = models.URLField(blank=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:exercise-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})

class Meal_type(models.Model):
    meal_type_description = models.CharField(max_length=200)
    def __str__(self):
        return self.meal_type_description
    def get_absolute_url(self):
        return reverse('heydayzdiary:meal_type-update',kwargs={'pk':self.pk})

class Meal(models.Model):
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    meal_type = models.ForeignKey(Meal_type, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    meal_time = models.TimeField()
    description = models.TextField(blank=True)
    calories = models.IntegerField(blank=True,null=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:meal-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})
        
class Transaction_type(models.Model):
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:transaction_type-update',kwargs={'pk':self.pk})

class Transaction(models.Model):
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(Transaction_type, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    transaction_time = models.TimeField()
    description = models.TextField(blank=True)
    amount = models.DecimalField(blank=True,max_digits=8, decimal_places=2)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:transaction-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})
		
class Job(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('heydayzdiary:job-update', kwargs={'pk': self.pk})   
		
class Work(models.Model):
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL,null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True) 
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:work-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})        
        
class Study_Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('heydayzdiary:study_subject-update', kwargs={'pk': self.pk})        

class Study(models.Model):
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    study_subject = models.ForeignKey(Study_Subject, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True) 
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:study-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})

class Location(models.Model):
    location_name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.location_name
    def get_absolute_url(self):
        return reverse('heydayzdiary:location-update', kwargs={'pk': self.pk})

class Mode_of_travel(models.Model):
    description = models.CharField(max_length=200)    
    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse('heydayzdiary:mode_of_travel-update', kwargs={'pk': self.pk})
        
class Day_entry_Location(models.Model):
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mode_of_travel = models.ForeignKey(Mode_of_travel, on_delete=models.CASCADE,blank=True,null=True)
    travel_time = models.DecimalField(blank=True,null=True,max_digits=4, decimal_places=2)
    travel_distance = models.DecimalField(blank=True,null=True,max_digits=4, decimal_places=2)   
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def get_absolute_url(self):
        return reverse('heydayzdiary:day_entry_location-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})
    def __str__(self):
        return self.location.location_name

class Person(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500,blank=True)
    phone_number_1 = models.CharField(max_length=50,blank=True)
    phone_number_2 = models.CharField(max_length=50,blank=True)
    email_1 = models.CharField(max_length=100,blank=True)
    email_2 = models.CharField(max_length=100,blank=True)
    website_1 = models.CharField(max_length=200,blank=True)
    website_2 = models.CharField(max_length=200,blank=True)
    social_media_1 = models.CharField(max_length=200,blank=True)
    social_media_2 = models.CharField(max_length=200,blank=True)
    social_media_3 = models.CharField(max_length=200,blank=True)
    social_media_4 = models.CharField(max_length=200,blank=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('heydayzdiary:person-update', kwargs={'pk': self.pk})

class Day_entry_Person(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def get_absolute_url(self):
        return reverse('heydayzdiary:day_entry_person-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})
    def __str__(self):
        return self.person.name

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('heydayzdiary:project-update', kwargs={'pk': self.pk})
        
class Day_entry_Project(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    day_entry = models.ForeignKey(Day_entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date_updated = models.DateTimeField('Date updated',auto_now=True)
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    def get_absolute_url(self):
        return reverse('heydayzdiary:day_entry_project-update', kwargs={'day_entry_id':self.day_entry_id,'pk': self.pk})
    def __str__(self):
        return self.project.name
    
    
        
