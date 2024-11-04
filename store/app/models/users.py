from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(25), unique=True, nullable=False)
    password = mapped_column(String(128), nullable=False)
    
    def checkPassword(password):
        upperChars, lowerChars, specialChars, digits, length = 0, 0, 0, 0, 0
        length = len(password)
        
        if (length < 8):
            print("Password must be at least 8 characters long!\n")
        else:
            for i in range(0, length):
                if(password[i].isUpper()):
                    upperChars += 1
                elif(password[i].isLower()):
                    lowerChars += 1
                elif(password[i].isdigit()):
                    digits +=1
                else:
                    specialChars +=1
                    
        if (upperChars != 0 and lowerChars != 0 and digits != 0 and specialChars != 0):
            if (length >= 10):
                print("The strength of password is strong.\n")
            else:
                print("The strength of password is medium.\n")
        else:
            if (upperChars == 0):
                print("Password must contain at least one uppercase character!\n")
            if (lowerChars == 0):
                print("Password must contain at least one lowercase character!\n")
            if (specialChars == 0):
                print("Password must contain at least one special character!\n")
            if (digits == 0):
                print("Password must contain at least one digit!\n")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
