import os
import json
import sqlite3

def extract_cve_data(json_data):
    cve_id = json_data.get('cveMetadata', {}).get('cveId', '')
    description = json_data.get('containers', {}).get('cna', {}).get('descriptions', [{}])[0].get('value', '')
    cvss_score = json_data.get('containers', {}).get('cna', {}).get('metrics', [{}])[0].get('cvssV3_1', {}).get('baseScore', '')
    return cve_id, description, cvss_score

def create_cve_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cve_data (
                        id INTEGER PRIMARY KEY,
                        cve_id TEXT,
                        description TEXT,
                        cvss_score TEXT
                    )''')
    conn.commit()
    conn.close()

def insert_cve_data(db_name, data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO cve_data (cve_id, description, cvss_score)
                           VALUES (?, ?, ?)''', data)
    conn.commit()
    conn.close()

def scan_directory(directory):
    cve_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                cve_files.append(os.path.join(root, file))
    return cve_files

def main():
    directory = input("Enter the directory path to scan recursively: ")
    db_name = 'RAVEN_CVE_Vuln.db'
    
    print("Creating SQLite database and table...")
    create_cve_table(db_name)
    print("Database and table created successfully.")

    print("Scanning directory for JSON files...")
    cve_files = scan_directory(directory)
    print(f"Found {len(cve_files)} JSON files.")

    all_cve_data = []
    total_files = len(cve_files)

    for index, file in enumerate(cve_files, start=1):
        print(f"Processing file {index}/{total_files}: {file}")
        try:
            with open(file, 'r') as f:
                json_data = json.load(f)
                if isinstance(json_data, list):
                    for data in json_data:
                        cve_data = extract_cve_data(data)
                        all_cve_data.append(cve_data)
                else:
                    cve_data = extract_cve_data(json_data)
                    all_cve_data.append(cve_data)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    print("Inserting data into SQLite database...")
    insert_cve_data(db_name, all_cve_data)
    print("Data insertion into SQL table completed.")

if __name__ == "__main__":
    main()
