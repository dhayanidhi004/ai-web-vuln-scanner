# 🔐 AI-Powered Web Vulnerability Scanner

An AI-enhanced Web Vulnerability Scanner built using Flask, SQLAlchemy, and JavaScript that detects common web security issues and generates intelligent remediation suggestions based on OWASP guidelines.

This project simulates a lightweight VAPT (Vulnerability Assessment & Penetration Testing) tool with AI-based analysis and PDF reporting.

---

## 🌐 Live Demo

🔗 Public Access Link:  
https://unsonorous-deborah-perioecic.ngrok-free.dev/

> ⚠️ Note: This demo link is hosted using ngrok and may become inactive if the server is offline.

---

## 🚀 Features

- 🔐 User Authentication (Signup/Login with Session Handling)
- 🧠 AI-Based Vulnerability Analysis
- 📊 Severity Classification (Critical, High, Medium, Low)
- 📚 OWASP Reference Mapping
- 📄 Downloadable PDF Scan Reports
- 📈 Interactive Dashboard
- 🗂 Scan History Storage (SQLite)
- 🌐 Public Deployment via ngrok

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- SQLAlchemy
- SQLite
- FPDF

### Frontend
- HTML
- CSS
- JavaScript

### Security Concepts Used
- Session-based authentication
- OWASP vulnerability categorization
- Basic VAPT simulation logic
- Secure cookie handling

---

## 📂 Project Structure

```
ai-web-vuln-scanner/
│
├── backend/
│   ├── app.py
│   ├── scanner.py
│   ├── ai_engine.py
│   ├── database.py
│   └── requirements.txt
│
├── frontend/
│   ├── login.html
│   ├── signup.html
│   ├── index.html
│   ├── dashboard.js
│   └── style.css
│
├── README.md
└── .gitignore
```

---

## ⚙️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-web-vulnerability-scanner.git
cd ai-web-vuln-scanner
```

### 2️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3️⃣ Run Application

```bash
cd backend
python app.py
```

App runs at:
```
http://127.0.0.1:8000
```

---

## 🌍 Public Demo via ngrok

```bash
ngrok http 8000
```

---

## 📊 How It Works

1. User logs in via session authentication.
2. User submits a target URL.
3. `scanner.py` performs vulnerability checks.
4. `ai_engine.py` generates intelligent analysis and remediation advice.
5. Results are categorized by severity.
6. PDF report can be generated and downloaded.
7. Scan history is stored in SQLite database.

---

## 🎯 Learning Outcomes

- Flask backend architecture
- Secure session management
- REST API integration
- Frontend-backend communication
- Basic VAPT workflow simulation
- AI-based vulnerability reporting logic

---

## 🔒 Future Improvements

- Password hashing (bcrypt)
- JWT authentication
- Real-time vulnerability scanning engine
- Deployment on Render / Railway
- Docker containerization
- Role-based access control (Admin/User)
- Advanced vulnerability detection modules

---

## 👨‍💻 Author

**Dhayanidhi S**  
AIML Student | Cybersecurity Enthusiast | VAPT Intern  

📌 Skills: Python, SQL, Flask, JavaScript, Burp Suite, Nmap  
📌 LinkedIn: https://www.linkedin.com/in/dhayanidhi-s-349705255/

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub!
