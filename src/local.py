"""
This module contains the local application for development.
"""
from dotenv import load_dotenv
from app import app

load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
