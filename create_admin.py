from database import SessionLocal
from models import User
from utils.security import hash_password

db = SessionLocal()

admin = User(
    email="admin@admin.com",
    password_hash=hash_password("admin123"),
    role="admin"
)

db.add(admin)
db.commit()

print("Admin creado correctamente")
