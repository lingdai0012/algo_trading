from dotenv import load_dotenv
import os

# Parse a .env file and then load all the variables found as environment variables.
load_dotenv()
API_KEY = os.environ["API_KEY"]
API_SECRETE = os.environ["API_SECRETE"]
