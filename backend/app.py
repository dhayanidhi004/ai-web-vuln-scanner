from flask import Flask, request, jsonify, send_file, send_from_directory, session
from flask_cors import CORS
from scanner import scan_site
from ai_engine import ai_analyze
from database import SessionLocal, ScanHistory, User
from fpdf import FPDF
import datetime
import os

# ================= INIT =================
app = Flask(__name__, static_folder='../frontend', static_url_path='')

app.secret_key = "super-secret-key"

# 🔥 IMPORTANT FOR NGROK SESSION FIX
app.config.update(
    SESSION_COOKIE_SECURE=False,   # MUST be False for ngrok
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

CORS(app, supports_credentials=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts", "DejaVuSans.ttf")


# ================= FRONTEND =================
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


# ================= AUTH =================
def login_required():
    return "user" in session


# ================= HEALTH =================
@app.route("/health")
def health():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"status": "backend connected"})


# ================= SIGNUP =================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing fields"})

    db = SessionLocal()

    if db.query(User).filter(User.username == username).first():
        db.close()
        return jsonify({"success": False, "message": "Username already exists"})

    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.close()

    return jsonify({"success": True})


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    db = SessionLocal()
    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()
    db.close()

    if not user:
        return jsonify({"success": False, "message": "Invalid credentials"})

    session["user"] = username
    session.permanent = True   # 🔥 Important

    return jsonify({"success": True})


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"success": True})


# ================= SCAN =================
@app.route("/scan", methods=["GET", "POST"])
def scan():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    url = request.args.get("url")
    if not url and request.is_json:
        url = request.json.get("url")

    if not url:
        return jsonify({"error": "No URL provided", "results": [], "total": 0})

    findings = scan_site(url)
    report = ai_analyze(findings)

    db = SessionLocal()
    for r in report["results"]:
        db.add(ScanHistory(
            url=url,
            severity=r["severity"],
            scanned_at=datetime.datetime.utcnow()
        ))
    db.commit()
    db.close()

    return jsonify(report)


# ================= PDF =================
@app.route("/pdf")
def generate_pdf():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    url = request.args.get("url", "Unknown")
    report = ai_analyze(scan_site(url))

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(0, 10, "AI Web Vulnerability Scan Report", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(0, 8, f"Target URL: {url}", ln=True)
    pdf.cell(0, 8, f"Date: {datetime.datetime.now()}", ln=True)
    pdf.ln(5)

    for r in report["results"]:
        pdf.multi_cell(0, 8, f"""
Vulnerability : {r['vulnerability']}
Severity      : {r['severity']}
Attack Vector : {r['attack']}
AI Prevention : {r['prevention']}
OWASP Ref     : {r['owasp_reference']}
-----------------------------
""".strip())
        pdf.ln(2)

    file_path = os.path.join(BASE_DIR, "scan_report.pdf")
    pdf.output(file_path)

    return send_file(file_path, as_attachment=True)


# ================= RUN =================
if __name__ == "__main__":
    # 🔥 TURN OFF DEBUG
    app.run(host="0.0.0.0", port=8000, debug=False)
