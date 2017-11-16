from BotConfig import BotConfig
import FIB

def start(bot, update):
    reply = "Hi! I'm RacoAssistant, a bot that will blablabla. " \
            "Please follow this link to authorize the bot: \n" + FIB.get_auth_url(BotConfig.client_id, BotConfig.complete_host,
                                                                                  update.effective_user.id)
    print(reply)
    update.message.reply_text(reply)

def stop(bot, update):
    update.message.reply_text("<a href=\"www.hackupc.com\">hackupc</a>", parse_mode="HTML")