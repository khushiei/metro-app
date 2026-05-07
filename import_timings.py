import sqlite3
import csv
import traceback
import os

def run_import():
    try:
        print("Connecting to database...")
        # 1. Ensure absolute path to db and csv
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'db.sqlite3')
        csv_path = '/Users/dhruvyadav/Downloads/grproj-main_n+k/data/train_timings.csv'
        
        if not os.path.exists(db_path):
            print(f"ERROR: Cannot find database at {db_path}")
            return
            
        if not os.path.exists(csv_path):
            print(f"ERROR: Cannot find CSV at {csv_path}")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 2. Build mapping of MetroLine names to IDs (to fix Foreign Key errors)
        print("Fetching Metro Lines to map IDs...")
        line_mapping = {}
        try:
            cursor.execute("SELECT line_id, line_name FROM base_metroline")
            for db_row in cursor.fetchall():
                line_mapping[db_row[1]] = db_row[0]
        except sqlite3.OperationalError as e:
            print("\nERROR: Table 'base_metroline' does not exist.")
            print("Did you forget to run 'python manage.py makemigrations' and 'python manage.py migrate'?")
            return

        print(f"Opening {csv_path}...")
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            count = 0
            for row in csv_reader:
                line_name = row['line']
                actual_line_id = line_mapping.get(line_name)
                
                if actual_line_id is None:
                    print(f"Warning: Line '{line_name}' not found in DB. Skipping row.")
                    continue

                # 3. Insert data securely
                cursor.execute('''
                INSERT INTO base_traintiming (timing_id, station_id, line_id, first_train_time, last_train_time, frequency_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['timing_id']), 
                    int(row['station']), 
                    actual_line_id,         # Uses mapped integer (e.g., 1) instead of text (e.g., "Blue Line")
                    row['first_train_time'], 
                    row['last_train_time'], 
                    int(row['frequency_minutes'])
                ))
                count += 1

        print(f"Attempting to commit {count} rows to the database...")
        conn.commit()
        conn.close()

        print("\nSUCCESS! Data successfully imported into db.sqlite3!")

    except sqlite3.OperationalError as e:
        print("\nDATABASE ERROR:")
        print(e)
        print("\nDid you run makemigrations and migrate? Is your app actually named 'base'?")
    except sqlite3.IntegrityError as e:
        print("\nDATA INTEGRITY ERROR:")
        print(e)
        print("\nThis usually means a Foreign Key ID from the CSV doesn't exist in the database.")
    except Exception as e:
        print("\nUNEXPECTED ERROR OCCURRED:")
        traceback.print_exc()

if __name__ == "__main__":
    run_import()
    # Prevents terminal from closing instantly
    input("\nPress Enter to exit...")