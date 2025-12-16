# **TARA – AI Loan Assistant**
A complete loan‑assistant system with:
- FastAPI backend
- Interactive chat UI
- Login + Signup system
- Session handling (localStorage)
- Dark/Light mode
- Glass UI + animations
- Logout system
- PDF sanction letter generation
- Full underwriting workflow

------------------------------------------------------------

# **PROJECT STRUCTURE**

tara-project/
│
├── tara-ai/                (Backend – FastAPI)
│     main.py
│     users.json
│     sanction_letter.pdf
│
└── tara-ui/                (Frontend – HTML/CSS/JS)
      index.html
      login.html
      signup.html

------------------------------------------------------------

# **BACKEND (FASTAPI)**

## **Run Backend**
cd tara-project/tara-ai  
python -m uvicorn main:app --reload

Backend runs at:  
http://127.0.0.1:8000

------------------------------------------------------------

# **API ENDPOINTS**

POST /login               → user login  
POST /signup              → user signup  
POST /chat                → loan workflow  
GET  /download-sanction   → returns sanction PDF  

------------------------------------------------------------

# **FRONTEND**

Start frontend by opening:  
tara-project/tara-ui/login.html

After login → redirects to index.html

------------------------------------------------------------

# **UI FEATURES**

- Glassmorphism animated UI  
- Floating + glow effects  
- Login & Signup pages  
- Session handling  
- Logout button  
- Dark/Light theme toggle  
- Chat UI supports:
  - timestamps  
  - clickable links  
  - reaction bar (👍 ❤️ 😂 😮 😢)  
  - auto‑scroll  
  - smooth alignment  
  - typing flow  

fetch request used:  
fetch("http://127.0.0.1:8000/chat")

------------------------------------------------------------

# **AUTHENTICATION FLOW**

**Signup** → stored in users.json  
**Login** → sets:  
localStorage.setItem("loggedIn", "true")

**Index page protection:**  
if (!localStorage.getItem("loggedIn")) redirect to login.html

**Logout:**  
localStorage.removeItem("loggedIn")  
redirect to login.html

------------------------------------------------------------

# **LOAN FLOW**

1. Enter loan amount  
2. Enter salary  
3. Enter PAN  
4. Backend checks:
   - PAN format  
   - Salary ≥ 20000  
   - Loan ≤ salary × 20  
5. If approved → generates sanction PDF  

------------------------------------------------------------

# **PDF SANCTION LETTER**

Generated using ReportLab. Contains:
- Loan amount  
- Salary  
- PAN  
- Terms & Conditions  

Download URL:  
http://127.0.0.1:8000/download-sanction

------------------------------------------------------------

# **TECH STACK**

**Backend**
- Python  
- FastAPI  
- Uvicorn  
- ReportLab  

**Frontend**
- HTML  
- CSS  
- JavaScript  

------------------------------------------------------------

# **HOW TO RUN EVERYTHING**

## **Start Backend**
cd tara-project/tara-ai  
python -m uvicorn main:app --reload

## **Start Frontend**
Open tara-ui/login.html in browser

------------------------------------------------------------

# **FUTURE IMPROVEMENTS**

- Email OTP verification  
- Database integration  
- Stronger underwriting logic  
- Deployment (Render / Netlify / Vercel)  
- Dashboard + analytics  
