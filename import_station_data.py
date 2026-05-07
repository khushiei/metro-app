import sqlite3
import csv

print("Connecting to database...")
# Connect to your existing database (db.sqlite must be in the same folder)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("Opening stations.csv...")
# Read the CSV and insert the data
with open('data/stations.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    count = 0
    for row in csv_reader:
        cursor.execute('''
        INSERT INTO base_station (station_id, station_name, line_id, station_order, is_interchange)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            int(row['station_id']), 
            row['station_name'], 
            row['line'], 
            int(row['station_order']), 
            int(row['is_interchange'])  # Data is already 1/0 in the CSV
        ))
        count += 1

print(f"Attempting to insert {count} rows...")

# Save and close
conn.commit()
conn.close()

print("Data successfully imported into db.sqlite!")