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
        """, (
            cve_record.get("cve_id"), 
            cve_record.get("state"), 
            cve_record.get("assigner_org_id"),
            cve_record.get("date_published"), 
            cve_record.get("description"), 
            cve_record.get("cvss_score", "Unknown"),
            cve_record.get("service_name"), 
            cve_record.get("service_version")
        ))
        conn.commit()
    finally:
        conn.close()

def log_unprocessed_files(file_path, reason):
    with open("unprocessed_files.log", "a") as log_file:
        log_file.write(f"{file_path}: {reason}\n")

def process_json_file(file_path, db_path="RAVEN_CVE_Vuln.db"):
    cve_record = {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        cveMetadata = data.get("cveMetadata", {})
        descriptions = data.get("containers", {}).get("cna", {}).get("descriptions", [])
        description = descriptions[0].get("value") if descriptions else None
        
        cve_record = {
            "cve_id": cveMetadata.get("cveId"),
            "state": cveMetadata.get("state"),
            "assigner_org_id": cveMetadata.get("assignerOrgId"),
            "date_published": cveMetadata.get("datePublished"),
            "description": description,
            "cvss_score": "Unknown",  # Update this as necessary
        }
        
        # At this point, we attempt to insert whatever data we've managed to extract.
        insert_cve_data(db_path, cve_record)
        print(f"Processed: {file_path}")
        
    except json.JSONDecodeError:
        reason = "Failed to decode JSON"
        log_unprocessed_files(file_path, reason)
    except Exception as e:
        reason = str(e)
        log_unprocessed_files(file_path, reason)
    finally:
        # If any key expected is missing, log this file for further review.
        missing_keys = [key for key in ["cve_id", "state", "assigner_org_id", "date_published", "description"] if key not in cve_record or not cve_record[key]]
        if missing_keys:
            log_unprocessed_files(file_path, f"Missing data for keys: {', '.join(missing_keys)}")

def scan_directories_and_process_jsons(root_dir, db_path="RAVEN_CVE_Vuln.db"):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                process_json_file(file_path, db_path)

if __name__ == "__main__":
    root_dir = input("Enter the root directory to scan for JSON files: ").strip()
    create_db()  # Ensures the database and tables are set up
    scan_directories_and_process_jsons(root_dir)
    print("Completed scanning directories and processing JSON files.")
