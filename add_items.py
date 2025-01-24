from app.database import SessionLocal
from app.models import LibraryItem
from datetime import date

# Создаём сессию для работы с базой данных
db = SessionLocal()

# Добавляем 5 записей
items = [
    LibraryItem(title="Clean Code", description="A Handbook of Agile Software Craftsmanship", publication_date=date(2008, 8, 1), author="Robert C. Martin", genre="Software Development", available_copies=5, published_year=2008),
    LibraryItem(title="Refactoring", description="Improving the Design of Existing Code", publication_date=date(1999, 7, 1), author="Martin Fowler", genre="Software Development", available_copies=3, published_year=1999),
    LibraryItem(title="The Pragmatic Programmer", description="Your Journey to Mastery", publication_date=date(1999, 10, 1), author="Andrew Hunt", genre="Software Development", available_copies=8, published_year=1999),
    LibraryItem(title="Design Patterns", description="Elements of Reusable Object-Oriented Software", publication_date=date(1994, 1, 1), author="Erich Gamma", genre="Software Engineering", available_copies=6, published_year=1994),
    LibraryItem(title="Code Complete", description="A Practical Handbook of Software Construction", publication_date=date(2004, 6, 9), author="Steve McConnell", genre="Software Development", available_copies=10, published_year=2004)
]

# Добавляем записи в базу
db.add_all(items)
db.commit()

# Закрываем сессию
db.close()
