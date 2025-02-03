from decouple import config

db_url = config("DATABASE_URL", default="Not Found")
print(f"DATABASE_URL: {db_url}")
