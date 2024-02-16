from functools import wraps
from flask import redirect, request
import jwt
import secrets
from models import User  # Adjust the import based on your project structure

# Secret key for encoding and decoding JWTs (keep this secret!)
secret_key = secrets.token_urlsafe(32)

def create_token(user_id):
    # Create a JWT token with the user_id as the payload
    return jwt.encode({'user_id': user_id}, secret_key, algorithm='HS256')

def decode_token(token):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(f"Decoded Payload: {payload}")
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

def get_user_details(user_id):
    # Fetch user details from the database (replace this with your actual database query)
    user = User.query.filter_by(chat_id=user_id).first()
    if user:
        return {'chat_id': user.chat_id}
    else:
        return None

def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')
        print(token)
        if not token:
            print('cookies token problem')
            # Redirect to the login page or return an unauthorized response
            return redirect('/login')  # Adjust the URL to your login route

        user_id = decode_token(token)

        if user_id is None:
            print('cookies user_id problem')
            print(user_id)
            # Redirect to the login page or return an unauthorized response
            return redirect('/login')  # Adjust the URL to your login route

        # Fetch user details from the database
        user_details = get_user_details(user_id)

        if user_details is None:
            print('cookies user_details problem')
            # Handle the case where user details are not found
            return redirect('/login')  # Adjust the URL to your login route

        # Attach the user details to the request for easy access in the route
        request.chat_id = int(user_details.get('chat_id', None))

        return f(*args, **kwargs)

    return decorated_function
