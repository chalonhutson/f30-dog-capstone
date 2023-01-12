from src import app
from src.model import connect_to_db

if __name__ == "__main__":
    connect_to_db(app)