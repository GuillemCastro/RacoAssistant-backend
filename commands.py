from BotConfig import BotConfig
import FIB

def start(bot, update):
    reply = "Hi! I'm RacoAssistant, a bot that will blablabla." \
    " Please follow <a href=\"" + FIB.get_auth_url(BotConfig.client_id, BotConfig.complete_host, update.effective_user.id) + "\">this link</a> to authorize the bot"
    update.message.reply_text(reply, parse_mode='HTML')

def stop(bot, update):
    update.message.reply_text("<a href=\"www.hackupc.com\">hackupc</a>", parse_mode="HTML")