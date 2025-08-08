from flask import Flask
from dotenv import load_dotenv
from .dashboard import app as dash_app

# Load environment variables from .env file
load_dotenv()

# The Flask server instance
server = Flask(__name__)

# Link the Dash app to the Flask server
dash_app.server = server

if __name__ == '__main__':
    # This block is for local development without Gunicorn/Docker
    server.run(debug=True)