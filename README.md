# 💊 DoseSafe — Medicine Combination Checker

> **Check medicine combinations. Understand potential interactions. Make informed decisions.**

DoseSafe is a **Django-based medicine combination checker** that allows users to search for medicines and check whether a combination has a known interaction according to the application's curated database.

The project is designed as an educational healthcare application demonstrating **Django, Python, database relationships, authentication, and backend logic**.

> ⚠️ **Medical Disclaimer:** DoseSafe is an educational/informational project. It does not provide medical diagnosis or treatment advice and should not be used as a substitute for a doctor or pharmacist. Users should consult a qualified healthcare professional before starting, stopping, or changing medicines.

---

## ✨ Features

### 🔐 User Authentication

* User registration
* Login and logout
* Personal medicine list
* User-specific search history

### 💊 Medicine Management

* Search medicines
* View medicine information
* Add medicines to a personal medicine cabinet
* Remove medicines from the cabinet

### 🔍 Combination Checker

* Select two or more medicines
* Check combinations against the interaction database
* Identify potentially documented interactions
* Display interaction severity
* Show an explanation of the interaction
* Provide a recommendation to consult a healthcare professional

### 📊 Interaction Results

The application categorizes results such as:

| Result                   | Meaning                                                  |
| ------------------------ | -------------------------------------------------------- |
| 🟢 No interaction listed | No interaction is recorded in the application's database |
| 🟡 Caution               | The combination may require professional review          |
| 🔴 Interaction listed    | A potentially significant interaction is recorded        |

**Note:** "No interaction listed" does not mean a combination is universally safe for every person.

### 🛠️ Admin Panel

Administrators can manage:

* Medicines
* Medicine categories
* Drug interactions
* Interaction severity
* Interaction descriptions
* Safety recommendations

---

# 🖥️ Application Flow

```text
                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Login / Signup  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Medicine Search  │
                  └────────┬─────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Select Medicines     │
                │ Medicine A + B + C   │
                └──────────┬───────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │ Interaction Engine  │
                 └──────────┬──────────┘
                            │
                  ┌─────────┼─────────┐
                  ▼         ▼         ▼
               No Match   Caution   Interaction
                  │         │         │
                  └─────────┼─────────┘
                            ▼
                   ┌─────────────────┐
                   │ Result + Advice │
                   └─────────────────┘
```

---

# 🧠 How the Combination Checker Works

When the user selects multiple medicines, DoseSafe checks the selected medicines against the application's interaction database.

For example:

```text
Medicine A
     +
Medicine B
     ↓
Interaction Database
     ↓
Match Found?
     ↓
Yes → Display interaction information
No  → Display no interaction listed
```

For multiple medicines, the system can evaluate combinations pair-by-pair:

```text
A + B
A + C
B + C
```

This demonstrates practical use of **Django ORM relationships and backend business logic**.

---

# 🗄️ Database Structure

The project can use the following core models:

```text
User
 │
 ├── UserMedicine
 │
 └── SearchHistory


Medicine
 │
 ├── name
 ├── generic_name
 ├── category
 └── description


Interaction
 │
 ├── medicine_1
 ├── medicine_2
 ├── severity
 ├── description
 └── recommendation
```

### Example

```text
Medicine
   │
   ├── Paracetamol
   ├── Ibuprofen
   └── Amoxicillin

Interaction
   │
   ├── Medicine 1
   ├── Medicine 2
   ├── Severity
   └── Description
```

---

# 🛠️ Technology Stack

### Backend

* **Python**
* **Django**
* **Django ORM**

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap *(optional)*

### Database

* SQLite for development
* PostgreSQL for production

### Deployment

* AWS EC2
* Gunicorn
* Nginx

### Version Control

* Git
* GitHub

---

# 📁 Project Structure

```text
DoseSafe/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── medicines/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── interactions/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── services.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── medicines.html
│   └── results.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/dosesafe.git
cd dosesafe
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Create an admin user

```bash
python manage.py createsuperuser
```

## 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔑 Admin Panel

Django's built-in admin panel can be used to manage the medicine and interaction database.

```text
/admin/
```

Example:

```text
Medicine
├── Add Medicine
├── Edit Medicine
└── Delete Medicine

Interactions
├── Add Interaction
├── Edit Interaction
└── Delete Interaction
```

---

# 📸 Screenshots

Add screenshots of your application here after completing the project.

```text
## Login

![Login](screenshots/login.png)

## Dashboard

![Dashboard](screenshots/dashboard.png)

## Medicine Search

![Medicine Search](screenshots/search.png)

## Combination Result

![Interaction Result](screenshots/result.png)
```

---

# 🚀 Future Improvements

The project can be expanded with:

* [ ] Django REST Framework API
* [ ] PostgreSQL database
* [ ] Medicine autocomplete search
* [ ] Medicine reminder system
* [ ] Prescription document upload
* [ ] OCR-based medicine-name extraction
* [ ] Email notifications
* [ ] Doctor/pharmacist verification workflow
* [ ] AWS deployment
* [ ] Mobile-friendly UI
* [ ] Interaction database import/update system

---

# 🎯 Learning Objectives

This project demonstrates practical understanding of:

* Django project architecture
* Django models
* ForeignKey and Many-to-Many relationships
* Django ORM
* CRUD operations
* User authentication
* Form handling
* Backend business logic
* Database design
* Search functionality
* Admin panel
* Git/GitHub
* Deployment concepts

---

# ⚠️ Disclaimer

DoseSafe is developed for **educational and software-development purposes**.

The interaction information displayed by the application depends on the application's underlying database and may be incomplete or outdated. The application does not diagnose medical conditions, prescribe medicines, or determine whether a medicine is appropriate for an individual.

**Always consult a qualified doctor or pharmacist before making decisions about medications.**



> **DoseSafe — Know the combination. Check before you act.**
