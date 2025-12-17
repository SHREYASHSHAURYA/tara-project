# 🚀 TARA – Intelligent Loan Assistant  
A full‑stack AI loan assistant with underwriting logic, PAN verification, profile management, and live chat interface.

---

## 📌 Features

### 🔹 **Frontend (HTML + JS)**
- Modern animated UI for login, signup, and chat  
- Profile page with editable user info  
- PAN verification indicator  
- Dark/light mode  
- Local session handling  
- Navigation sidebar  

### 🔹 **Backend (FastAPI)**
- `/signup` — register users with full profile  
- `/login` — authenticate users  
- `/profile/{email}` — fetch user profile  
- `/update-profile/{email}` — update user details  
- `/verify-pan/{email}` — mark PAN as verified  
- `/chat` — underwriting + conversation engine  
- `/download-sanction` — PDF generation  

### 🔹 **Storage**
- `users.json` used as a lightweight database  
- Auto-created if not present  

---

## 📁 Project Structure

```
tara-project/
│
├── index.html
├── login.html
├── signup.html
├── profile.html
├── verify.html
│
├── tara-ai/
│   ├── main.py
│   └── users.json
│
└── README.md
```

---

## ⚙️ Installation & Running the Backend

### 1️⃣ Install dependencies
```bash
pip install fastapi uvicorn reportlab pydantic
```

### 2️⃣ Run backend server
```bash
uvicorn main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

## 🌐 Frontend Setup

Just open **index.html** in a browser.  
Make sure all HTML files are in the same folder.

For navigation:
- `index.html` → main chat interface  
- `profile.html` → user profile  
- `verify.html` → PAN verification  

---

## 🔥 API Endpoints Summary

### **Authentication**
| Method | Endpoint | Purpose |
|--------|----------|----------|
| POST | `/signup` | Create new user |
| POST | `/login` | Login |

### **Profile**
| Method | Endpoint | Purpose |
|--------|----------|----------|
| GET | `/profile/{email}` | Fetch user profile |
| POST | `/update-profile/{email}` | Update name, city, bank, occupation |
| POST | `/verify-pan/{email}` | Mark PAN as verified |

### **AI Chat Engine**
| POST | `/chat` |
|------|----------|
| Runs underwriting flow, responds like TARA |

### **Sanction Letter**
| GET | `/download-sanction` |

---

## 🧠 Underwriting Logic (Summary)
- Minimum salary: **₹20,000**  
- Loan eligibility: **20 × salary**  
- PAN is validated via regex before underwriting  
- Generates PDF sanction letter if approved  

---

## ✔️ GitHub Usage (Now Working Clean)
Future updates require only:

```bash
git add .
git commit -m "update"
git push
```

---


