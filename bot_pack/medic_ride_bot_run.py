from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    PicklePersistence

import os
from dotenv import load_dotenv

from adding_ride_funcs_2 import add_ride, get_ride_status, get_departure_time, get_departure_date, \
    get_ride_type_or_start_point, get_finish_point_and_send_requests
from other_funcs import start, cancel, not_ended_action
from register_funcs import register, get_user_status
from view_details_funcs import get_details, view_finish_point, get_chat, get_back_mock, end_viewing
from vars_module import *

load_dotenv()


def main():
    # my_persistence = PicklePersistence(filename='my_pickle_storage')
    updater = Updater(os.getenv("BOT_TOKEN"),
                      # persistence=my_persistence,
                      use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register, pass_user_data=True),
                      CommandHandler('add_ride', add_ride, pass_user_data=True)],
        states={
            GET_USER_STATUS: [CallbackQueryHandler(get_user_status, pattern=f'^{str(DRIVER)}$|^{str(DOCTOR)}$')],
            GET_RIDE_STATUS: [CallbackQueryHandler(get_ride_status, pattern=f'^{str(ONE_TIME)}$|^{str(REGULAR)}$')],
            GET_DEPARTURE_TIME: [MessageHandler(Filters.text, get_departure_time, pass_user_data=True)],
            GET_DEPARTURE_DATE: [MessageHandler(Filters.text, get_departure_date, pass_user_data=True)],
            GET_START_POINT: [MessageHandler(Filters.text, get_ride_type_or_start_point, pass_user_data=True)],
            GET_FINISH_POINT: [MessageHandler(Filters.text, get_finish_point_and_send_requests, pass_user_data=True)],
            # ниже - conversation для получения инфы о совпадении
            GET_RESULT_LIST: [CallbackQueryHandler(get_details, pattern=f'^{str(GET_DETAILS)}$', pass_user_data=True)],
            SELECTING_DETAILS_ACTION: [CallbackQueryHandler(view_finish_point, pattern=f'^{str(VIEW)}$', pass_user_data=True),
                                       CallbackQueryHandler(get_chat, pattern=f'^{str(CHAT)}$', pass_user_data=True),
                                       CallbackQueryHandler(get_back_mock, pattern=f'^{str(BACK_BUTTON)}$', pass_user_data=True),
                                       CallbackQueryHandler(end_viewing, pattern=f'^{str(NO)}$'),
                                       # CallbackQueryHandler(not_ended_action, pattern=f'^/register|/add_ride$')],
                                       MessageHandler(Filters.regex(r'^/register|/add_ride$'), not_ended_action)
                                       ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(start_handler)
    dp.add_handler(conversation_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
