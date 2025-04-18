# Mentorship & Research Collaboration Matching System

This project is a simple web-based system that allows users to create, browse, update, delete, and search for academic profiles to connect for mentorship or collaboration.

## Features
- Create a new profile with research interests and mentorship/collaboration roles
- Upload a custom headshot or use a default one
- View all profiles in a clean searchable table
- Search by:
  - Name, Position, Institution, Department
  - Mentorship/Collaboration intent
  - Research Interests
- Update or delete profiles by verifying your email
- Demo-ready with 11 dummy profiles + 1 live demo user to show create/update/delete/match

---

## How to Run This Project

### Requirements:
- Python 3.10+
- MySQL server
- Flask + MySQL bindings

---

### 1. Clone the Repo
```bash
git clone <repo-url>
cd mentorship_database
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv z_venv
source z_venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the MySQL Database
```bash
mysql -u root -p
```
Then inside the MySQL shell:
```sql
CREATE DATABASE mentorship_db;
EXIT;
```

### 5. Import Schema and Data
```bash
mysql -u root -p mentorship_db < sql/mentorship_db_backup.sql
```

### 6. Run the App
```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Notes
- Your virtual environment (`z_venv/`) should **not be submitted**
- All profile data and logic is already included in the backup
- Search logic is built for accurate multi-field and checkbox filtering

---

## Demo Tips
- Create a “live demo” user (`live.demo@email.com`) during your presentation
- Update that profile to show the edit functionality
- Delete it at the end to complete the loop

---