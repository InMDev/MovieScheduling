from flask import Flask

# Create the Flask application instance
app = Flask(__name__, template_folder='templates')


from app import routes