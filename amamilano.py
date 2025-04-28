import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logger configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

def log_user_info(update: Update):
    """
    Log information about the user and chat.

    This function logs the user's first name, last name (if available), and username
    (if available), as well as the chat ID and chat type.

    :param update: The incoming update.
    """
    user = update.effective_user
    chat = update.effective_chat

    user_info = f"User: {user.first_name} {user.last_name or ''} (@{user.username or 'N/A'})"
    chat_info = f"Chat ID: {chat.id}, Chat Type: {chat.type}"

    logger.info(f"{user_info}, {chat_info}")

async def engage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /engage command.

    This function is responsible for handling the /engage command, which is used to
    retrieve a random verb from the verbs.txt file and send a response back to the
    user.

    It logs information about the user and chat, then reads the verbs.txt file to
    count the number of lines in it. The response is then composed as a string and
    sent back to the user.

    If the verbs.txt file is not found, an error message is sent back to the user.
    If any other exception is raised, an error message is logged and sent back to
    the user.
    """
    log_user_info(update)
    try:
        with open("verbs.txt", "r") as f:
            verbs = f.readlines()
        random_verb = random.choice(verbs).strip() + "MILANO"
        response = f"Lascio colare un po' di engagement: {random_verb}"
        logger.info(f"Responding with: {response}")
        await update.message.reply_text(response)
    except FileNotFoundError:
        error_message = (
            "Errore: Il file 'verbs.txt' non è stato trovato, rivolgersi al peracottaro che mi ha messo al mondo."
        )
        logger.error(error_message)
        await update.message.reply_text(error_message)
    except Exception as e:
        error_message = f"Errore: {str(e)}"
        logger.error(error_message)
        await update.message.reply_text(error_message)

async def version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /version command.

    This function is responsible for handling the /version command, which is used to
    retrieve the current version of the bot.

    It logs information about the user and chat, then reads the verbs.txt file to
    count the number of lines in it. The response is then composed as a string and
    sent back to the user.

    If the verbs.txt file is not found, an error message is sent back to the user.
    If any other exception is raised, an error message is logged and sent back to
    the user.
    """
    log_user_info(update)
    try:
        with open("verbs.txt", "r") as f:
            verbs = f.readlines()
        line_count = len(verbs)
        version_info = "0.7.3"
        logger.info(f"Version info: {version_info}")
        response = (
            "#AmaMilano, il bot per il vero imbruttito della City.\n"
            f"Versione {version_info}\n"
            "Edizione 'PYTHONAMILANO'\n"
            f"File locale: verbs.txt, voci caricate in libreria: {line_count}"
        )
        logger.info(f"Responding with version info: {response}")
        await update.message.reply_text(response)
    except FileNotFoundError:
        error_message = "Errore: Il file 'verbs.txt' non è stato trovato."
        logger.error(error_message)
        await update.message.reply_text(error_message)
    except Exception as e:
        error_message = f"Errore: {str(e)}"
        logger.error(error_message)
        await update.message.reply_text(error_message)

def main():
    """
    Main entry point for the bot.

    This function is responsible for:

    - Getting the Telegram token from the TELEGRAM_TOKEN environment variable.
    - Creating the Application object.
    - Registering the command handlers.
    - Starting the bot.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.critical("Error: TELEGRAM_TOKEN is not set.")
        exit(1)

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("engage", engage))
    app.add_handler(CommandHandler("version", version))

    logger.info("Bot started and running ...")
    app.run_polling()

if __name__ == "__main__":
    main()
