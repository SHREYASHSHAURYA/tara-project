# TARA – AI Loan Assistant

A complete loan‑assistant system with a FastAPI backend and a custom HTML/CSS/JS chat interface. Users can enter loan details, validate PAN, check eligibility, react to messages, switch themes, and download a sanction letter (PDF).

## Project Structure
```
tara-project/
│
├── tara-ai/          # Backend
│   └── main.py
│
└── tara-ui/          # Frontend
    └── index.html
```

## Backend (FastAPI)

### Run the server
```
cd tara-project/tara-ai
uvicorn main:app --reload
```

Runs at:
```
http://127.0.0.1:8000
```

### Endpoints
| Method | Route                | Description |
|--------|-----------------------|-------------|
| POST   | /chat                | Loan workflow + messages |
| GET    | /download-sanction   | Returns sanction letter PDF |

## Frontend (HTML/CSS/JS)

Launch the UI by opening:
```
tara-project/tara-ui/index.html
```

### UI Features
- Chat interface  
- Dark/light mode toggle  
- Message timestamps (aligned left/right)  
- Auto‑clickable links  
- Reaction menu (👍 ❤️ 😂 😮 😢) — one reaction per message  
- Smooth bubble alignment  
- Typing indicator  

Communicates with backend via:
```javascript
fetch("http://127.0.0.1:8000/chat", { ... })
```

## Loan Flow
1. User enters loan amount  
2. Enters salary  
3. Enters PAN  
4. Backend checks:
   - PAN format  
   - Loan ≤ 20× salary  
   - Minimum income requirement  
5. If eligible → generate sanction letter (PDF)

## Sanction Letter (PDF)
Generated via ReportLab. Includes:
- Loan amount  
- Salary  
- PAN  
- Terms & conditions  

Downloaded via:
```
/download-sanction
```

## Tech Stack
### Backend
- Python  
- FastAPI  
- Uvicorn  
- ReportLab  

### Frontend
- HTML  
- CSS  
- JavaScript  

## How to Run Entire Project

### 1️⃣ Start Backend
```
cd tara-project/tara-ai
uvicorn main:app --reload
```

### 2️⃣ Start Frontend
Open:
```
tara-project/tara-ui/index.html
```

## Future Improvements
- Stronger underwriting logic  
- Chat history storage  
- Deployment to cloud  
- UI animations  
- Login + dashboard  
