from django.contrib import admin

# Register your models here.

from .models import Day_entry, Exercise, Exercise_type, Location, Meal_type, Transaction_type, Mode_of_travel

admin.site.register(Day_entry)
admin.site.register(Exercise)
admin.site.register(Exercise_type)
admin.site.register(Meal_type)
admin.site.register(Transaction_type)
admin.site.register(Location)
admin.site.register(Mode_of_travel)