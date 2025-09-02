from models import SessionLocal, init_db, Company

init_db()
db = SessionLocal()

companies = [
    {"name": "Acme Corp", "hr_name": "nandana", "hr_email": "nandanapramodak@gmail.com", "role": "SDE Intern"},
    {"name": "Globex", "hr_name": "Rahul Verma", "hr_email": "rahul.verma@globex.com", "role": "Frontend Engineer"},
]

for c in companies:
    if not db.query(Company).filter_by(name=c["name"]).first():
        db.add(Company(**c))

db.commit()
db.close()
print("Seeded companies ✅")