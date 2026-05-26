from flask import Flask
from config import Config
from models import db
from routers import register_routes

app = Flask(__name__)

# Load Config
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Register Routes
register_routes(app)

# Create Tables
with app.app_context():
    db.create_all()
    print("Tables created successfully.")

if __name__ == "__main__":
    app.run(debug=True)
    