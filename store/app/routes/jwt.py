import jwt  # Importing the PyJWT library to handle JWT encoding and decoding
import datetime  # Importing datetime for handling the token expiration time

# JWT configuration constants
JWT_SECRET_KEY = "sapatoes"  # Replace this with a strong secret key (for signing the JWT securely)
JWT_ALGORITHM = "HS256"  # HS256 is a widely used algorithm for signing JWTs
JWT_EXPIRATION_TIME = 3600  # Token expiration time set to 1 hour (in seconds)


def create_jwt_token(username):
    """
    Generate a JWT token for the given username.
    
    Args:
        username (str): The username to include in the token's payload.

    Returns:
        str: A signed JWT token as a string.
    """
    # Set the expiration time for the token by adding JWT_EXPIRATION_TIME seconds to the current time (UTC)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_TIME)
    
    # The payload (data stored in the token) includes:
    # - `username`: the user's username (passed in as an argument)
    # - `exp`: the expiration timestamp (automatically verified by PyJWT when decoding)
    payload = {
        "username": username,
        "exp": expiration_time
    }
    
    # Generate the token by encoding the payload with the secret key and algorithm
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token  # Return the signed JWT as a string


def decode_jwt_token(token):
    """
    Decode and verify a JWT token.
    
    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload if the token is valid.
    
    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid in any way.
    """
    try:
        # Decode the token using the secret key and algorithm
        # This also checks the `exp` claim automatically (raises an error if expired)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload  # Return the payload if token is valid
    
    except jwt.ExpiredSignatureError:
        # Raised if the token is expired
        raise jwt.ExpiredSignatureError("The token has expired.")
    
    except jwt.InvalidTokenError:
        # Raised if the token is invalid in any way
        raise jwt.InvalidTokenError("The token is invalid.")

'''
Summary of jwt.py
1. 1JWT Configuration Constants:
    JWT_SECRET_KEY: Used to sign and verify JWTs. This should ideally be stored securely (e.g., as an environment variable).
    JWT_ALGORITHM: Specifies the signing algorithm (HS256 in this case).
    JWT_EXPIRATION_TIME: Sets the token’s expiration to 1 hour from the time of creation.
    
2. create_jwt_token(username):
    Generates a JWT that contains a payload with:
    username: The user’s username.
    exp: Expiration time in UTC (set to 1 hour from token creation).
    The token is signed using JWT_SECRET_KEY and JWT_ALGORITHM, and is returned as a signed JWT string.


3. decode_jwt_token(token):
    Decodes and verifies a JWT.
    Checks the token’s expiration and validates the signature using the secret key and algorithm.
    If the token is expired or invalid, raises an appropriate exception (ExpiredSignatureError or InvalidTokenError).


'''