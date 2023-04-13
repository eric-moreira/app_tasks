from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from bcrypt import hashpw, gensalt, checkpw
from modules.auth import auth_blueprint
from modules.tasks import task_blueprint
from models.models import User, Task
from extensions import db
from __init__ import create_app
import secrets

app = create_app()

app.secret_key = secrets.token_hex(16)

# Registre a blueprint auth com o db
app.register_blueprint(auth_blueprint)
app.register_blueprint(task_blueprint)


# The "@" decorator associates this route with the function immediately following
@app.route('/')
def index():
    return render_template('index.html')



# Run the app in debug mode.
if __name__ == "__main__":
    app.run(debug=True)

