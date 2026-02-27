# Auto-Apply App

A minimal, working starter to send your resume to stored HR contacts with one click.

> **MVP features**: upload resume (PDF), store companies/HR emails, list companies, send email with attachment, view send logs.

## Running Locally

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python db_seed.py
python app.py
```

Backend runs at `http://localhost:5001`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Important Notes

1. Create both `.env` files before running
2. For Gmail, enable 2FA and create an **App Password**
3. Or use a provider like SendGrid/Mailgun and place their SMTP creds in backend `.env`
