R.A.V.E.N (Risk Assessment and Vulnerability Enumeration)

R.A.V.E.N is a powerful tool designed for penetration testers and cybersecurity professionals. It streamlines the process of parsing .nmap scan files to extract services and their versions, querying a database for CVE vulnerabilities based on those services, and generating detailed PDF reports. This tool is crafted to enhance the efficiency of security analysis workflows.
Features

    Parses .nmap scan files to identify services and their versions.
    Searches a SQLite database for CVE vulnerabilities matching identified services.
    Generates comprehensive PDF reports detailing the vulnerabilities, including CVE IDs, descriptions, and CVSS scores.

Installation
Prerequisites

R.A.V.E.N requires Python 3.x and the following dependencies:

    sqlite3
    re
    reportlab

Steps

    Ensure Python 3.x is installed on your system.
    Install ReportLab:

    bash

    pip install reportlab

    Clone or download the R.A.V.E.N repository to your local machine.

Making R.A.V.E.N Easily Accessible in Bash

To run R.A.V.E.N from any directory without having to specify the full path to the script, you can add it to your system's PATH or create a bash alias.
Adding to PATH

    Open your .bashrc or .bash_profile file in your home directory:

    bash

nano ~/.bashrc

Add the following line at the end of the file, replacing /path/to/raven with the actual path to the R.A.V.E.N directory:

bash

export PATH=$PATH:/path/to/raven

Save and close the file, then reload .bashrc or .bash_profile:

bash

    source ~/.bashrc

Creating a Bash Alias

Alternatively, you can create a bash alias for R.A.V.E.N:

    Open your .bashrc or .bash_profile file:

    bash

nano ~/.bashrc

Add the following alias, replacing /path/to/raven.py with the actual path to the R.A.V.E.N script:

bash

alias raven='python /path/to/raven.py'

Save and close the file, then reload it:

bash

    source ~/.bashrc

Now, you can simply type raven in your terminal to run the script from anywhere.
Suggested Nmap Scan

    Basic scan for version detection: nmap -sV -sC -T4 -Pn -oN your_output_file.nmap target (Ranking: 8/10)

Additional Nmap Scan Options
Full Port Scan with Version Detection and Script Scanning

    Command: nmap -p- -sV -sC -T4 -oN full_scan_with_scripts.nmap target
    Ranking: 9/10

Aggressive Scan with OS Detection

    Command: nmap -A -T4 -oN aggressive_scan.nmap target
    Ranking: 7/10

UDP Scan for Detecting UDP Services

    Command: nmap -sU -sV -oN udp_scan.nmap target
    Ranking: 6/10

Stealth Scan for Sensitive Environments

    Command: nmap -sS -sV -sC --version-intensity 5 -T2 -oN stealth_scan.nmap target
    Ranking: 8/10

Usage

To use R.A.V.E.N:

    Prepare your .nmap scan file and ensure your SQLite database (RAVEN_CVE_Vuln.db) is populated with the relevant CVE data.
    Run R.A.V.E.N from the command line:

    bash

    python raven.py

    Follow the prompts to enter the path to your .nmap file and specify the directory where the PDF report should be saved.

Target Audience

R.A.V.E.N is intended for penetration testers, cybersecurity researchers, and IT professionals engaged in security analysis and vulnerability assessments. It is designed to be used for ethical, legal purposes only.
Contribution

Contributions to R.A.V.E.N are welcome! If you have suggestions for improvements or bug fixes, please feel free to fork the repository, make your changes, and submit a pull request.
License

[Specify the license under which R.A.V.E.N is released, e.g., MIT, GPL, etc.]
Disclaimer

R.A.V.E.N is developed for educational and ethical testing purposes only. The developers assume no liability for any misuse or damage caused by this program. Use it at your own risk.
Acknowledgments

    Thanks to the open-source community for the invaluable resources and support.
