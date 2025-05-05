import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from backend.database import SessionLocal
from backend.models import Vacante

# Cargar variables de entorno
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Falta TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en el .env")
    sys.exit(1)

bot = Bot(token=TELEGRAM_TOKEN)


def crear_mensaje(v):
    return (
        f"\U0001F680 {v.titulo} en {v.empresa}!\n"
        f"\U0001F4CD {v.ubicacion}, {v.pais}\n"
        f"\U0001F4BC {v.experiencia}\n"
        f"\U0001F4B0 {v.salario}\n"
        f"\U0001F3AF {v.role}\n"
        f"\U0001F4DE {v.contacto_nombre}: {v.contacto}\n"
        f"https://www.magneto365.com/es\n"
        f"#Empleo #Vacantes #Trabajo"
    )


async def publicar_vacante(job_id: int):
    db = SessionLocal()
    vacante = db.query(Vacante).filter(Vacante.job_id == job_id).first()
    db.close()

    if not vacante:
        print(f"⚠️ Vacante con ID {job_id} no encontrada.")
        return

    mensaje = crear_mensaje(vacante)

    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje)
        print("✅ Vacante publicada en Telegram.")
    except Exception as e:
        print(f"❌ Error al publicar en Telegram: {e}")


# Para pruebas directas desde consola
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Debes proporcionar el job_id como argumento.")
    else:
        asyncio.run(publicar_vacante(int(sys.argv[1])))
