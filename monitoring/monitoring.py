import os
import time
import asyncio
import psutil
import requests
import docker
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# === Логирование в файл ===
logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# === Загрузка .env ===
load_dotenv()
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# === Константы ===
CHECK_INTERVAL = 60
ALERT_REPEAT_INTERVAL = 30
CPU_CRIT = 90
MEM_CRIT = 90
DISK_CRIT = 90
CHAT_DB_FILE = "chats.txt"

URLS_TO_CHECK = {
    "Django": "https://yumlschool.ru",
    "API": "https://yumlschool.ru/api/users"
}

CONTAINERS = ["django-app", "aspnet-api", "mssql-db", "nginx"]

client = docker.from_env()
alerts_active = {}

# === Очистка лога, если он слишком большой ===
def cleanup_log_file():
    log_path = "logfile.log"
    max_size_mb = 10
    if os.path.exists(log_path):
        if os.path.getsize(log_path) > max_size_mb * 1024 * 1024:
            with open(log_path, "w") as f:
                f.truncate(0)
            logging.info("Файл логов превышал 10 МБ и был очищен.")

# === Telegram команды ===
def register_chat_id(chat_id: str):
    if not os.path.exists(CHAT_DB_FILE):
        with open(CHAT_DB_FILE, "w") as f:
            f.write(f"{chat_id}\n")
    else:
        with open(CHAT_DB_FILE, "r+") as f:
            chats = {line.strip() for line in f}
            if str(chat_id) not in chats:
                f.write(f"{chat_id}\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_chat_id(str(update.effective_chat.id))
    await update.message.reply_text("Вы подписались на мониторинг сервера. Используйте /menu для опций.")

async def stop_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts_active.clear()
    await update.message.reply_text("Оповещения остановлены.")

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[f"/getlogs {name}"] for name in CONTAINERS]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите контейнер для просмотра логов:", reply_markup=markup)

async def get_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажите имя контейнера, например: /getlogs aspnet-api")
        return
    container_name = context.args[0]
    if container_name not in CONTAINERS:
        await update.message.reply_text(f"Контейнер '{container_name}' не найден.")
        return
    log_path = save_container_logs(container_name)
    await send_log_file(update.effective_chat.id, log_path)

# === Работа с логами ===
def save_container_logs(container_name):
    log_filename = f"{container_name}_log_{time.strftime('%Y%m%d_%H%M%S')}.log"
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=200).decode(errors='ignore')
    except Exception as e:
        logs = f"Ошибка получения логов: {str(e)}"
        logging.error(logs)
    with open(log_filename, "w") as f:
        f.write(logs)
    return log_filename

async def send_log_file(chat_id, log_path):
    try:
        bot = Bot(TG_BOT_TOKEN)
        with open(log_path, "rb") as f:
            await bot.send_document(chat_id=chat_id, document=f, filename=os.path.basename(log_path))
    except Exception as e:
        logging.error(f"Ошибка при отправке файла: {e}")
    finally:
        try:
            os.remove(log_path)
        except Exception as e:
            logging.warning(f"Ошибка при удалении файла: {e}")

async def broadcast_message(message, log_path=None):
    if not os.path.exists(CHAT_DB_FILE):
        return
    with open(CHAT_DB_FILE, "r") as f:
        chat_ids = [line.strip() for line in f]
    bot = Bot(TG_BOT_TOKEN)
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            if log_path:
                with open(log_path, "rb") as f_log:
                    await bot.send_document(chat_id=chat_id, document=f_log, filename=os.path.basename(log_path))
        except Exception as e:
            logging.error(f"Ошибка отправки в чат {chat_id}: {e}")

async def send_alert(key, message, log_path=None):
    if key not in alerts_active:
        alerts_active[key] = time.time()
        await broadcast_message(message, log_path)
    elif time.time() - alerts_active[key] >= ALERT_REPEAT_INTERVAL:
        alerts_active[key] = time.time()
        await broadcast_message(message, log_path)

# === Мониторинг ===
async def check_services():
    for name, url in URLS_TO_CHECK.items():
        alert_key = f"service_{name}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200:
                await send_alert(alert_key, f"{name} недоступен! Код: {r.status_code}")
            else:
                # если раньше был алерт — уведомим о восстановлении
                if alert_key in alerts_active:
                    await broadcast_message(f"{name} снова доступен (код {r.status_code})")
                    alerts_active.pop(alert_key, None)
        except Exception as e:
            await send_alert(alert_key, f"{name} недоступен!")

async def check_containers():
    running = {c.name for c in client.containers.list()}
    for container_name in CONTAINERS:
        alert_key = f"container_{container_name}"
        if container_name not in running:
            log_path = save_container_logs(container_name)
            await send_alert(alert_key, f"Контейнер {container_name} не работает!", log_path)
        else:
            # Если контейнер раньше был в алерте, а теперь работает — уведомляем об этом
            if alert_key in alerts_active:
                await broadcast_message(f"Контейнер {container_name} снова запущен!")
                alerts_active.pop(alert_key, None)

async def check_resources():
    if psutil.cpu_percent() > CPU_CRIT:
        await send_alert("cpu", "Внимание! Высокая нагрузка на CPU")
    else:
        alerts_active.pop("cpu", None)

    if psutil.virtual_memory().percent > MEM_CRIT:
        await send_alert("memory", "Внимание! Высокое потребление памяти")
    else:
        alerts_active.pop("memory", None)

    if psutil.disk_usage('/').percent > DISK_CRIT:
        await send_alert("disk", "Внимание! Заканчивается место на диске")
    else:
        alerts_active.pop("disk", None)

async def monitor_loop(context: ContextTypes.DEFAULT_TYPE):
    cleanup_log_file()
    await check_services()
    await check_containers()
    await check_resources()

# === Инициализация ===
if __name__ == "__main__":
    app = Application.builder().token(TG_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop_alerts))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("getlogs", get_logs))

    app.job_queue.run_repeating(monitor_loop, interval=CHECK_INTERVAL)
    app.run_polling()
