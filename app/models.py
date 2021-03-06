from app import bcrypt, db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

class Recipe(db.Model):
    
    __tablename__='recipes'
    
    id=db.Column(db.Integer, primary_key=True)
    recipe_title=db.Column(db.String, nullable=False)
    recipe_description=db.Column(db.String, nullable=False)
    is_public=db.Column(db.Boolean, nullable=False)
    image_filename=db.Column(db.String, default=None, nullable=True)
    image_url=db.Column(db.String, default=None, nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
        
    def __init__(self, title, description, user_id, is_public, image_filename=None, image_url=None):
        self.recipe_title=title
        self.recipe_description=description
        self.is_public=is_public
        self.image_filename=image_filename
        self.image_url=image_url
        self.user_id=user_id
                
    def __repr__(self):
        return '<Title {}>'.format(self.title)
    
class User(db.Model):

    __tablename__='users'
    
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String, unique=True, nullable=False)
    _password=db.Column(db.Binary(60), nullable=False)
    authenticated=db.Column(db.Boolean, default=False)
    email_confirmation_sent_on=db.Column(db.DateTime, nullable=True)
    email_confirmed=db.Column(db.Boolean, nullable=False)
    email_confirmed_on=db.Column(db.DateTime, nullable=True)
    registered_on=db.Column(db.DateTime, nullable=True)
    last_logged_in=db.Column(db.DateTime, nullable=True)
    current_logged_in=db.Column(db.DateTime, nullable=True)
    role=db.Column(db.String, default='user')
    recipes=db.relationship('Recipe', backref='user', lazy='dynamic')
    
    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'): 
        self.email=email
        self.password=plaintext_password
        self.authenticated=False
        self.email_confirmation_sent_on=email_confirmation_sent_on
        self.email_confirmed=False
        self.email_confirmed_on=None
        self.registered_on=datetime.now()
        self.last_logged_in=None
        self.current_logged_in=datetime.now()
        self.role=role

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password=bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        '''Return True if user is authenticated'''
        return bcrypt.check_password_hash(self.password, plaintext_password)
    
    @property
    def is_authenticated(self):
        '''Return True is user is authenticated'''
        return self.authenticated

    @property
    def is_active(self):
        '''Always True. All users are active'''
        return True

    @property
    def is_anonymous(self):
        '''Always False. Anonymous users are not supported'''
        return False

    def get_id(self):
        '''Return the email address to satisfy Flask-Login requirements'''
        '''Requires use of Python 3'''
        return str(self.id)
    
    def __repr__(self): 
        return '<User {}>'.format(self.name)
