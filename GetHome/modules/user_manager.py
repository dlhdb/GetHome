import google.oauth2.id_token
import google.auth.transport.requests
import logging

from app_config import config

logger = logging.getLogger()

def validate_google_token(token):
    CLIENT_ID = config['env_vars']['google_oauth']['CLIENT_ID']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = google.oauth2.id_token.verify_oauth2_token(
            token, google.auth.transport.requests.Request(), CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        logger.info("userid: " + userid)
        
        return True
    except ValueError:
        # Invalid token
        return False