import requests

def send_telegram_msg(msg, config):
    """
    Sends a message to a Telegram chat using the Telegram Bot API.

    Args:
        msg (str): The message to be sent.
        config (Config): An instance of the Config dataclass containing the configuration information.

    Returns:
        None
    """
    # Construct the URL for the Telegram API endpoint
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage?chat_id={config.TELEGRAM_CHAT_ID}&text={msg}"

    # Send GET request to the Telegram API to send the message
    response = requests.get(url)

    # Return response
    return response
