import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config


config_dict = get_default_config()
config_dict['language'] = 'ua'

owm = OWM('849b5fda8bbe5a7b07a9f991a13633b1', config_dict)
mgr=owm.weather_manager()


bot = telebot.TeleBot("6618552597:AAE90oYpBe_07LqdClgZC7CkvWn8WswSBe4")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привіт, я погодний бот. В якому місті/країні ви хотіли б дізнатись погоду?")

@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]

    answer= "В місті " + message.text + " зараз " + w.detailed_status + "\n"
    answer+= "Температура зараз приблизно " + str(temp) + "\n\n"


    if temp<10:
        answer+= "Зараз прохолодно, одягайтесь тепліше!!"
    elif temp>10 and temp<20:
        answer+="Зараз досить прохолодно, можно вдягнутись у спортивний костюм!"
    elif temp>20 and temp<30:
        answer+="Зараз тепло, можно вдягнути щось легке"
    elif temp>30:
        answer+="Зараз спека, вдягайтесь якомога легше!!"
    else:
        pass

        
    bot.send_message(message.chat.id, answer)
        
   
bot.infinity_polling(none_stop= True)

