from dotenv import load_dotenv
import os

# Parse a .env file and then load all the variables found as environment variables.
load_dotenv()
API_KEY = os.environ["API_KEY"]
API_SECRETE = os.environ["API_SECRETE"]
DB_HOST = os.environ["DB_HOST"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
