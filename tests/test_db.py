from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

# Создаём сессию для подключения к базе данных
db: Session = SessionLocal()

# Выполняем запрос
user = db.query(User).filter(User.username == "new_user").first()

if user:
    print(f"User found: {user.username}, Email: {user.email}")
else:
    print("User not found")

db.close()
