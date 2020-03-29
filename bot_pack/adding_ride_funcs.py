from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from medic_ride_bot_run import GET_START_POINT, GET_FINISH_POINT, GET_DEPARTURE_DATE, GET_DEPARTURE_TIME, \
    GET_RIDE_STATUS, \
    ONE_TIME, REGULAR


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
