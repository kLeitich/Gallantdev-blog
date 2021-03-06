
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog',backref = 'users',lazy="dynamic")
    comments = db.relationship('Comment',backref = 'users',lazy="dynamic")
    subscribers = db.relationship('Subcription',backref = 'users',lazy="dynamic")

    
   

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def get_pic_path(cls,profile_pic_path):

        return User.query.filter_by(profile_pic_path=profile_pic_path)

    def __repr__(self):
        return f'User {self.username}'

    


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Blog(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String)
    blogTitle=db.Column(db.String)
    blogContent = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    updatedPosted= db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref='post',lazy='dynamic')
    

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_blog(cls):
        '''
        Function that queries the databse and returns all the blogs
        '''
        return Blog.query.all()

    @classmethod
    def get_blogs_by_category(cls,category):
        '''
        Function that queries the databse and returns pitches based on the
        category passed to it
        '''
        return Blog.query.filter_by(category= category)

    def _repr_(self):
        return f'Blog{self.category}'


class Comment(db.Model):

    __tablename__= "comments"

    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()

        return comments

    @classmethod
    def delete_comments(cls,comment):
        db.session.delete(comment)
        db.session.commit()
    def _repr_(self):
        return f'Blog{self.comment}'


class Subcription(db.Model):
    __tablename__='subcribers'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def _repr_(self):
        return f'Subcription{self.subscriber}'

    