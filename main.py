import logging
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from functions import *

# Установка уровня логирования для отображения ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция-обработчик команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Я бот для поиска дней рождения. Просто отправь мне вопрос в формате: "Когда у Пети день рождение?" или "У кого 30 июня день рождения?".')

# Функция-обработчик входящих текстовых сообщений
async def handle_message(update, context):
    query_text = update.message.text  # Получаем текст сообщения
    output = output_answer(query_text)  # Получаем ответ от функции output_answer
    print("Ответ от гпт:" , output)
    await update.message.reply_text(output)  # Отправляем ответ пользователю

# Главная функция, которая будет вызвана при запуске скрипта
def main():
    application = Application.builder().token(telegram_token).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчики текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Стартуем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
