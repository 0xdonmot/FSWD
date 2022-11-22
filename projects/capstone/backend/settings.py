from dotenv import load_dotenv
import os

load_dotenv()

# db settings
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USERNAME = os.environ.get("DB_USERNAME")
DATABASE_URL = os.environ.get('DATABASE_URL')

database_config = DATABASE_URL

# auth settings
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

casting_assistant_auth = os.environ.get('casting_assistant_auth')
casting_director_auth = os.environ.get('casting_director_auth')
executive_producer_auth = os.environ.get('executive_producer_auth')
