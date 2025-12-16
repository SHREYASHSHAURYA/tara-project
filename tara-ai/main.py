from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
import json, os, re

app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ USER AUTH STORAGE ------------------
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class SignupData(BaseModel):
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(data: SignupData):
    users = load_users()

    if data.email in users:
        raise HTTPException(400, "Email already registered.")

    users[data.email] = {"password": data.password}
    save_users(users)

    return {"message": "Signup successful!"}

@app.post("/login")
def login(data: LoginData):
    users = load_users()

    if data.email not in users:
        raise HTTPException(400, "User not found.")

    if users[data.email]["password"] != data.password:
        raise HTTPException(400, "Incorrect password.")

    return {"message": "Login successful"}


# ------------------ STATE ------------------
def reset_user():
    return {
        "stage": "intent",
        "loan_amount": None,
        "salary": None,
        "pan": None
    }

USER = reset_user()

class Message(BaseModel):
    text: str

# ---------------- UNDERWRITING ----------------
def run_underwriting():
    amount = int(USER["loan_amount"])
    salary = int(USER["salary"])

    if salary < 20000:
        return {"reply": "❌ Loan cannot be approved because salary is below ₹20,000."}

    if amount > salary * 20:
        max_allowed = salary * 20
        return {"reply": f"❌ Requested amount ₹{amount} is too high.\n"
                         f"Maximum allowed = ₹{max_allowed}."}

    return {
        "reply": f"🎉 Congratulations! Your loan of ₹{amount} is approved.\n"
                 "Would you like me to generate your sanction letter?"
    }

# ---------------- CHAT BOT ----------------
@app.post("/chat")
def chat(msg: Message):
    user_input = msg.text.strip()
    stage = USER["stage"]

    # ---------- Restart ----------
    if user_input.lower() in ["restart", "start", "hi", "hello"]:
        USER.update(reset_user())
        USER["stage"] = "loan_amount"
        return {"reply": "Hi, I'm TARA 😊 How much loan do you need?"}

    # ---------- Loan amount ----------
    if stage == "intent":
        USER["stage"] = "loan_amount"
        return {"reply": "How much loan do you need?"}

    if stage == "loan_amount":
        try:
            USER["loan_amount"] = int(user_input)
        except:
            return {"reply": "Enter loan amount in numbers only."}

        USER["stage"] = "salary"
        return {"reply": "Great! What is your monthly salary?"}

    # ---------- Salary ----------
    if stage == "salary":
        try:
            USER["salary"] = int(user_input)
        except:
            return {"reply": "Enter a numeric salary like 45000."}

        USER["stage"] = "kyc"
        return {"reply": "Thanks! Please enter your PAN number."}

    # ---------- PAN ENTRY ----------
    if stage == "kyc":
        pan = user_input.upper().strip()

        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan):
            return {"reply": "Invalid PAN. Enter something like ABCDE1234F."}

        USER["pan"] = pan
        USER["stage"] = "decision"

        underwriting_reply = run_underwriting()
        return {"reply": f"PAN received.\n\n{underwriting_reply['reply']}"}

    # ---------- YES = generate sanction ----------
    if stage == "decision" and user_input.lower() in ["yes", "generate"]:
        USER["stage"] = "sanction"
        return {"reply": "Your sanction letter is ready:\nhttp://127.0.0.1:8000/download-sanction"}

    if stage == "decision":
        return {"reply": "Please type YES to generate your sanction letter."}

    # ---------- Already sanctioned ----------
    if stage == "sanction":
        return {"reply": "Your sanction letter is ready:\nhttp://127.0.0.1:8000/download-sanction"}

# ---------------- PDF ----------------
def generate_sanction_pdf(filename, amount, salary, pan):
    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "TATA CAPITAL – SANCTION LETTER")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Loan Amount Approved: ₹{amount}")
    c.drawString(50, 750, f"Monthly Salary: ₹{salary}")
    c.drawString(50, 730, f"PAN: {pan}")

    c.drawString(50, 700, "Terms & Conditions:")
    c.drawString(70, 680, "- Processing Fee: ₹999")
    c.drawString(70, 660, "- Tenure: 12–60 months")
    c.drawString(70, 640, "- Standard NBFC policies apply")

    c.save()

@app.get("/download-sanction")
def download_sanction():
    filename = "sanction_letter.pdf"
    generate_sanction_pdf(filename, USER["loan_amount"], USER["salary"], USER["pan"])
    return FileResponse(filename, media_type="application/pdf", filename=filename)
