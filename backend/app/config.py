import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://coges:coges_dev_password@localhost:5432/coges_configurator",
)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Password condivisa per l'area interna staff (lista richieste di preventivo).
# Protezione minima per il prototipo: un'unica password nota allo staff
# Coges, non account individuali. Vedi app/staff_auth.py.
STAFF_ACCESS_TOKEN = os.getenv("STAFF_ACCESS_TOKEN", "")
