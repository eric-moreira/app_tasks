from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from dotenv import load_dotenv
import os

def create_app():

    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL')

    # Connect to the database
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    db.init_app(app)

    return app

