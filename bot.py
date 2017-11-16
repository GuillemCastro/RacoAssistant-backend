from telegram.ext import (Updater, CommandHandler)
import commands
from BotConfig import BotConfig
from threading import Thread

import AuthServer
import queue

def auth_thread():
    auth_queue = queue.Queue()
    auth_server = AuthServer.AuthServer(("0.0.0.0", BotConfig.port), AuthServer.AuthRequestHandler, auth_queue)
    auth_server.serve_forever()

def main():
    BotConfig.load_config("config.ini")
    updater = Updater(BotConfig.bot_token)

    th = Thread(target=auth_thread, args=())
    th.start()

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(CommandHandler('stop', commands.stop))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("""
  _____                                    _     _              _   
 |  __ \                     /\           (_)   | |            | |  
 | |__) |__ _  ___ ___      /  \   ___ ___ _ ___| |_ __ _ _ __ | |_ 
 |  _  // _` |/ __/ _ \    / /\ \ / __/ __| / __| __/ _` | '_ \| __|
 | | \ \ (_| | (_| (_) |  / ____ \\__ \__ \ \__ \ || (_| | | | | |_ 
 |_|  \_\__,_|\___\___/  /_/    \_\___/___/_|___/\__\__,_|_| |_|\__|                                                              
    """)
    main()