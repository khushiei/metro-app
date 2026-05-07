from django.contrib import admin
from .models import (
    MetroLine, Station, StationConnection, Fare, 
    Route, RouteStep, TrainTiming, Parking, 
    Feedback, StationGate
)


admin.site.register(MetroLine)
admin.site.register(Station)
admin.site.register(StationConnection)
admin.site.register(Fare)
admin.site.register(Route)
admin.site.register(RouteStep)
admin.site.register(TrainTiming)
admin.site.register(Parking)
admin.site.register(Feedback)
admin.site.register(StationGate)