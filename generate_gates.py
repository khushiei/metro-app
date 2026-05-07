import pandas as pd
import random

# Read the uploaded stations data
stations_df = pd.read_csv('/Users/dhruvyadav/Downloads/grproj-main_n+k/data/stations.csv')

gate_data = []
gate_id_counter = 1

# Mock options for descriptions and landmarks
directions = [
    "Towards Main Road", "Towards Residential Area", 
    "Towards Commercial Hub", "Towards Bus Stand",
    "Towards North Block", "Towards South Block",
    "Towards East Avenue", "Towards West Avenue"
]
landmarks = [
    "City Mall", "Central Park", "Hospital", 
    "Local Market", "Bus Terminus", "Police Station", 
    "University", "Sports Complex", "PVR Cinemas",
    "Bank Branch", "Post Office"
]

# Using seed guarantees you get the exact same results every time
random.seed(42) 

for index, row in stations_df.iterrows():
    station_id = row['station_id']
    station_name = row['station_name']
    
    num_gates = random.randint(2, 4)
    
    for i in range(num_gates):
        gate_data.append({
            'gate_id': gate_id_counter,
            'station': station_id,
            'gate_number': str(i + 1),
            'direction_description': random.choice(directions),
            'nearby_landmark': f"{random.choice(landmarks)} near {station_name}"
        })
        gate_id_counter += 1

# Save the full data to CSV
gates_df = pd.DataFrame(gate_data)
gates_df.to_csv('station_gates.csv', index=False)
print("Success! station_gates.csv has been created with all 757 rows.")