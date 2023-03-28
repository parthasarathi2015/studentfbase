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
        return pyrebase.initialize_app(firebaseConfig) 
    except:
        pass
    return None


def get_fb_auth():
    fb = get_fb()
    auth = fb.auth()
    try:
        user = auth.sign_in_with_email_and_password(os.getenv('FB_USER'),os.getenv('FB_PASSWORD'))
    except:
        user = None
        
    return user




# testuser1@gmail.com / Testuser1@1234
