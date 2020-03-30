from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import os
from dotenv import load_dotenv

# from adding_ride_funcs import add_ride, get_start_point, get_finish_point, get_date_of_departure, \
#     get_time_of_departure, get_ride_status
from adding_ride_funcs_2 import add_ride, get_ride_status, get_departure_time, get_departure_date, \
    get_ride_type_or_start_point, get_finish_point_and_send_requests
from other_funcs import start, cancel
from register_funcs import register, get_user_status
from vars_module import *

load_dotenv()


def main():
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register),
                      CommandHandler('add_ride', add_ride)],
        states={
            GET_USER_STATUS: [CallbackQueryHandler(get_user_status, pattern=f'^{str(DRIVER)}$|^{str(DOCTOR)}$')],
            GET_RIDE_STATUS: [CallbackQueryHandler(get_ride_status, pattern=f'^{str(ONE_TIME)}$|^{str(REGULAR)}$')],
            GET_DEPARTURE_TIME: [MessageHandler(Filters.text, get_departure_time, pass_user_data=True)],
            GET_DEPARTURE_DATE: [MessageHandler(Filters.text, get_departure_date, pass_user_data=True)],
            GET_START_POINT: [MessageHandler(Filters.text, get_ride_type_or_start_point, pass_user_data=True)],
            GET_FINISH_POINT: [MessageHandler(Filters.text, get_finish_point_and_send_requests, pass_user_data=True)]

            # GET_DEPARTURE_TIME: [MessageHandler(Filters.text, get_time_of_departure, pass_user_data=True)],
            # GET_DEPARTURE_DATE: [MessageHandler(Filters.text, get_date_of_departure, pass_user_data=True)],
            # GET_START_POINT: [MessageHandler(Filters.text, get_start_point, pass_user_data=True)],
            # GET_FINISH_POINT: [MessageHandler(Filters.text, get_finish_point, pass_user_data=True)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(start_handler)
    dp.add_handler(conv_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
