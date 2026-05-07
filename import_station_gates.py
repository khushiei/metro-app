import sqlite3
import csv

print("Connecting to database...")
# Connect to your existing database (db.sqlite3 must be in the same folder)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("Opening station_gates.csv...")
# Read the CSV and insert the data
with open('/Users/dhruvyadav/Downloads/grproj-main_n+k/data/station_gates.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    count = 0
    for row in csv_reader:
        cursor.execute('''
        INSERT INTO base_stationgate (gate_id, station_id, gate_number, direction_description, nearby_landmark)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            int(row['gate_id']), 
            int(row['station']),           # 'station' in CSV maps to 'station_id' in the DB
            row['gate_number'], 
            row['direction_description'], 
            row['nearby_landmark']
        ))
        count += 1

print(f"Attempting to insert {count} rows...")

# Save and close
conn.commit()
conn.close()

print("Data successfully imported into db.sqlite3!")