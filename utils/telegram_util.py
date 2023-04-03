import requests
def send_telegram_msg(msg,config):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage?chat_id={config.TELEGRAM_CHAT_ID}&text={msg}"
    print(requests.get(url).json())