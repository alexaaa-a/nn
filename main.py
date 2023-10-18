import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6452713344:AAFeRc8G0KZSGL0ZWiEWYmYrkYqs5lbFX84",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Познакомиться"
text_button_1 = "Месяцы"
text_button_2 = "Дни недели"
text_button_3 = "500 слов"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Давай познакомимся!',
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Как я могу к тебе обращаться?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Отлично! Подскажи, сколько тебе лет?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Приятно познакомиться!', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Здесь] (https://ru.speaklanguages.com/%D0%B8%D1%82%D0%B0%D0%BB%D1%8C%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B9/%D0%BB%D0%B5%D0%BA%D1%81%D0%B8%D0%BA%D0%B0/%D0%BC%D0%B5%D1%81%D1%8F%D1%86%D1%8B-%D0%B8-%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B0-%D0%B3%D0%BE%D0%B4%D0%B0) ты можешь изучить времена года и месяцы на итальянском языке",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Здесь] (https://lingo.com.ru/settimana-mese-anno) ты можешь изучить дни недели на итальянском языке, и то, как правильно их использовать в предложениях",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Здесь] (https://poligloty.blogspot.com/2013/10/500-slov-italyanskogo-yazyka.html) ты можешь изучить 500 широко употребимых слов в итальянском языке",
                     reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()