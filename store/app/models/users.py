from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(25), unique=True, nullable=False)
    password = mapped_column(String(128), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    def check_password_strength(self, password):
        upperChars, lowerChars, specialChars, digits, length = 0, 0, 0, 0, len(password)

        if length < 8:
            return "Password must be at least 8 characters long!"

        for char in password:
            if char.isupper():
                upperChars += 1
            elif char.islower():
                lowerChars += 1
            elif char.isdigit():
                digits += 1
            else:
                specialChars += 1
                
        if upperChars > 0 and lowerChars > 0 and digits > 0 and specialChars > 0:
            return "The strength of password is strong." if length >= 10 else "The strength of password is medium."
        else:
            messages = []
            if upperChars == 0:
                messages.append("Password must contain at least one uppercase character!")
            if lowerChars == 0:
                messages.append("Password must contain at least one lowercase character!")
            if specialChars == 0:
                messages.append("Password must contain at least one special character!")
            if digits == 0:
                messages.append("Password must contain at least one digit!")
            return " ".join(messages)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
