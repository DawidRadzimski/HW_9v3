from mongoengine import connect
import configparser

def connect_to_mongodb():
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'username')
    mongo_pass = config.get('DB', 'password')
    db_name = config.get('DB', 'database')
    host = config.get('DB', 'host')

    try:
        connect(host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{host}/{db_name}?retryWrites=true&w=majority", ssl=True)
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

if __name__ == "__main__":
    connect_to_mongodb()
