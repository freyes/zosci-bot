#!/usr/bin/env python3
import logging

from mmpy_bot import Bot, Settings
from zosci_bot.plugins import ZOSCIBotPlugin, PrometheusPlugin
from zosci_bot.config import load_config


def setup_logging(config):
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('mattermostdriver.websocket').setLevel(logging.WARN)
    logging.getLogger('websockets.client').setLevel(logging.ERROR)

def main():
    config = load_config('myconfig.yaml')
    setup_logging(config)
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL=config["mattermost"]["url"],
            MATTERMOST_PORT=config["mattermost"]["port"],
            #MATTERMOST_API_PATH=config["mattermost"]["api_path"],
            BOT_TOKEN=config["mattermost"]["token"],
            BOT_TEAM=config["mattermost"]["team"],
            SSL_VERIFY=config["mattermost"]["ssl_verify"],
        ),
        plugins=[ZOSCIBotPlugin(config),
                 PrometheusPlugin(config)],
    )
    bot.run()


if __name__ == '__main__':
    main()
