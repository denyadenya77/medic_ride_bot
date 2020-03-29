from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import os
from dotenv import load_dotenv

from adding_ride_funcs import add_one_time_ride, get_start_point, get_finish_point, get_date_of_departure, \
    get_time_of_departure, get_ride_status
from other_funcs import start, cancel
from register_funcs import register, get_user_status

load_dotenv()


GET_USER_STATUS, GET_START_POINT, GET_FINISH_POINT, GET_DEPARTURE_DATE, GET_DEPARTURE_TIME, \
 GET_RIDE_STATUS = map(chr, range(6))
DRIVER, DOCTOR = map(chr, range(6, 8))
ONE_TIME, REGULAR = map(chr, range(8, 10))


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
