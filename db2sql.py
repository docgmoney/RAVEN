import os
import json
import sqlite3

def create_db(db_path="RAVEN_CVE_Vuln.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cve_data (
            id INTEGER PRIMARY KEY,
            cve_id TEXT UNIQUE,
            state TEXT,
            assigner_org_id TEXT,
            date_published DATE,
            description TEXT,
            cvss_score TEXT DEFAULT 'Unknown',
            service_name TEXT,
            service_version TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert_cve_data(db_path, cve_record):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cve_data (cve_id, state, assigner_org_id, date_published, description, cvss_score, service_name, service_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(cve_id) DO UPDATE SET
                state=excluded.state,
                assigner_org_id=excluded.assigner_org_id,
                date_published=excluded.date_published,
                description=excluded.description,
                cvss_score=excluded.cvss_score,
                service_name=excluded.service_name,
                service_version=excluded.service_version;
        """, (cve_record["cve_id"], cve_record["state"], cve_record["assigner_org_id"],
              cve_record["date_published"], cve_record["description"], cve_record["cvss_score"],
              cve_record.get("service_name"), cve_record.get("service_version")))
        conn.commit()
    finally:
        conn.close()

def process_json_file(file_path, db_path="RAVEN_CVE_Vuln.db"):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Assuming a single CVE per file structure based on your provided JSON example
    cve_record = {
        "cve_id": data["cveMetadata"]["cveId"],
        "state": data["cveMetadata"]["state"],
        "assigner_org_id": data["cveMetadata"]["assignerOrgId"],
        "date_published": data["cveMetadata"]["datePublished"],
        "description": data["containers"]["cna"]["descriptions"][0]["value"],
        "cvss_score": "Unknown",  # Placeholder, adapt as needed
        # "service_name" and "service_version" would require additional logic to extract
    }

    insert_cve_data(db_path, cve_record)

def scan_directories_and_process_jsons(root_dir, db_path="RAVEN_CVE_Vuln.db"):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    process_json_file(file_path, db_path)
                    print(f"Processed: {file_path}")
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    root_dir = input("Enter the root directory to scan for JSON files: ").strip()
    create_db()  # Ensures the database and tables are set up
    scan_directories_and_process_jsons(root_dir)  # Now this function is properly defined
    print("Completed scanning directories and processing JSON files.")
