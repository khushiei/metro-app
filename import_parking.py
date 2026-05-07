import sqlite3
import csv

print("Connecting to database...")
# Connect to your existing database (db.sqlite must be in the same folder)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("Opening parking.csv...")
# Read the CSV and insert the data
with open('/Users/dhruvyadav/Downloads/grproj-main_n+k/data/parking.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    count = 0
    for row in csv_reader:
        cursor.execute('''
        INSERT INTO base_parking (parking_id, station_id, total_slots, parking_fee_per_hour)
        VALUES (?, ?, ?, ?)
        ''', (
            int(row['parking_id']), 
            int(row['station']),           # 'station' in CSV maps to 'station_id' in DB
            int(row['total_slots']), 
            float(row['parking_fee_per_hour']) 
        ))
        count += 1

print(f"Attempting to insert {count} rows...")

# Save and close
conn.commit()
conn.close()

print("Data successfully imported into db.sqlite!")