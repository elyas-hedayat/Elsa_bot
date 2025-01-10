import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from the root of the project
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)


class Config:
    # Bot Configuration
    API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

    # API Keys
    METIS_API_KEY = os.getenv('METIS_API_KEY')
    BOT_ID = os.getenv('BOT_ID')

    # Feature Limits
    MAX_DAILY_SEARCHES = int(os.getenv('MAX_DAILY_SEARCHES', '3'))

    # API Endpoints
    METIS_BASE_URL = os.getenv('METIS_BASE_URL', 'https://api.metisai.ir/api/v1')
    METIS_BASE_SESSION_URL = os.getenv("METIS_BASE_SESSION_URL", 'https://api.metisai.ir/api/v1/chat/session')

    @classmethod
    def get_chat_message_url(cls, session_id):
        return f'{cls.METIS_BASE_URL}/chat/session/{session_id}/message'
