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

    def UPDATE(self, highScore, name = "", uid = "", pwd = ""):
        if len(name)>0:
            self.name = name
        if len(uid)>0:
            self.uid = uid
        if len(pwd)>0:
            self.pwd = pwd
        if highScore>0:
            self.highScore = highScore
    def DELETE(self):
        db.session.delete(self)
        db.session.commit()
        return None
        
        
    # Database Creation Stuff
    
def initUsers():
        with app.app_context():
            db.create_all()
        """Tester data for table"""
        u1 = User(name='Thomas Edison', uid='toby', pwd='123toby', highScore=3)
        u2 = User(name='Nicholas Tesla', uid='niko', pwd='3242haseeb', highScore=4)
        u3 = User(name='Alexander Graham Bell', uid='lex', pwd='123lex', highScore=1)
        u4 = User(name='Eli Whitney', uid='whit', pwd='123whit', highScore=5)
        u5 = User(name='John Mortensen', uid='jm1021', pwd='bobTheBuilder', highScore=2)

        users = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")