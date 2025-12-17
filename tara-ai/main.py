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
    name: str = ""
    city: str = ""
    occupation: str = ""
    bank_account: str = ""

class LoginData(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(data: SignupData):
    users = load_users()
    if data.email in users:
        raise HTTPException(400, "Email already registered.")

    # ⭐ ONLY ADDITIONS BELOW ⭐
    users[data.email] = {
        "password": data.password,
        "name": data.name,
        "city": data.city,
        "occupation": data.occupation,
        "bank_account": data.bank_account,
        "pan_verified": False
    }
    # ⭐ ADDITIONS END ⭐

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
        "stage": "start",
        "loan_amount": None,
        "salary": None,
        "pan": None,
        "purpose": None,
        "employment": None,
        "city": None,
        "last_underwriting": None
    }

USER = reset_user()

class Message(BaseModel):
    text: str

# ---------------- UNDERWRITING ----------------
def run_underwriting():
    amount = int(USER["loan_amount"])
    salary = int(USER["salary"])
    max_allowed = salary * 20

    if salary < 20000:
        return {
            "status": "reject",
            "reply": "Income below ₹20,000 is not eligible for loan approval."
        }

    if amount > max_allowed:
        return {
            "status": "exceeds",
            "max_allowed": max_allowed,
            "reply": (
                f"The requested amount ₹{amount} exceeds your eligible limit.\n"
                f"You can get up to ₹{max_allowed}.\n"
                "Would you like to adjust your request?"
            )
        }

    return {
        "status": "approved",
        "reply": (
            "Great! You are eligible for this amount.\n"
            "Would you like me to generate your sanction letter?"
        )
    }

# ---------------- CHAT ENGINE ----------------
@app.post("/chat")
def chat(msg: Message):
    global USER
    user_raw = msg.text.strip()
    user_lower = user_raw.lower()
    stage = USER["stage"]

    if user_lower in ["hi", "hello", "hey", "restart", "reset", "start"]:
        USER = reset_user()
        USER["stage"] = "intent"
        return {"reply": "Hi, I'm TARA 😊 How can I help you today?"}

    if stage == "start":
        USER["stage"] = "intent"
        return {"reply": "Hi, I'm TARA 😊 How can I help you today?"}

    if stage == "intent":
        USER["intent"] = user_raw
        USER["stage"] = "purpose"
        return {"reply": "Sure! What is the purpose of your loan?"}

    if stage == "purpose":
        USER["purpose"] = user_raw
        USER["stage"] = "employment"
        return {"reply": "Are you Salaried or Self‑employed?"}

    if stage == "employment":
        USER["employment"] = user_raw
        USER["stage"] = "city"
        return {"reply": "Which city do you live in?"}

    if stage == "city":
        USER["city"] = user_raw
        USER["stage"] = "loan_amount"
        return {"reply": "What loan amount are you looking for?"}

    if stage == "loan_amount":
        if not user_raw.isdigit():
            return {"reply": "Please enter the loan amount in numbers only."}

        USER["loan_amount"] = int(user_raw)
        USER["stage"] = "salary"
        return {"reply": "And what is your monthly salary?"}

    if stage == "salary":
        if not user_raw.isdigit():
            return {"reply": "Please enter your salary in numbers only."}

        USER["salary"] = int(user_raw)
        USER["stage"] = "kyc"
        return {"reply": "Please enter your PAN number."}

    if stage == "kyc":
        pan = user_raw.upper()
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan):
            return {"reply": "Invalid PAN format. Enter something like ABCDE1234F."}

        USER["pan"] = pan
        result = run_underwriting()
        USER["last_underwriting"] = result
        USER["stage"] = "decision"

        return {"reply": f"PAN verified successfully.\n\n{result['reply']}"}

    if stage == "decision":
        result = USER["last_underwriting"]

        if result["status"] == "exceeds":

            if user_raw.isdigit():
                USER["loan_amount"] = int(user_raw)
                new_result = run_underwriting()
                USER["last_underwriting"] = new_result
                return {"reply": f"Rechecking...\n\n{new_result['reply']}"}

            if user_lower in ["yes", "y"]:
                USER["stage"] = "adjust_amount"
                return {"reply": f"Please enter a new amount (Max ₹{result['max_allowed']})."}

            if user_lower in ["no", "n"]:
                USER["stage"] = "end"
                return {"reply": "Alright. Let me know if you need anything else."}

            return {"reply": result["reply"]}

        if result["status"] == "approved":
            if user_lower in ["yes", "y", "generate"]:
                USER["stage"] = "sanction"
                return {
                    "reply": (
                        "Preparing your sanction letter...\n"
                        "http://127.0.0.1:8000/download-sanction"
                    )
                }
            return {"reply": "Please type YES to generate your sanction letter."}

        if result["status"] == "reject":
            USER["stage"] = "end"
            return {"reply": result["reply"]}

    if stage == "adjust_amount":
        if not user_raw.isdigit():
            return {"reply": "Enter numeric amount only."}

        USER["loan_amount"] = int(user_raw)
        new_result = run_underwriting()
        USER["last_underwriting"] = new_result
        USER["stage"] = "decision"

        return {"reply": f"Updated check:\n\n{new_result['reply']}"}

    if stage == "sanction":
        return {
            "reply": "Your sanction letter is ready:\nhttp://127.0.0.1:8000/download-sanction"
        }

    return {"reply": "Type restart to begin again."}

# ---------------- PDF GENERATION ----------------
def generate_sanction_pdf(filename, amount, salary, pan):
    c = canvas.Canvas(filename)

    tick = u"\u2713"

    processing_fee = int(amount * 0.02)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "TATA CAPITAL – SANCTION LETTER")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"{tick} Loan Amount Approved: ₹{amount}")
    c.drawString(50, 750, f"{tick} Monthly Salary Verified: ₹{salary}")
    c.drawString(50, 730, f"{tick} PAN Verified: {pan}")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, 700, "Terms & Conditions:")

    c.setFont("Helvetica", 12)
    c.drawString(70, 680, f"{tick} Processing Fee: ₹{processing_fee}")
    c.drawString(70, 660, f"{tick} Tenure: 12–60 months")
    c.drawString(70, 640, f"{tick} Standard NBFC policies apply")

    c.save()

@app.get("/download-sanction")
def download_sanction():
    filename = "sanction_letter.pdf"
    generate_sanction_pdf(
        filename, USER["loan_amount"], USER["salary"], USER["pan"]
    )
    return FileResponse(filename, media_type="application/pdf", filename=filename)

# -------------------------------------------------------------
# ⭐⭐⭐ ADDED NEW PROFILE ENDPOINTS (NOTHING ABOVE WAS MODIFIED) ⭐⭐⭐
# -------------------------------------------------------------

class UpdateProfile(BaseModel):
    name: str = ""
    city: str = ""
    occupation: str = ""
    bank_account: str = ""

@app.get("/profile/{email}")
def get_profile(email: str):
    users = load_users()
    if email not in users:
        raise HTTPException(404, "User not found")
    return users[email]

@app.post("/update-profile/{email}")
def update_profile(email: str, data: UpdateProfile):
    users = load_users()
    if email not in users:
        raise HTTPException(404, "User not found")

    for key, value in data.dict().items():
        if value != "":
            users[email][key] = value

    save_users(users)
    return {"message": "Profile updated successfully"}

@app.post("/verify-pan/{email}")
def verify_pan(email: str):
    users = load_users()
    if email not in users:
        raise HTTPException(404, "User not found")

    users[email]["pan_verified"] = True
    save_users(users)
    return {"message": "PAN verified successfully!"}
