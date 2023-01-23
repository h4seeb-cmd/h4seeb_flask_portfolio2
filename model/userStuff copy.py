# import json
# """ database dependencies to support sqliteDB examples """

# from random import randrange
# from datetime import date
# import os, base64
# import json

# from __init__ import app, db
# from sqlalchemy.exc import IntegrityError
# from werkzeug.security import generate_password_hash, check_password_hash


# class Post(db.Model):
#     __tablename__ = 'posts'

#     # Define the Notes schema
#     id = db.Column(db.Integer, primary_key=True)
#     note = db.Column(db.Text, unique=False, nullable=False)
#     image = db.Column(db.String, unique=False)
#     # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
#     userID = db.Column(db.Integer, db.ForeignKey('users.id'))

#     # Constructor of a Notes object, initializes of instance variables within object
#     def __init__(self, id, note, image):
#         self.userID = id
#         self.note = note
#         self.image = image

#     # Returns a string representation of the Notes object, similar to java toString()
#     # returns string
#     def __repr__(self):
#         return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

#     # CRUD create, adds a new record to the Notes table
#     # returns the object added or None in case of an error
#     def create(self):
#         try:
#             # creates a Notes object from Notes(db.Model) class, passes initializers
#             db.session.add(self)  # add prepares to persist person object to Notes table
#             db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
#             return self
#         except IntegrityError:
#             db.session.remove()
#             return None

#     # CRUD read, returns dictionary representation of Notes object
#     # returns dictionary
#     def read(self):
#         # encode image
#         path = app.config['UPLOAD_FOLDER']
#         file = os.path.join(path, self.image)
#         file_text = open(file, 'rb')
#         file_read = file_text.read()
#         file_encode = base64.encodebytes(file_read)
        
#         return {
#             "id": self.id,
#             "userID": self.userID,
#             "note": self.note,
#             "image": self.image,
#             "base64": str(file_encode)
#         }

# class User:   
#     def __init__(self, username, pwd, email, highScore, uid):
#         self._username = username
#         self._pwd = pwd
#         self._email = email
#         self._highScore = highScore
#         self._uid = uid
#     #getter and setter for the username property
#     @property
#     def username(self):
#         return self._username
    
#     @username.setter
#     def username(self, username):
#         self._username = username
    
#     # getter and setter for the email property
#     @property
#     def email(self):
#         return self._email
    
#     @email.setter
#     def email(self, email):
#         self._email = email
    
#     # getter and setter for password property along with adding basic security measures
#     @property
#     def pwd(self):
#         return self._pwd
    
#     @pwd.setter
#     def pwd(self, pwd):
#         self._pwd = generate_password_hash(pwd, method='sha256')

#     def is_password(self, password):
#         """Check against hashed password."""
#         result = check_password_hash(self._pwd, password)
#         return result
    
#     # getter and setter for high score property
#     @property
#     def highScore(self):
#         return self._highScore
    
#     @highScore.setter
#     def highScore(self, highScore):
#         self._highScore = highScore
    
#     # getter and setter for uid
#     @property 
#     def uid(self):
#         return self._uid
    
#     @uid.setter
#     def uid(self, uid):
#         self._uid = uid
    
#     # json dump code :)
#     def __str__(self):
#         return json.dumps({'username': self._username, 'pwd': self._pwd, 'email': self._email, 'highScore': self._highScore, 'uid': self._uid})
    
#     def __repr__(self):
#         return f'User(username={self._username}, pwd={self._pwd}, email={self._email}, highScore={self._highScore}, uid={self._uid})'
    

# if __name__ == "__main__":
    
#     u1 = User(username='h4seeb', pwd='ILOVETHISCLASS100', email='mirzahaseebbeg@yahoo.com', highScore= 3, uid = "0")
#     u2 = User(username='nathan', pwd='iAmSoSorry1000', email='sorry@hotmail.com', highScore=2, uid = "1")
    
#     print("JSON ready string:\n", u1, "\n") 
#     print("Raw Variables of object:\n", vars(u1), "\n") 
#     print("Raw Attributes and Methods of object:\n", dir(u1), "\n")
#     print("Representation to Re-Create the object:\n", repr(u1), "\n") 
    
        
#     print("JSON ready string:\n", u2, "\n") 
#     print("Raw Variables of object:\n", vars(u2), "\n") 
#     print("Raw Attributes and Methods of object:\n", dir(u2), "\n")
#     print("Representation to Re-Create the object:\n", repr(u2), "\n") 