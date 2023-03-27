import pyrebase
import os
from dotenv import load_dotenv
load_dotenv()

def get_fb():
    try:
        firebaseConfig = {
            "apiKey": os.getenv('apiKey'),
            "databaseURL": os.getenv('databaseURL'),
            "authDomain":  os.getenv('authDomain'),
            "projectId":  os.getenv('projectId'),
            "storageBucket":  os.getenv('storageBucket'),
            "messagingSenderId":  os.getenv('messagingSenderId'),
            "appId": os.getenv('appId'),
        }
        firebase =  pyrebase.initialize_app(firebaseConfig) 
        return firebase.database()
    except:
        pass
    return None

# testuser1@gmail.com / Testuser1@1234
