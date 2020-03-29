from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import os
from dotenv import load_dotenv
load_dotenv()


(GET_USER_STATUS, GET_START_POINT, GET_FINISH_POINT, GET_DEPARTURE_DATE, GET_DEPARTURE_TIME,
 GET_RIDE_STATUS) = map(chr, range(6))
DRIVER, DOCTOR = map(chr, range(6, 8))
ONE_TIME, REGULAR = map(chr, range(8, 10))


# other commands

def start(update, context):
    update.message.reply_text('Вітаємо!')


def cancel(update, context):
    return ConversationHandler.END


# register commands

def register(update, context):
    text = 'Enter user type:'
    buttons = [[
        InlineKeyboardButton(text='DRIVER', callback_data=str(DRIVER)),
        InlineKeyboardButton(text='DOCTOR', callback_data=str(DOCTOR))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)
    return GET_USER_STATUS


def get_user_status(update, context):
    user_type = update.callback_query.data

    if user_type is DRIVER:
        user_type = 'driver'
    else:
        user_type = 'doctor'

    text = f'Now you are a {user_type}'
    update.callback_query.answer()
    update.callback_query.edit_message_text(text)
    return ConversationHandler.END


# adding ride commands
def add_one_time_ride(update, context):
    update.message.reply_text('Надішліть координати старту. \n51.6680, 32.6546')
    return GET_START_POINT


def get_start_point(update, context):
    latitude, longitude = update.message.text.split(', ')

    # adding vars to user_data
    context.user_data['start_latitude'] = latitude
    context.user_data['start_longitude'] = longitude

    update.message.reply_text(f'Координати місця вашого відправлення: {latitude}, {longitude}')
    update.message.reply_text('А тепер вкажіть, куди ви прямуєте.')
    return GET_FINISH_POINT


def get_finish_point(update, context):
    latitude, longitude = update.message.text.split(', ')

    # adding vars to user_data
    context.user_data['finish_latitude'] = latitude
    context.user_data['finish_longitude'] = longitude

    update.message.reply_text(f'Координати місця вашого призначення: {latitude}, {longitude}')
    update.message.reply_text('Будь ласка, введіть дату поїздки у форматі DD.MM.YYYY')
    return GET_DEPARTURE_DATE


def get_date_of_departure(update, context):
    date_of_departure = update.message.text

    # adding vars to user_data
    context.user_data['date_of_departure'] = date_of_departure

    update.message.reply_text(f'Дата вашого відправлення: {date_of_departure}.'
                              f'Залишилося визначитися з часом! Введіть час у форматі HH.MM')
    return GET_DEPARTURE_TIME


def get_time_of_departure(update, context):
    time_of_departure = update.message.text

    # adding vars to user_data
    context.user_data['time_of_departure'] = time_of_departure

    keyboard = [[InlineKeyboardButton("Однократна поїздка", callback_data=str(ONE_TIME))],
                [InlineKeyboardButton("Регулярна поїздка", callback_data=str(REGULAR))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f'Час вашого відправлення: {time_of_departure}.'
                              f'Якщо ви здійснюєте цю поїздку регулярно - повідомте про це, будь ласка.',
                              reply_markup=reply_markup)
    return GET_RIDE_STATUS


def get_ride_status(update, context):
    query = update.callback_query
    ride_type = query.data

    # adding vars to user_data
    if ride_type is ONE_TIME:
        context.user_data['ride_type'] = 'ONE_TIME'
    else:
        context.user_data['ride_type'] = 'REGULAR'

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        f'Дякуємо! Ваша поїздка зереєстрована у системі. Ми повідомимо, коли знайдемо вам '
        f'попутника\n'
        f'Деталі:\n'
        f'Координати відправлення: {context.user_data["start_latitude"]}, {context.user_data["start_longitude"]}.\n'
        f'Координати призначення: {context.user_data["finish_latitude"]}, {context.user_data["finish_longitude"]}\n'
        f'Дата відправлення: {context.user_data["date_of_departure"]}.\n'
        f'Час выдправлення: {context.user_data["time_of_departure"]}.\n'
        f'Тип поїдки: {context.user_data["ride_type"]}.')
    return ConversationHandler.END


def main():
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register),
                      CommandHandler('add_one_time_ride', add_one_time_ride)],
        states={
            GET_USER_STATUS: [CallbackQueryHandler(get_user_status, pattern=f'^{str(DRIVER)}$|^{str(DOCTOR)}$')],
            GET_START_POINT: [MessageHandler(Filters.text, get_start_point, pass_user_data=True)],
            GET_FINISH_POINT: [MessageHandler(Filters.text, get_finish_point, pass_user_data=True)],
            GET_DEPARTURE_DATE: [MessageHandler(Filters.text, get_date_of_departure, pass_user_data=True)],
            GET_DEPARTURE_TIME: [MessageHandler(Filters.text, get_time_of_departure, pass_user_data=True)],
            GET_RIDE_STATUS: [CallbackQueryHandler(get_ride_status, pattern=f'^{str(ONE_TIME)}$|^{str(REGULAR)}$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(start_handler)
    dp.add_handler(conv_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
