# Create your models here.
from django.db import models

# 1. Metro Lines
class MetroLine(models.Model):
    line_id = models.AutoField(primary_key=True)
    line_name = models.CharField(max_length=100)
    line_color = models.CharField(max_length=50)

    def __str__(self):
        return self.line_name

# 2. Stations
class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=255)
    line = models.ForeignKey(MetroLine, on_delete=models.CASCADE)
    station_order = models.IntegerField()
    is_interchange = models.IntegerField()

    def __str__(self):
        return self.station_name

# 3. Route Mapping (Connections between stations)
class StationConnection(models.Model):
    connection_id = models.AutoField(primary_key=True)
    from_station = models.ForeignKey(Station, related_name='connections_from', on_delete=models.CASCADE)
    to_station = models.ForeignKey(Station, related_name='connections_to', on_delete=models.CASCADE)
    travel_time_minutes = models.IntegerField()

# 4. Fare Table
class Fare(models.Model):
    fare_id = models.AutoField(primary_key=True)
    source_station = models.ForeignKey(Station, related_name='fare_sources', on_delete=models.CASCADE)
    destination_station = models.ForeignKey(Station, related_name='fare_destinations', on_delete=models.CASCADE)
    token_fare = models.DecimalField(max_digits=6, decimal_places=2)
    smartcard_fare = models.DecimalField(max_digits=6, decimal_places=2)

# 5. Routes (Saved or frequent routes)
class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    source_station = models.ForeignKey(Station, related_name='route_sources', on_delete=models.CASCADE)
    destination_station = models.ForeignKey(Station, related_name='route_destinations', on_delete=models.CASCADE)
    total_stations = models.IntegerField()
    total_time_minutes = models.IntegerField()
    interchanges_count = models.IntegerField()

# 6. Route Steps (Breakdown of a route)
class RouteStep(models.Model):
    step_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    line = models.ForeignKey(MetroLine, on_delete=models.CASCADE)
    step_order = models.IntegerField()
    instruction_text = models.TextField()
    time_from_previous = models.IntegerField()

# 7. Train Timings
class TrainTiming(models.Model):
    timing_id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    line = models.ForeignKey(MetroLine, on_delete=models.CASCADE)
    first_train_time = models.TimeField()
    last_train_time = models.TimeField()
    frequency_minutes = models.IntegerField()

# 8. Parking
class Parking(models.Model):
    parking_id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    total_slots = models.IntegerField()
    parking_fee_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

# 9. Feedback
class Feedback(models.Model): 
    feedback_id = models.AutoField(primary_key=True) 
    user_name = models.CharField(max_length=255) 
    email = models.EmailField() 
    message = models.TextField() 
    rating = models.IntegerField() 
    submitted_at = models.DateTimeField(auto_now_add=True)

# 10. Gates & Directions
class StationGate(models.Model):
    gate_id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    gate_number = models.CharField(max_length=10)
    direction_description = models.TextField()
    nearby_landmark = models.CharField(max_length=255)
