from django.urls import path
from . import views

urlpatterns = [    
    path('',views.home, name="home"), 
    path('fare/',views.fare, name="fare"),
    path('route & map/',views.routemap, name="route & map"),
    path('timings/',views.timings, name="timings"),
    path('parkings/',views.parkings, name="parkings"),
    path('feedback/',views.feedback, name="feedback"),
    path('gates & direction/',views.gatesdir, name="gates & direction"), 
]