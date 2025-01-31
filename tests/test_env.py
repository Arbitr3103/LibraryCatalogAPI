from decouple import config

SECRET_KEY = config("SECRET_KEY", default="fallback_default_key")
print(f"Значение SECRET_KEY: {SECRET_KEY}")
