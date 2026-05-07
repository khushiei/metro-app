import sqlite3
import csv

print("Connecting to database...")
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Clear the table so we don't get duplicates on retry
cursor.execute('DELETE FROM base_stationconnection')

print("Opening connections.csv...")
# 'utf-8-sig' handles invisible characters often added by Excel or Notepad
with open('data/station_connections.csv', 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    
    count = 0
    for row in csv_reader:
        # Safely grab all values
        c_id = row.get('connection_id')
        f_id = row.get('from_station')
        t_id = row.get('to_station')
        time = row.get('travel_time_minutes')

        # Skip any completely blank rows
        if c_id is None or str(c_id).strip() == '':
            continue

        try:
            cursor.execute('''
            INSERT INTO base_stationconnection (connection_id, from_station_id, to_station_id, travel_time_minutes)
            VALUES (?, ?, ?, ?)
            ''', (
                int(c_id), 
                int(f_id), 
                int(t_id), 
                int(time)
            ))
            count += 1
            
        except TypeError:
            # If it STILL crashes, it will print exactly what caused the crash instead of failing silently
            print(f"\nCRASHED ON THIS ROW: {row}")
            print(f"Values it tried to read -> ID:{c_id}, From:{f_id}, To:{t_id}, Time:{time}\n")
            break

print(f"Successfully inserted {count} rows.")
conn.commit()
conn.close()