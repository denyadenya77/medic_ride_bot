from telegram.ext import ConversationHandler
from vars_module import SELECTING_DETAILS_ACTION


# other commands

def start(update, context):
    update.message.reply_text(f'Вітаємо! Тут буде інструкція з користування.\nЧат айди: {update.message.chat.id}')


def cancel(update, context):
    return ConversationHandler.END


def not_ended_action(update, context):
    context.bot.send_message(update.effective_message.chat_id, 'Будь ласка, спочатку закінчіть перегляд '
                                                               'перерахованих вище маршрутів!')
    return SELECTING_DETAILS_ACTION


