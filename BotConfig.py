import configparser

class BotConfig:

    bot_token = ""
    client_secret = ""
    client_id = ""
    host = ""
    port = 0
    complete_host = ""

    @classmethod
    def load_config(cls, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        cls.client_id = config['FIB']['ClientID']
        cls.client_secret = config['FIB']['ClientSecret']
        cls.bot_token = config['Telegram']['Token']
        cls.host = config['URLS']['Host']
        cls.port = int(config['URLS']['Port'])
        cls.complete_host = cls.host + ":" + str(cls.port)