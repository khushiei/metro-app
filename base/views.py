from django.shortcuts import render
from .models import Station, StationConnection, StationGate, Parking, TrainTiming
from .form import FeedbackForm
import heapq

def dijkstra(graph, start, end):
    queue = [(0, start)] 
    times = {node: float('inf') for node in graph} #infinty time for unknown
    times[start] = 0 #start 0
    previous = {node: None for node in graph} 

    while queue:
        current_time, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, weight in graph[current_node].items():
            new_time = current_time + weight

            if new_time < times[neighbor]:
                times[neighbor] = new_time
                previous[neighbor] = current_node
                heapq.heappush(queue, (new_time, neighbor))

    path = []
    current = end
    while current:
        path.insert(0, current)
        current = previous[current]

    return path, times[end]

def home(request):
    stations = Station.objects.all()

    if request.method == "POST":
        source_id = request.POST.get('source')
        dest_id = request.POST.get('destination')
        source = Station.objects.filter(station_id=source_id).first()
        destination = Station.objects.filter(station_id=dest_id).first()

        if not source or not destination:
            return render(request, 'base/home.html', {
                        'stations': stations,
                        'error': 'Invalid station selected. Please try again.'
                        })
        if source_id == dest_id:
            return render(request, 'base/home.html', {
                        'stations': stations,
                        'error': 'Source and destination cannot be the same!'
                        })
        graph = {}

        connections = StationConnection.objects.all()

        for conn in connections:
            a = conn.from_station.station_id
            b = conn.to_station.station_id
            t = conn.travel_time_minutes   # using time as weight

            graph.setdefault(a, {})[b] = t
            graph.setdefault(b, {})[a] = t   
        if int(source_id) not in graph or int(dest_id) not in graph:
            return render(request, 'base/home.html', {
                'stations': stations,
                'error': 'Selected station is not connected in the network'
            })
        path_ids, total_time = dijkstra(graph, int(source_id), int(dest_id)) #mapping algo called
        path_names = [
            Station.objects.get(station_id=i).station_name
            for i in path_ids
        ]

        # fare logic!!!!
        if len(path_ids)>=0 and len(path_ids)<=2:
            fare = 10
        elif len(path_ids)>=3 and len(path_ids)<=5:
            fare = 20
        elif len(path_ids)>=6 and len(path_ids)<=12:
            fare = 30
        elif len(path_ids)>=13 and len(path_ids)<=21:
            fare = 40
        elif len(path_ids)>=22 and len(path_ids)<=32:
            fare = 50
        else:
            fare = 60

        return render(request, 'base/home.html', {
            'stations': stations,
            'path': path_names,
            'time': total_time,
            'fare': fare
        })

    return render(request, 'base/home.html', {'stations': stations})

def fare(request):
    stations = Station.objects.all()

    if request.method == "POST":
        source_id = request.POST.get('source')
        dest_id = request.POST.get('destination')
        source = Station.objects.filter(station_id=source_id).first()
        destination = Station.objects.filter(station_id=dest_id).first()

        if not source or not destination:
            return render(request, 'base/fare.html', {
                        'stations': stations,
                        'error': 'Invalid station selected. Please try again.'
                        })
        if source_id == dest_id:
            return render(request, 'base/fare.html', {
                        'stations': stations,
                        'error': 'Source and destination cannot be the same!'
                        })
        graph = {}

        connections = StationConnection.objects.all()

        for conn in connections:
            a = conn.from_station.station_id
            b = conn.to_station.station_id
            t = conn.travel_time_minutes   # using time as weight

            graph.setdefault(a, {})[b] = t
            graph.setdefault(b, {})[a] = t   
        if int(source_id) not in graph or int(dest_id) not in graph:
            return render(request, 'base/fare.html', {
                'stations': stations,
                'error': 'Selected station is not connected in the network'
            })
        path_ids, total_time = dijkstra(graph, int(source_id), int(dest_id)) #mapping algo called
        path_names = [
            Station.objects.get(station_id=i).station_name
            for i in path_ids
        ]

        stops = len(path_ids)

        # fare logic!!!!
        if stops <= 2:
            token_fare = 10
        elif stops <= 5:
            token_fare = 20
        elif stops <= 12:
            token_fare = 30
        elif stops <= 21:
            token_fare = 40
        elif stops <= 32:
            token_fare = 50
        else:
            token_fare = 60

        smartcard_fare = round(token_fare * 0.9)

        return render(request, 'base/fare.html', {
                'stations': stations,
                'path': path_names,
                'token_fare': token_fare,
                'smartcard_fare': smartcard_fare
                })
    return render(request, 'base/fare.html', {
    'stations': stations
    })

def routemap(request):
    return render(request, 'base/route.html')

def timings(request):
    stations = Station.objects.all()

    if request.method == "POST":
        station_id = request.POST.get('station')
        station = Station.objects.filter(pk=station_id).first()

        timings = TrainTiming.objects.filter(station=station)

        return render(request, 'base/timings.html', {
            'stations': stations,
            'timings': timings,
            'station': station
        })

    return render(request, 'base/timings.html', {'stations': stations})

def parkings(request):
    stations = Station.objects.all()

    if request.method == "POST":
        station_id = request.POST.get('station')
        station = Station.objects.filter(pk=station_id).first()

        parking = Parking.objects.filter(station=station).first()

        return render(request, 'base/parkings.html', {
            'stations': stations,
            'parking': parking,
            'station': station
        })

    return render(request, 'base/parkings.html', {'stations': stations})

def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base/feedback.html', {
                'form': FeedbackForm(),
                'success': 'Feedback submitted successfully!' 
            })
    else:
        form = FeedbackForm()
    return render(request, 'base/feedback.html',{'form':form})

def gatesdir(request):
    stations = Station.objects.all()

    if request.method == "POST":
        station_id = request.POST.get('station')
        station = Station.objects.filter(pk=station_id).first()

        gates = StationGate.objects.filter(station=station)

        return render(request, 'base/gates.html', {
            'stations': stations,
            'gates': gates,
            'station': station
        })

    return render(request, 'base/gates.html', {'stations': stations})