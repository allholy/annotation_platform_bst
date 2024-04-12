from django.urls import path
from . import views

app_name = 'classurvey'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('instructions/', views.instructions_view, name='instructions'),
    path('taxonomy/', views.taxonomy_view, name='taxonomy'),
    path('user-data/', views.user_details_view, name='user_details'),
    path('annotate-sound/',views.annotate_sound_view, name='main'),
    path('batch-end/', views.batch_end_view, name='batch_end'),
    path('data-end/', views.data_end_view, name='data_end'),
    path('results/', views.results_view, name='results'),
    path('export/', views.export_view, name='export'),
]