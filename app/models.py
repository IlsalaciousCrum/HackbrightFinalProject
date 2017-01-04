'''Models for K(i)ndTable WebApp.'''
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.hash import bcrypt
from . import db, login_manager

##############################################################################
# Model definitions


class User(db.Model):
    '''Registered users of KindTable WebApp.'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)
    _password = db.Column(db.String(128))
    email_verified = db.Column(db.Boolean, unique=False, default=False)

    parties = db.relationship('Party')

    user_profile = db.relationship('Profile', backref='user', post_update=True)

    saved_recipes = db.relationship('RecipeCard',
                                    secondary='recipebox',
                                    backref='users',
                                    post_update=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        """Encrypts a password for the user table."""

        h = bcrypt.encrypt(plaintext)
        self._password = h

    def verify_password(self, password):
        """Verifies a password from the user table."""

        if bcrypt.verify(password, self._password) is True:
            return True
        else:
            return False

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<User user_id=%s profile_id=%s \
        validated=%s>' % (self.user_id,
                          self.profile_id,
                          self.validated)


class Profile(db.Model):
    '''Information about users and their contacts'''

    __tablename__ = 'profiles'

    profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    is_user_profile = db.Column(db.Boolean, unique=False, default=False)
    email = db.Column(db.String(200), nullable=False, unique=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    # ie, ethical, religious, general health, specific health
    diet_reason = db.Column(db.String(120), nullable=True)
    profile_notes = db.Column(db.String(300), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    diet = db.relationship('Diet', backref='profiles', lazy='joined', post_update=True)

    avoidances = db.relationship('IngToAvoid', backref='profiles', lazy='joined', post_update=True)

    intolerances = db.relationship('Intolerance',
                                   secondary='userintolerances',
                                   backref='profiles',
                                   lazy='joined',
                                   post_update=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Profile profile_id=%s user_id=%s user_id=%s \
        is_user_profile=%s email=%s first_name=%s last_name=%s \
        diet_id=%s diet_reason=%s>' % (self.profile_id,
                                       self.user_id,
                                       self.is_user_profile,
                                       self.email,
                                       self.first_name,
                                       self.last_name,
                                       self.diet_id,
                                       self.diet_reason)


class Friend(db.Model):
    '''Makes connection between the user and their contact'''

    __tablename__ = 'friends'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    friend_profile_id = db.Column(db.Integer,
                                  db.ForeignKey('profiles.profile_id'),
                                  nullable=False)
    friendship_verified_by_email = db.Column(db.Boolean, unique=False,
                                             default=False)
    friendship_verified_by_facebook = db.Column(db.Boolean, unique=False,
                                                default=False)

    profile = db.relationship('Profile', backref='friend', post_update=True)
    user = db.relationship('User', backref='friends', post_update=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Friend record_id=%s user_id=%s  profile_id=%s \
        friendship_verified_by_email=%s \
        friendship_verified_by_facebook=%s>' % (self.record_id,
                                                self.user_id,
                                                self.profile_id,
                                                self.friendship_verified_by_email,
                                                self.friendship_verified_by_facebook)


class UserIntolerance(db.Model):
    '''Associates the intolerances that each user has.'''

    __tablename__ = 'userintolerances'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)
    intol_id = db.Column(db.Integer, db.ForeignKey('intolerances.intol_id'),
                         nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<UserIntolerance record_id=%s profile_id=%s \
        intol_id=%s>' % (self.record_id,
                         self.profile_id,
                         self.intol_id)


class Intolerance(db.Model):
    '''Spoonacular's list of possible intolerances.'''

    __tablename__ = 'intolerances'

    intol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intol_name = db.Column(db.String(64), nullable=False)
    intol_description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Intolerance int_id=%s int_name=%s \
        int_description=%s>' % (self.intol_id,
                                self.intol_name,
                                self.intol_description)


class Diet(db.Model):
    '''Spoonacular's diet choices.'''

    __tablename__ = 'diets'

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Diet diet_id=%s diet_type=%s description=%s \
        restrictive_ranking=%s>' % (self.diet_id,
                                    self.diet_type,
                                    self.description,
                                    self.restrictive_ranking)


class Cuisine(db.Model):
    '''Spoonacular cuisine types.'''

    __tablename__ = 'cuisine'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Cuisine cuisine_id=%s cuisine_name=%s>' % (self.cuisine_id,
                                                            self.cuisine_name)


class Course(db.Model):
    '''Spoonacular course types'''

    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Course course_id=%s course_name=%s>' % (self.course_id,
                                                         self.course_name)


class IngToAvoid(db.Model):
    '''Ingredients users would like to avoid.'''

    __tablename__ = 'avoid'

    avoid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<IngToAvoid avoid_id=%s profile_id=%s ingredient=%s \
        reason=%s>' % (self.avoid_id,
                       self.profile_id,
                       self.ingredient,
                       self.reason)


class PartyGuest(db.Model):
    '''Associate users with a party'''

    #  this is a true association table now

    __tablename__ = 'party_guests'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'),
                         nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'),
                           nullable=False)


class Party(db.Model):
    '''Create a dinner party to store and link information about a party'''

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    date_of_party = db.Column(db.Date, nullable=True)
    time_of_party = db.Column(db.Time(timezone=True), nullable=True)

    guest_profiles = db.relationship('Profile',
                                     secondary='party_guests',
                                     lazy='joined',
                                     backref='party',
                                     post_update=True)

    recipes = db.relationship('RecipeCard',
                              secondary='partyrecipes',
                              backref='parties',
                              lazy='joined',
                              post_update=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Party party_id=%s title_id=%s host_id=%s date=%s \
        time=%s>' % (self.party_id,
                     self.title,
                     self.host_id,
                     self.date,
                     self.time)


class RecipeCard(db.Model):
    '''Add a recipe to a users recipe box'''

    __tablename__ = 'recipecard'

    recipe_record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    recipe_image_url = db.Column(db.String(300), nullable=False)
    recipe_url = db.Column(db.String(300), nullable=False)
    ingredients = db.Column(db.String(2000), nullable=True)
    instructions = db.Column(db.String(2000), nullable=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<RecipeCard recipe_record_id=%s recipe_id=%s title=%s \
        recipe_image_url=%s recipe_url=%s ingredients=%s \
        instructions=%s>' % (self.recipe_record_id,
                             self.recipe_id,
                             self.title,
                             self.recipe_image_url,
                             self.recipe_url,
                             self.ingredients,
                             self.instructions)


class RecipeBox(db.Model):
    '''Recipes bookmarked by a user'''

    __tablename__ = 'recipebox'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)

    recipes = db.relationship('RecipeCard', lazy='joined', post_update=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<RecipeBox record_id=%s user_id=%s \
        recipe_record_id=%s>' % (self.record_id,
                                 self.user_id,
                                 self.recipe_record_id)


class PartyRecipes(db.Model):
    '''Associate a recipe with a party'''

    __tablename__ = 'partyrecipes'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'),
                         nullable=False)
    recipe_record_id = db.Column(db.Integer,
                                 db.ForeignKey('recipecard.recipe_record_id'),
                                 nullable=False)
    works_for = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<PartyRecipes record_id=%s party_id=%s \
        recipe_record_id=%s works_for=%s>' % (self.record_id,
                                              self.party_id,
                                              self.recipe_record_id,
                                              self.works_for)
