import telepot
import datetime
from decouple import config

API_KEY = config('TELEGRAM_API_KEY')

bot = telepot.Bot(API_KEY)
# rec = "-1001762239055"


def send_message( id , complain_title, complain_text, photo_url, region, city, authority_responsible):
    text = "Title :  " + complain_title + "\n\n"
    text += "Date : " + str(datetime.date.today()) + "\n\n"
    text += complain_text + "\n\n"
    text += f"Region : {region}\n\n"
    text += f"city : {city}\n\n"
    autho_info = "Authorities Responsible : " + authority_responsible + "\n\n"
    text += autho_info

    if photo_url != "":
        bot.sendPhoto(chat_id="-1001762239055", photo=photo_url, caption=text)
        bot.sendPhoto(chat_id=id,photo=photo_url,caption=text)
    else:
        bot.sendMessage(chat_id="-1001762239055", text=text)
        bot.sendMessage(chat_id=id, text=text)

    

def sample():
    title = "Public Garden getting dirty on weekends"
    complain_text = "A public garden near sobo center becomes extremely dirty during weekends and becomes really " \
                    "difficult to walk. "
    image_url = "https://c8.alamy.com/comp/2A46PKD/garbage-in-public-garden-2A46PKD.jpg"
    region = "Sobo center , South Bopal"
    city = "Ahmedabad"
    authority = ["XYZ authority 1", "XYZ authority 2"]

    send_message(title, complain_text, image_url, region, city, authority)


