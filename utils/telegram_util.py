def send_telegram_msg(msg,TOKEN = TOKEN, CHAT_ID = CHAT_ID):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    print(requests.get(url).json())