import requests

from config.config import Config


def create_metis_session(bot_id: str, content: str = '') -> str | None:
    """
    Creates a session with the Metis API.

    Args:
        bot_id (str): The ID of the bot to create a session for.
        content (str): The initial message content to start the session.

    Returns:
        Optional[str]: The session ID if successful, otherwise None.
    """
    url = Config.METIS_BASE_SESSION_URL
    headers = {
        'Authorization': f'Bearer {Config.METIS_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "botId": bot_id,
        "user": None,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        return response.json().get('id')
    except Exception as e:
        print(str(e))
        return None
