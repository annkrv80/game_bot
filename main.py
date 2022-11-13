import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import random

reply_keyboard = [['/play', '/info', '/close','/stop']]
stop_keyboard = [['/stop']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=False)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5701526571:AAHj4t7GN4T6uTdjjKnp1LBvUYtgFaaygpg'

candy = 0
step = 0


def start(update, context):
    update.message.reply_text(
        "Привет! Давай поиграем!",
        reply_markup=markup
    )


def play(update, context):
    update.message.reply_text(
        'Введите количество конфент на кону', reply_markup=stop_markup)
    return 1


def play_get_candy(update, context):
    global candy
    global step
    candy = int(update.message.text)
    update.message.reply_text('Сколько конфет вы возьмете?')
    return 2


def step_control(update, context):
    global candy
    global step
    step = int(update.message.text)
    if step > candy:
        update.message.reply_text('Столько конфет нет.Попробуй снова!')
        return 2
    elif step > 28:
        update.message.reply_text(f'Максимальный ход 28 конфет!')
        return 2
    else: 
        return 3


def player_1(update, context):
    global candy
    global step
    try:
        candy -= step
        update.message.reply_text(f'Конфет осталось {candy}')
        if candy > 28:
            temp = random.randint(1, 29)
            candy -= temp
            update.message.reply_text(
                f'Бот взял {temp} конфет.Конфет осталось {candy}.')
            if candy > 28:
                update.message.reply_text('Сколько конфет вы возьмете?')
                return 2
            else:
                update.message.reply_text(
                    'Вы победили!!!', reply_markup=markup)
                context.bot.send_document(
                    chat_id=update.effective_chat.id, document='http://vamotkrytka.my1.ru/_ph/85/2/69652083.gif?1668348596')
                return CommandHandler.END
        else:
            update.message.reply_text('Победил Бот', reply_markup=markup)
            return CommandHandler.END
    except ValueError:
        update.message.reply_text('Введите число')
        return 3


def stop(update, context):
    update.message.reply_text("Всего доброго!", reply_markup=markup)
    return ConversationHandler.END


def info(update, context):
    update.message.reply_text(
        "Правила игры.")


def close(update, context):
    update.message.reply_text(
        "Спасибо за игру",
        reply_markup=ReplyKeyboardRemove())


play_handler = ConversationHandler(
    entry_points=[CommandHandler('play', play)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, play_get_candy)],
        2: [MessageHandler(Filters.text & ~Filters.command, step_control)],
        3: [MessageHandler(Filters.text & ~Filters.command, player_1)]

    },

    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(play_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("info", info))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
