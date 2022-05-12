# Telegram Bot

## Usage

* Docker Run Command

```shell
docker run -d --name=telebot  \
       -e TELEBOT_TOKEN="Telegram Bot API token"\
       -e TELEBOT_SHODAN_API_KEY="Shodan API key" \
       -e ENV_FOR_DYNACONF="production" \ 
       wdnmdcyka/telebot:latest
```