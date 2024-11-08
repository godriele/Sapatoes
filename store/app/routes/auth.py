from flask import Flask, request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User  # Assuming the User model is imported here
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = "sneaker"  # Required for session to work

# Your SQLite Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/goody/Library/Mobile Documents/com~apple~CloudDocs/Code/Projects/Sapatoes1/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")


# Login
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Raw SQL Query with `text()`
    result = db.session.execute(
        text("SELECT password_hash FROM user WHERE username = :username"),
        {"username": username}
    ).fetchone()  # Get the first result, as `username` should be unique

    if result:
        user_password_hash = result[0]  # Fetch the first column (password_hash)

        if check_password_hash(user_password_hash, password):
            session["username"] = username  # Store the username in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            return render_template("index.html", error="Invalid credentials")
    else:
        return render_template("index.html", error="User not found")


# Register
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

            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback if there’s an error
            return render_template("index.html", error="Error occurred while registering the user. Please try again.")


# Dashboard route
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html", username=session["username"])


if __name__ == "__main__":
    app.run(debug=True)
