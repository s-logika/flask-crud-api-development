from flask import Flask
from config import Config
from models import db
from router import register_routes

app = Flask(__name__)

# Load Config
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Register Routes
register_routes(app)

# Create Tables
with app.app_context():
    db.create_all()
    print("Tables ready.")

if __name__ == "__main__":
    app.run(debug=True)