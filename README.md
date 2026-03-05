# SkillMap – Role-Based Skill Assessment System

SkillMap is a Django-based web application that helps users evaluate their technical skills through structured assessments.
The system tracks skill progression, calculates readiness for specific roles, and provides insights into strengths and weaknesses.

---

## 🚀 Features

* User registration and authentication
* Role-based skill mapping
* Multi-level skill assessments
* Automatic score evaluation
* Skill progression tracking
* Role readiness calculation
* Assessment history and detailed review
* Dashboard showing weakest and strongest skills
* Clean UI for assessments and results

---

## 🛠 Tech Stack

**Backend**

* Python
* Django

**Database**

* MySQL

**Frontend**

* HTML
* CSS

---

## 📂 Project Structure

```
SkillMapProject
│
├── config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── skillmap
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   ├── admin.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/SkillMapProject.git
cd SkillMapProject
```

---

### 2️⃣ Create a virtual environment

```
python -m venv demo_env
```

Activate it:

**Windows**

```
demo_env\Scripts\activate
```

**Mac/Linux**

```
source demo_env/bin/activate
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Configure MySQL database

Update `config/settings.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skillmap_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Create the database in MySQL:

```
CREATE DATABASE skillmap_db;
```

---

### 5️⃣ Run migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Create admin user

```
python manage.py createsuperuser
```

---

### 7️⃣ Run the server

```
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 📊 How It Works

1. Users register and log in.
2. Users select roles they want to prepare for.
3. Each role has multiple required skills.
4. Skills contain assessment questions with difficulty levels.
5. After completing assessments, the system:

   * Calculates the score
   * Determines skill level
   * Updates role readiness
6. The dashboard visualizes progress and highlights improvement areas.

---

## 📈 Future Improvements

* REST API integration
* React frontend
* Skill progress charts
* AI-based skill recommendations
* Leaderboard and gamification
* Deployment to cloud (Render / AWS)

---

## 👨‍💻 Author

Fil
Full Stack Developer (Python / Django / React)

---

## 📜 License

This project is for educational and portfolio purposes.
