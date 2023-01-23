import json
""" database dependencies to support sqliteDB examples """

from random import randrange
import os, base64
import json

from __init__ import *

import os
import base64

from random import randrange
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

import string
import random

class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, userID, note, image):
        self.userID = userID
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.rollback()
            return None
    
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }

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

class User(db.Model):   
    
    __tablename__ = "users"  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _pwd = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _highScore = db.Column(db.Integer, primary_key=False)
        
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)
        
    def __init__(self, name, email, uid, pwd=''.join(random.choices(string.ascii_uppercase + string.digits, k=7)), highScore=""):
        self._name = name
        self._pwd = pwd
        self._email = email
        self._highScore = highScore
        self._uid = uid

        
    #getter and setter for the username property
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    # getter and setter for the email property
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
    
    # getter and setter for password property along with adding basic security measures
    @property
    def pwd(self):
        return self._pwd
    
    @pwd.setter
    def pwd(self, pwd):
        self._pwd = generate_password_hash(pwd, method='sha256')

    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._pwd, password)
        return result
    
    # getter and setter for high score property
    @property
    def highScore(self):
        return self._highScore
    
    @highScore.setter
    def highScore(self, highScore):
        self._highScore = highScore
    
    # getter and setter for uid
    @property 
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self, uid):
        self._uid = uid
    
    # json dump code :)
    def __str__(self):
        return json.dumps(self.read())
    
    
    # Implemenation of CRUD for user records
    def CREATE(self):
        try:
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "name": self._name,
            "uid": self._uid,
            "pwd": self._pwd,
            "email": self._email,
            "high score": self._highScore,
            "posts": [post.read() for post in self.posts]
        }

    def UPDATE(self, highScore, name = "", uid = "", pwd = "", userID = ""):
        if len(name)>0:
            self.name = name
        if len(uid)>0:
            self.uid = uid
        if len(pwd)>0:
            self.pwd = pwd
        if highScore>0:
            self.highScore = highScore
        if len(userID)>0:
            self.userID = userID
    
    def DELETE(self):
        db.session.delete(self)
        db.session.commit()
        return None
        
        
    # Database Creation Stuff
    
def initUsers():
    db.create_all()
    # Testing Data
    u1 = User(name='h4seeb', pwd='ILOVETHISCLASS100', email='mirzahaseebbeg@yahoo.com', highScore= 3, uid = "0")
    u2 = User(name='nathan', pwd='iAmSoSorry1000', email='sorry@hotmail.com', highScore=2, uid = "1")
    u3 = User(name='fishyflow', pwd='annoying', email='annoying@gmail.com', highScore=1, uid = "2")
    u4 = User(name='beab', pwd='ayee', email='annag@gmail.com', highScore=1, uid = "3")
    u5 = User(name='HEHHEHE', pwd='idkanymore', email='ZESTYY@gmail.com', highScore=1, uid = "4")

    users = [u1, u2, u3, u4, u5]

    for user in users:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(userID='users.id', note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.CREATE()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.uid}")


# if __name__ == "__main__":
    

#     print("JSON ready string:\n", u1, "\n") 
#     print("Raw Variables of object:\n", vars(u1), "\n") 
#     print("Raw Attributes and Methods of object:\n", dir(u1), "\n")
#     print("Representation to Re-Create the object:\n", repr(u1), "\n") 
    
        
#     print("JSON ready string:\n", u2, "\n") 
#     print("Raw Variables of object:\n", vars(u2), "\n") 
#     print("Raw Attributes and Methods of object:\n", dir(u2), "\n")
#     print("Representation to Re-Create the object:\n", repr(u2), "\n") 


