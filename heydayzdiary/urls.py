from django.conf.urls import url

from . import views

app_name='heydayzdiary'

urlpatterns = [
    # ex: /heydayzdiary/
    url(r'^$',views.IndexView.as_view(),name='index'),
    # ex: /polls/5/
    #rl(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(),name='detail'),
    url(r'^add/$', views.DetailCreate.as_view(), name='detail-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailUpdate.as_view(), name='detail-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DetailDelete.as_view(), name='detail-delete'),
    #day-read-view
      url(r'^(?P<pk>[0-9]+)/read$', views.DetailReadFormat.as_view(), name='read-format'),
    #exercise
    url(r'^(?P<day_entry_id>[0-9]+)/exercise/(?P<pk>[0-9]+)$', views.ExerciseUpdate.as_view(), name='exercise-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/exercise/add/$', views.ExerciseCreate.as_view(), name='exercise-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/exercise/(?P<pk>[0-9]+)/delete/$', views.ExerciseDelete.as_view(), name='exercise-delete'),
    #work
    url(r'^(?P<day_entry_id>[0-9]+)/work/(?P<pk>[0-9]+)$', views.WorkUpdate.as_view(), name='work-update'),
    url(r'^(?P<day_entry_id>[0-9]+)/work/add/$', views.WorkCreate.as_view(), name='work-add'),
    url(r'^(?P<day_entry_id>[0-9]+)/work/(?P<pk>[0-9]+)/delete/$', views.WorkDelete.as_view(), name='work-delete'),
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
    url(r'^location/$', views.LocationView.as_view(), name='location'),
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