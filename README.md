R.A.V.E.N (Risk Assessment and Vulnerability Enumeration)

R.A.V.E.N is a robust tool crafted for penetration testers and cybersecurity professionals. It enhances security analysis workflows by automating the extraction of services and versions from .nmap scan files, querying a SQLite database for CVE vulnerabilities based on those services, and generating comprehensive PDF reports detailing the identified vulnerabilities. R.A.V.E.N is designed to streamline the vulnerability assessment process, making it more efficient and effective.
Features

    Service Identification: Parses .nmap scan files to detect services and their versions.
    CVE Search: Queries a SQLite database for CVE vulnerabilities that match the identified services.
    Report Generation: Produces detailed PDF reports, summarizing the vulnerabilities, including CVE IDs, descriptions, and CVSS scores.

Installation
Prerequisites

    Python 3.x
    CVE JSON 5.0 format: Download main.zip from CVE Downloads
    sqlite3
    re (included in Python standard library)
    reportlab

Setup Steps

    Ensure Python 3.x is installed on your system.
    Install ReportLab using pip:

    bash

    pip install reportlab

    Clone or download the R.A.V.E.N repository to your local machine.

Preparing the CVE Database

To enable CVE search functionality, follow these steps to download CVE data and prepare the SQLite database:

    Download and Extract CVE Data: Obtain the main.zip from CVE Downloads, focusing on the CVE JSON 5.0 format.
    Database Setup: Create RAVEN_CVE_Vuln.db using SQLite3 and define a table structure suitable for storing CVE information.
    Populate Database: Develop a script or manually input the CVE data into the database, ensuring each entry includes a CVE ID, description, and CVSS score.

Making R.A.V.E.N Accessible in Bash

Enhance usability by adding R.A.V.E.N to the system's PATH or creating a bash alias:
Adding to PATH

    Open .bashrc or .bash_profile and append:

    bash

export PATH=$PATH:/path/to/raven

Reload the configuration:

bash

    source ~/.bashrc

Creating a Bash Alias

    In .bashrc or .bash_profile, add:

    bash

    alias raven='python /path/to/raven.py'

    Reload the file to apply changes.

Suggested Nmap Scans

Optimize R.A.V.E.N's effectiveness with comprehensive Nmap scans:

    Basic Scan: nmap -sV -sC -T4 -Pn -oN your_output_file.nmap target (Ranking: 8/10)

Additional Nmap Scan Options

    Full Port Scan: nmap -p- -sV -sC -T4 -oN full_scan_with_scripts.nmap target (9/10)
    Aggressive Scan: nmap -A -T4 -oN aggressive_scan.nmap target (7/10)
    UDP Scan: nmap -sU -sV -oN udp_scan.nmap target (6/10)
    Stealth Scan: nmap -sS -sV -sC --version-intensity 5 -T2 -oN stealth_scan.nmap target (8/10)

Usage

    Prepare your .nmap scan file.
    Ensure RAVEN_CVE_Vuln.db is populated with CVE data.
    Execute R.A.V.E.N:

    bash

    python raven.py

    Follow prompts to specify the .nmap file and report output directory.

Target Audience

R.A.V.E.N is tailored for penetration testers, cybersecurity researchers, and IT professionals conducting security analysis and vulnerability assessments. It is intended for ethical and legal use.
Contribution

Contributions are welcomed. For improvements or bug fixes, fork the repository, implement changes, and submit a pull request.
License
MIT License

Disclaimer

R.A.V.E.N is developed for educational and ethical testing purposes. The developers are not liable for misuse or damages
