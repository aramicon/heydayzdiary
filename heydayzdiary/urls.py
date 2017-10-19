from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name='heydayzdiary'

urlpatterns = [
    #home page
    url(r'^home/$',views.HomeView.as_view(),name='home'),
       
    #login/logout/signup
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'heydayzdiary:home'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^admin/', admin.site.urls),
    #days
	url(r'^days/$',views.DaysView.as_view(),name='days'),
    url(r'^add/$', views.DayCreate.as_view(), name='day-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.DayUpdate.as_view(), name='day-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DayDelete.as_view(), name='day-delete'),
	#totals
	url(r'^totals/$',views.TotalsView.as_view(),name='totals'),	
	url(r'^totals/totals_sample_d3/$',views.TotalsSampleD3View.as_view(),name='totals_sample_d3'),	
	url(r'^totals_sample_d3/person_count_by_day$',views.person_count_by_day,name='person_count_by_day'),	
	url(r'^totals_sample_d3/project_work_by_day$',views.project_work_by_day,name='project_work_by_day'),	
	url(r'^totals_sample_d3/calorie_count_by_day$',views.calorie_count_by_day,name='calorie_count_by_day'),	
	url(r'^totals_sample_d3/exercise_time_by_day$',views.exercise_time_by_day,name='exercise_time_by_day'),	
    #day-read-view
    url(r'^(?P<pk>[0-9]+)/read$', views.DayReadFormat.as_view(), name='read-format'),
    # template days
    url(r'^(?P<day_entry_id>[0-9]+)/assign-day-template/$', views.AssignTemplateDay.as_view(), name='assign-template-day'),
    url(r'^use-template-day/$', views.UseTemplateDay, name='use-template-day'),
    url(r'^day-template-list/$', views.TemplateDayView.as_view(), name='template-day-list'),
    url(r'^day-template/add/$', views.TemplateDayCreate.as_view(), name='template-day-add'),
    url(r'^day-template/(?P<pk>[0-9]+)/$', views.TemplateDayUpdate.as_view(), name='template-day-update'),
    url(r'^day-template/(?P<pk>[0-9]+)/delete/$', views.TemplateDayDelete.as_view(), name='template-day-delete'),
    #exercise
    url(r'^(?P<day_entry_id>[0-9]+)/exercise/(?P<pk>[0-9]+)$', views.ExerciseUpdate.as_view(), name='exercise-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/exercise/add/$', views.ExerciseCreate.as_view(), name='exercise-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/exercise/(?P<pk>[0-9]+)/delete/$', views.ExerciseDelete.as_view(), name='exercise-delete'),
    #work
    url(r'^(?P<day_entry_id>[0-9]+)/work/(?P<pk>[0-9]+)$', views.WorkUpdate.as_view(), name='work-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/work/add/$', views.WorkCreate.as_view(), name='work-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/work/(?P<pk>[0-9]+)/delete/$', views.WorkDelete.as_view(), name='work-delete'),
    #job
    url(r'^job/$', views.JobView.as_view(), name='job-list'),
    url(r'^job/add/$', views.JobCreate.as_view(), name='job-add'),
    url(r'^job/(?P<pk>[0-9]+)/$', views.JobUpdate.as_view(), name='job-update'),
    url(r'^job/(?P<pk>[0-9]+)/delete$', views.JobDelete.as_view(), name='job-delete'),
    #meal
    url(r'^(?P<day_entry_id>[0-9]+)/meal/(?P<pk>[0-9]+)$', views.MealUpdate.as_view(), name='meal-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/meal/add/$', views.MealCreate.as_view(), name='meal-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/meal/(?P<pk>[0-9]+)/delete/$', views.MealDelete.as_view(), name='meal-delete'),
    #transaction
    url(r'^(?P<day_entry_id>[0-9]+)/transaction/(?P<pk>[0-9]+)$', views.TransactionUpdate.as_view(), name='transaction-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/transaction/add/$', views.TransactionCreate.as_view(), name='transaction-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/transaction/(?P<pk>[0-9]+)/delete/$', views.TransactionDelete.as_view(), name='transaction-delete'),
    #study
    url(r'^(?P<day_entry_id>[0-9]+)/study/(?P<pk>[0-9]+)$', views.StudyUpdate.as_view(), name='study-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/study/add/$', views.StudyCreate.as_view(), name='study-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/study/(?P<pk>[0-9]+)/delete/$', views.StudyDelete.as_view(), name='study-delete'),
    #study_subject
    url(r'^study_subject/$', views.StudySubjectView.as_view(), name='study_subject-list'),
    url(r'^study_subject/add/$', views.StudySubjectCreate.as_view(), name='study_subject-add'),
    url(r'^study_subject/(?P<pk>[0-9]+)/$', views.StudySubjectUpdate.as_view(), name='study_subject-update'),
    url(r'^study_subject/(?P<pk>[0-9]+)/delete$', views.StudySubjectDelete.as_view(), name='study_subject-delete'),
    #locations
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_location/(?P<pk>[0-9]+)$', views.DayEntryLocationUpdate.as_view(), name='day_entry_location-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_location/(?P<pk>[0-9]+)/delete$', views.DayEntryLocationDelete.as_view(), name='day_entry_location-delete'),
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_location/add/$', views.DayEntryLocationCreate.as_view(), name='day_entry_location-add'),
    url(r'^location/$', views.LocationView.as_view(), name='location-list'),
    url(r'^location/add/$', views.LocationCreate.as_view(), name='location-add'),
    url(r'^location/(?P<pk>[0-9]+)/$', views.LocationUpdate.as_view(), name='location-update'),
    url(r'^location/(?P<pk>[0-9]+)/delete$', views.LocationDelete.as_view(), name='location-delete'),
    #day-entry-persons
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_person/(?P<pk>[0-9]+)$', views.DayEntryPersonUpdate.as_view(), name='day_entry_person-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_person/(?P<pk>[0-9]+)/delete$', views.DayEntryPersonDelete.as_view(), name='day_entry_person-delete'),
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_person/add/$', views.DayEntryPersonCreate.as_view(), name='day_entry_person-add'),
    #person
    url(r'^person/$', views.PersonView.as_view(), name='person-list'),
    url(r'^person/add/$', views.PersonCreate.as_view(), name='person-add'),
    url(r'^person/(?P<pk>[0-9]+)/$', views.PersonUpdate.as_view(), name='person-update'),
    url(r'^person/(?P<pk>[0-9]+)/delete$', views.PersonDelete.as_view(), name='person-delete'),
    #day-entry-projects
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_project/(?P<pk>[0-9]+)$', views.DayEntryProjectUpdate.as_view(), name='day_entry_project-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_project/(?P<pk>[0-9]+)/delete$', views.DayEntryProjectDelete.as_view(), name='day_entry_project-delete'),
    url(r'^(?P<day_entry_id>[0-9]+)/day_entry_project/add/$', views.DayEntryProjectCreate.as_view(), name='day_entry_project-add'),
    #project
    url(r'^project/$', views.ProjectView.as_view(), name='project-list'),
    url(r'^project/add/$', views.ProjectCreate.as_view(), name='project-add'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'^project/(?P<pk>[0-9]+)/delete$', views.ProjectDelete.as_view(), name='project-delete'),
]