import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from models import SessionLocal, init_db, Company, Application
from emailer import send_email_with_attachment

load_dotenv()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print(f"Upload directory ready: {UPLOAD_DIR}")
except Exception as e:
    print(f"Error creating upload directory: {e}")
    
app = Flask(__name__)
CORS(app)
init_db()

# Health
@app.get("/api/health")
def health():
    return {"ok": True}

# List companies
@app.get("/api/companies")
def list_companies():
    db = SessionLocal()
    companies = db.query(Company).all()
    data = [
        {
            "id": c.id,
            "name": c.name,
            "hr_name": c.hr_name,
            "hr_email": c.hr_email,
            "role": c.role,
            "notes": c.notes,
        }
        for c in companies
    ]
    db.close()
    return jsonify(data)

# Add a company
@app.post("/api/companies")
def add_company():
    payload = request.json or {}
    required = ["name", "hr_email"]
    for k in required:
        if not payload.get(k):
            return jsonify({"error": f"Missing {k}"}), 400
    db = SessionLocal()
    c = Company(
        name=payload["name"],
        hr_name=payload.get("hr_name"),
        hr_email=payload["hr_email"],
        role=payload.get("role"),
        notes=payload.get("notes"),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    return jsonify({"id": c.id}), 201

# Upload resume
@app.post("/api/resume")
def upload_resume():
    try:
        if "file" not in request.files:
            print("Error: No file in request")
            return jsonify({"error": "No file part"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            print("Error: Empty filename")
            return jsonify({"error": "No selected file"}), 400
            
        if not file.filename.lower().endswith(".pdf"):
            print(f"Error: Invalid file type: {file.filename}")
            return jsonify({"error": "Only PDF allowed"}), 400
            
        save_path = os.path.join(UPLOAD_DIR, "resume.pdf")
        file.save(save_path)
        print(f"Resume saved successfully at: {save_path}")
        
        full_url = f"/uploads/resume.pdf"
        print(f"Returning URL: {full_url}")
        return jsonify({
            "ok": True,
            "url": full_url,
            "message": "Resume uploaded successfully"
        })
    except Exception as e:
        print(f"Error uploading resume: {str(e)}")
        return jsonify({
            "ok": False,
            "error": f"Upload failed: {str(e)}"
        }), 500

# Get stored resume
@app.get("/api/resume")
def get_resume():
    resume_path = os.path.join(UPLOAD_DIR, "resume.pdf")
    if os.path.exists(resume_path):
        return jsonify({"ok": True, "url": "/uploads/resume.pdf"})
    return jsonify({"ok": False, "error": "No resume uploaded yet"})

# Send resume to company
@app.post("/api/send/<int:company_id>")
def send_resume(company_id):
    db = SessionLocal()
    company = db.query(Company).get(company_id)
    if not company:
        db.close()
        return jsonify({"error": "Company not found"}), 404

    resume_path = os.path.join(UPLOAD_DIR, "resume.pdf")
    if not os.path.exists(resume_path):
        db.close()
        return jsonify({"error": "Upload resume first"}), 400

    subject = f"Application for {company.role or 'Role'} — {os.getenv('FROM_NAME', 'Candidate')}"
    hr_name = company.hr_name or "Hiring Team"
    body = (
        f"Dear {hr_name},\n\n"
        "I hope you're doing well. Please find my resume attached for your consideration.\n\n"
        "Best regards,\n"
        f"{os.getenv('FROM_NAME', 'Candidate')}\n"
        f"{os.getenv('FROM_EMAIL', '')}"
    )

    app_rec = Application(company_id=company.id)
    try:
        send_email_with_attachment(company.hr_email, subject, body, resume_path)
        app_rec.status = "SENT"
        app_rec.error_message = None
    except Exception as e:
        app_rec.status = "FAILED"
        app_rec.error_message = str(e)

    db.add(app_rec)
    db.commit()
    db.refresh(app_rec)
    db.close()

    return jsonify({"status": app_rec.status, "error": app_rec.error_message})

# List applications (logs)
@app.get("/api/applications")
def list_applications():
    db = SessionLocal()
    apps = db.query(Application).order_by(Application.sent_at.desc()).all()
    data = [
        {
            "id": a.id,
            "company_id": a.company_id,
            "company": a.company.name if a.company else None,
            "sent_at": a.sent_at.isoformat(),
            "status": a.status,
            "error": a.error_message,
        }
        for a in apps
    ]
    db.close()
    return jsonify(data)

# Serve uploaded files
@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)