# auth.py
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User  # Assuming the User model is imported here (modify as necessary)
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import jwt  # Import PyJWT for JWT decoding/encoding
from jwt import create_jwt_token, decode_jwt_token  # Import JWT functions from jwt.py (modify the import if needed)

app = Flask(__name__)

# Your SQLite Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/goody/Library/Mobile Documents/com~apple~CloudDocs/Code/Projects/Sapatoes1/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "sneaker"  # For session or other uses; consider securing this better.
db = SQLAlchemy(app)

# Routes
@app.route("/")
def home():
    return render_template("index.html")


# Login route: Now using JWT for authentication
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Raw SQL Query to find the user's password hash
    result = db.session.execute(
        text("SELECT password_hash FROM user WHERE username = :username"),
        {"username": username}
    ).fetchone()

    if result:
        user_password_hash = result[0]  # Fetch the first column (password_hash)

        if check_password_hash(user_password_hash, password):
            # Password matched, generate a JWT token
            token = create_jwt_token(username)
            return jsonify({"token": token})  # Return the JWT token to the client
        else:
            return render_template("index.html", error="Invalid credentials")
    else:
        return render_template("index.html", error="User not found")


# Register route: Using raw SQL and password hashing
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if the user already exists using raw SQL query with `text()`
    existing_user = db.session.execute(
        text("SELECT username FROM user WHERE username = :username"),
        {"username": username}
    ).fetchone()

    if existing_user:
        return render_template("index.html", error="User Already Exists!")
    else:
        try:
            # Hash the password before storing it in the database
            password_hash = generate_password_hash(password)

            # Insert new user into the database using raw SQL query
            db.session.execute(
                text("INSERT INTO user (username, password_hash) VALUES (:username, :password_hash)"),
                {"username": username, "password_hash": password_hash}
            )
            db.session.commit()  # Commit the transaction

            # After successful registration, generate a JWT token
            token = create_jwt_token(username)
            return jsonify({"token": token})  # Return the JWT token to the client
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback if there’s an error
            return render_template("index.html", error="Error occurred while registering the user. Please try again.")


# Dashboard route: Protected by JWT token
@app.route("/dashboard")
def dashboard():
    token = request.headers.get("Authorization")  # Expect the token to be in the Authorization header

    if token:
        try:
            # Decode and validate the JWT token
            payload = decode_jwt_token(token)
            username = payload["username"]  # Retrieve the username from the payload
            return render_template("dashboard.html", username=username)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("home", error="Session expired, please log in again"))
        except jwt.InvalidTokenError:
            return redirect(url_for("home", error="Invalid token, please log in again"))
    else:
        return redirect(url_for("home", error="Token required, please log in first"))


if __name__ == "__main__":
    app.run(debug=True)
