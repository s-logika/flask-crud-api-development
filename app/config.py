from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('root')}:{os.getenv('root123')}"
        f"@{os.getenv('local')}/{os.getenv('flask_crud_db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False