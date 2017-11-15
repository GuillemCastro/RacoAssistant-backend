import configparser
import FIB

config = configparser.ConfigParser()
config.read("config.ini")
client_id = config['FIB']['ClientID']
client_secret = config['FIB']['ClientSecret']
redirect_url = config['URLS']['Host']


def start(bot, update):
    reply = "Hi! I'm RacoAssistant, a bot that will blablabla. " \
            "Please follow this link to authorize the bot: \n" + FIB.get_auth_url(client_id, redirect_url,
                                                                                  update.effective_user.id)
    print(reply)
    update.message.reply_text(reply)

def stop(bot, update):
    update.message.reply_text("<a href=\"www.hackupc.com\">hackupc</a>", parse_mode="HTML")