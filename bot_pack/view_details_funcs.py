from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from vars_module import SELECTING_DETAILS_ACTION, VIEW, CHAT, BACK_BUTTON, NO


def get_details(update, context):
    result_list = context.user_data['response']['result_list']
    update.callback_query.edit_message_text('Ми знайшли медиків поряд з місцем вашого відправлення!')

    context.chat_data['info'] = {'count_of_active_messages': 0}

    for key, value in result_list.items():

        context.chat_data['info']['count_of_active_messages'] += 1

        keyboard = [[InlineKeyboardButton("Переглянути пункт призначення", callback_data=str(VIEW))],
                    [InlineKeyboardButton("Зв'язатися з медиком", callback_data=str(CHAT))],
                    [InlineKeyboardButton("Цей маршрут мені не підходить", callback_data=str(NO))]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = f'{key}.\n'\
               f'Час відправлення: {value["time_of_departure"]}\n' \
               f'Дата відправлення: {value["date_of_departure"]}'

        # context.user_data.clear()
        # context.user_data['user_info'] = item  # не передаем CallbackQuery методам ничего лишего

        context.bot.send_message(chat_id=update.effective_message.chat_id, text=text,
                                 reply_tomessage_id=update.effective_message.message_id, reply_markup=reply_markup)
    return SELECTING_DETAILS_ACTION


def view_finish_point(update, context):

    message_data_index = int(update.effective_message.text[0])
    message_data = get_concrete_message_data(message_data_index, context)

    keyboard = [[InlineKeyboardButton("Зв'язатися з медиком", callback_data=str(CHAT))],
                [InlineKeyboardButton("Назад", callback_data=str(BACK_BUTTON))],
                [InlineKeyboardButton("Цей маршрут мені не підходить", callback_data=str(NO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f'{str(message_data_index)}.' \
           f'Замість тесту тут буде telegram.Location\n' \
           f'Наразі пунк призначення -- {message_data["finish_point"]}'
    update.callback_query.edit_message_text(f'{text}', reply_markup=reply_markup)
    return SELECTING_DETAILS_ACTION


def get_chat(update, context):
    message_data_index = int(update.effective_message.text[0])
    message_data = get_concrete_message_data(message_data_index, context)

    keyboard = [[InlineKeyboardButton("Переглянути пункт призначення", callback_data=str(VIEW))],
                [InlineKeyboardButton("Назад", callback_data=str(BACK_BUTTON))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f'{str(message_data_index)}.\n' \
           f'Замість тексту тут буде профіль медика.\n' \
           f'Наразі його чат-айді -- {message_data["user_chat_id"]}'

    update.callback_query.edit_message_text(f'{text}', reply_markup=reply_markup)
    return SELECTING_DETAILS_ACTION


def get_back_mock(update, context):
    """
    Этот метод возвращет исходное состояние сообщения. Вызываем его, потому что прописывать отдельное условие в
    get_details - глупо. В добавок может возникнуть конфлик двух CallbackQueryHandler: один будет в entry_points,
    а дургой в states.
    """
    message_data_index = int(update.effective_message.text[0])
    message_data = get_concrete_message_data(message_data_index, context)

    keyboard = [[InlineKeyboardButton("Переглянути пункт призначення", callback_data=str(VIEW))],
                [InlineKeyboardButton("Зв'язатися з медиком", callback_data=str(CHAT))],
                [InlineKeyboardButton("Цей маршрут мені не підходить", callback_data=str(NO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f'{message_data_index}.\n' \
           f'Час відправлення: {message_data["time_of_departure"]}\n' \
           f'Дата відправлення: {message_data["date_of_departure"]}'

    update.callback_query.edit_message_text(f'{text}', reply_markup=reply_markup)
    return SELECTING_DETAILS_ACTION


def end_viewing(update, context):
    update.callback_query.edit_message_text(f'Шкода! Можливо наступного разу нам пощастить більше!')

    if context.chat_data['info']['count_of_active_messages'] == 1:
        context.chat_data['info']['count_of_active_messages'] = 0
        context.user_data.clear()
        return ConversationHandler.END
    else:
        context.chat_data['info']['count_of_active_messages'] -= 1
        return SELECTING_DETAILS_ACTION

    
def get_concrete_message_data(message_data_index, context):
    message_data = {}
    for key, value in context.user_data['response']['result_list'].items():
        if key == message_data_index:
            message_data = value
    return message_data
