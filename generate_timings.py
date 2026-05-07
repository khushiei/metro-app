import pandas as pd
import random

random.seed(42)
stations_df = pd.read_csv('/Users/dhruvyadav/Downloads/grproj-main_n+k/data/stations.csv')

timings = []
timing_id = 1

for _, row in stations_df.iterrows():
    # Randomize first train time
    h_first = 5
    m_first = random.choice([0, 10, 15, 20, 30, 40, 45])
    first_time = f"{h_first:02d}:{m_first:02d}:00"
    
    # Randomize last train time
    h_last = 23
    m_last = random.choice([0, 15, 30, 40, 45, 50, 55])
    last_time = f"{h_last:02d}:{m_last:02d}:00"
    
    # Randomize frequency
    freq = random.choice([3, 4, 5, 6, 8, 10])
    
    timings.append({
        'timing_id': timing_id,
        'station': row['station_id'],
        'line': row['line'],  
        'first_train_time': first_time,
        'last_train_time': last_time,
        'frequency_minutes': freq
    })
    timing_id += 1
    
timings_df = pd.DataFrame(timings)
timings_df.to_csv('train_timings.csv', index=False)
print(f"Success! Created train_timings.csv with {len(timings_df)} rows.")