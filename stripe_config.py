import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
from flask import Flask, redirect, url_for
from stripe_config import stripe


stripe.api_version = '2023-10-16'

from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__, static_folder='dist',
  static_url_path='/<path:path>', template_folder='dist')


if __name__ == '__main__':
    app.run(port=4242)

