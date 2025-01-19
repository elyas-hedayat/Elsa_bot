import requests

from config.config import Config


def process_ai_chat_handler(message, session_id):
    url = Config.get_chat_message_url(session_id=session_id)
    headers = {
        'Authorization': f'Bearer {Config.METIS_API_KEY}',
        'Content-Type': 'application/json'
    }
    print(message)
    data = {
        "message": {
            "content": message,
            "type": "USER"
        }
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        ai_response = response.json().get('content', 'No response from AI')
        return ai_response
    else:
        print(response.content)
        return "Failed to get response from AI. Please try again."
