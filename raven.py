import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def parse_nmap_file(file_path):
    """Parse an .nmap scan file to extract services and their versions."""
    services = []
    with open(file_path, 'r') as file:
        for line in file:
            if "/tcp" in line and "open" in line:
                parts = line.split()
                service_name = parts[2]
                service_version = ' '.join(parts[3:]) if len(parts) > 3 else "unknown"
                services.append((service_name, service_version))
    return services

def search_cve_vulnerabilities(db_name, services):
    """Search the database for CVE vulnerabilities based on service names and versions."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cve_data = []

    for service_name, service_version in services:
        search_patterns = [
            f"%{service_name}%",
            f"%{service_version}%",
        ]
        
        for pattern in search_patterns:
            cursor.execute("SELECT cve_id, description, cvss_score FROM cve_data WHERE description LIKE ?", (pattern,))
            results = cursor.fetchall()
            cve_data.extend(results)
    
    conn.close()
    return cve_data

def generate_pdf_report_with_reportlab_improved(services, cve_data, output_file_path):
    doc = SimpleDocTemplate(output_file_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Wrapped', wordWrap='LTR', fontSize=8, leading=10))

    elements = []

    # Header, could be replaced with a more dynamic approach
    elements.append(Paragraph('R.A.V.E.N Scan Report', styles['Title']))
    elements.append(Spacer(1, 12))

    # Summary Section
    summary_text = f'Total Services Scanned: {len(services)}, Vulnerabilities Found: {len(cve_data)}'
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Services Listing
    if services:
        for service_name, additional_info in services:
            service_text = f"Service: {service_name}, Version/Info: {additional_info}"
            elements.append(Paragraph(service_text, styles['Wrapped']))
            elements.append(Spacer(1, 6))

    # CVE Details
    if cve_data:
        for cve_id, description, cvss_score in cve_data:
            cve_text = f"CVE ID: {cve_id}, Description: {description}, CVSS Score: {cvss_score}"
            elements.append(KeepTogether([Paragraph(cve_text, styles['Wrapped']), Spacer(1, 6)]))

    doc.build(elements)

if __name__ == "__main__":
    nmap_file_path = input("Please enter the file path to your Nmap scan file (.nmap): ").strip()
    report_directory_path = input("Please enter the directory path where you want the PDF report to be saved: ").strip()
    report_file_path = f"{report_directory_path.rstrip('/')}/RAVEN_report.pdf"

    services = parse_nmap_file(nmap_file_path)
    db_name = "RAVEN_CVE_Vuln.db"
    cve_data = search_cve_vulnerabilities(db_name, services)
    
    generate_pdf_report_with_reportlab_improved(services, cve_data, report_file_path)
    print(f"Report generated and saved to: {report_file_path}")
