from telegram.ext import ConversationHandler

# other commands
def start(update, context):
    update.message.reply_text('Вітаємо!')


def cancel(update, context):
    return ConversationHandler.END
