'''Models for K(i)ndTable WebApp.'''
from flask_sqlalchemy import SQLAlchemy
# from seed import load_testdata

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    '''User of K(i)nd website. Guests and hosts are stored in the same table.'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=True)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    diet_reason = db.Column(db.String(120), nullable=True)  # ie, ethical, religious, general health, specific health

    avoidances = db.relationship('IngToAvoid', backref=db.backref('users_a'))

    intolerances = db.relationship('Intolerance',
                                   secondary='userintolerances',
                                   backref='users')

    diet = db.relationship('Diet', backref='users')

    parties = db.relationship('Party')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<User user_id=%s email=%s  first_name=%s last_name=%s>' % (self.user_id, self.email, self.first_name, self.last_name)


class Friends(db.Model):
    '''Makes connections between the user and other users they know'''

    __tablename__ = 'friends'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    users = db.relationship('User', foreign_keys=[user_id], backref='friends')
    friends = db.relationship('User', foreign_keys=[friend_id], backref='users')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Friends record_id=%s user_id=%s  friend_id=%s>' % (self.record_id, self.user_id, self.friend_id)


class UserIntolerance(db.Model):
    '''The intolerances that each user has.'''

    __tablename__ = 'userintolerances'

    user_intol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    intol_id = db.Column(db.Integer, db.ForeignKey('intolerances.intol_id'), nullable=False)


class Intolerance(db.Model):
    '''Spoonacular's list of possible intolerances.'''

    __tablename__ = 'intolerances'

    intol_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intol_name = db.Column(db.String(64), nullable=False)
    intol_description = db.Column(db.String(120), nullable=False)  # Spoonacular's criteria for searching

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Intolerances int_id=%s int_name=%s int_description=%s>' % (self.intol_id, self.intol_name, self.intol_description)


class Diet(db.Model):
    '''What diet a user follows.'''

    __tablename__ = 'diets'

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Diet diet_id=%s diet_type=%s description=%s>' % (self.diet_id, self.diet_type, self.description)


class Cuisine(db.Model):
    '''Spoonacular cuisine types.'''

    __tablename__ = 'cuisine'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Cuisine cuisine_id=%s cuisine_name=%s>' % (self.cuisine_id, self.cuisine_name)


class Course(db.Model):
    '''Spoonacular course types'''

    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Course course_id=%s course_name=%s>' % (self.course_id, self.course_name)


class IngToAvoid(db.Model):
    '''Ingredients users would like to avoid.'''

    __tablename__ = 'avoid'

    avoid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    users = db.relationship('User', backref='ingredients')

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<IngToAvoid avoid_id=%s user_id=%s ingredient=%s reason=%s>' % (self.avoid_id, self.user_id, self.ingredient, self.reason)


class PartyGuest(db.Model):
    '''Associate users with a party'''

    #  this is a true association table now

    __tablename__ = 'party_guests'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)


class Party(db.Model):
    '''Create a dinner party to store and link information about a party'''

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    users = db.relationship('User',
                            secondary='party_guests')

    recipes = db.relationship('RecipeBox', backref=db.backref('party'))

    def __repr__(self):
        '''Provide helpful representation when printed.'''

        return '<Party party_id=%s title_id=%s host_id=%s>' % (self.party_id, self.title, self.host_id)


class RecipeBox(db.Model):
    '''Add a recipe to a recipe box for a given party'''

    __tablename__ = 'recipes'

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    recipe_id = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    recipe_image_url = db.Column(db.String(300), nullable=False)
    recipe_url = db.Column(db.String(300), nullable=False)
    works_for = db.Column(db.String(1000), nullable=True)
    ingredients = db.Column(db.String(2000), nullable=True)
    instructions = db.Column(db.String(2000), nullable=True)


##############################################################################
# Helper functions

def connect_to_db(app):
    '''Connect the database to our Flask app.'''

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///kind'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

##############################################################################
# For testing:

    #  TODO: DOh! These should all be class methods. Move them up under each Class

    def example_data():
        '''Create some sample data.'''

        goldilocks = User(email='goldilocks@gmail.com',
                          diet_id=7,
                          first_name='Goldy',
                          last_name='Locks',
                          diet_reason='It\'s what works for me',
                          verified='True',
                          password='FakeyFakey')
        goldilocks_avoid = IngToAvoid(user_id=1,
                                      ingredient='cinnamon',
                                      reason='too spicy')
        goldilocks_intol = UserIntolerance(user_id=1,
                                           intol_id=11)

        mama_bear = User(email='mama@bears.com',
                         diet_id=4,
                         first_name='Mama',
                         last_name='Bears',
                         diet_reason='Weight loss',
                         verified='False',
                         password='Ihatekids')
        mama_bear_avoid = IngToAvoid(user_id=2,
                                     ingredient='rutabegas',
                                     reason='gas')
        mama_bear_friendship = Friends(user_id=1,
                                       friend_id=2)

        papa_bear = User(email='papa@bear.com',
                         diet_id=10,
                         first_name='Papa',
                         last_name='Bear',
                         diet_reason='I\'m a bear',
                         verified='False',
                         password='Rawr')
        papa_bear_friendship = Friends(user_id=1,
                                       friend_id=3)

        baby_bear = User(email='baby@bear.com',
                         diet_id=8,
                         first_name='Baby',
                         last_name='Bear',
                         diet_reason='Growing bear',
                         verified='False',
                         password='FakeyFakey')
        baby_bear_avoid = IngToAvoid(user_id=4,
                                     ingredient='jalapenos',
                                     reason='too spicy')
        baby_bear_intol = UserIntolerance(user_id=4,
                                          intol_id=4)
        baby_bear_friendship = Friends(user_id=1,
                                       friend_id=4)

        teddy_bear_picnic = Party(title='Teddy Bear\'s Picnic',
                                  host_id=1, )

        picnic_guest1 = PartyGuest(party_id=1,
                                   user_id=2)
        picnic_guest2 = PartyGuest(party_id=1,
                                   user_id=3)
        picnic_guest3 = PartyGuest(party_id=1,
                                   user_id=4)

        test_recipe = RecipeBox(party_id=1,
                                recipe_id=472678,
                                title='Paleo honey cake',
                                recipe_image_url='https://webknox.com/recipeImages/472678-556x370.jpg',
                                recipe_url='https://spoonacular.com/recipes/paleo-honey-cake-472678',
                                works_for='{"Diets": ["any", "paleo" "primal"], "Ingredients to omit": ["jalapenos", "rutabegas"], "Intolerances/Allergies": ["wheat", "peanuts"]}',
                                ingredients='2 1/2 cup blanched almond flour, 1/2 teaspoon celtic sea salt, 4 eggs, 1 tablespoon ground cinnamon, 1/4 teaspoon ground cloves, 1/2 cup honey, 1/2 cup palm oil, 1/2 cup raisins',
                                instructions=('Add all the ingredients to a large blender or food processor and puree until smooth.',
                                              'Scrape down the sides of the bowl when necessary. Give it a taste and add more stevia or salt to taste. Be sure to puree the mixture as much as possible, you don\'t lose anything by overblending but you sacrifice texture and flavor by underblending!',
                                              'Pour into serving bowls and serve immediately.', 'If not serving right away, cover with plastic wrap and refrigerate',
                                              'Top the mousse with chopped, salted peanuts and some mini dark chocolate chips if you\'re feeling extra indulgent!'))

        db.session.add_all([goldilocks,
                            goldilocks_avoid,
                            goldilocks_intol,
                            mama_bear,
                            mama_bear_avoid,
                            mama_bear_friendship,
                            papa_bear,
                            papa_bear_friendship,
                            baby_bear,
                            baby_bear_avoid,
                            baby_bear_intol,
                            baby_bear_friendship,
                            teddy_bear_picnic,
                            picnic_guest1,
                            picnic_guest2,
                            picnic_guest3,
                            test_recipe])
        db.session.commit()

##############################################################################

if __name__ == '__main__':
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print 'Connected to DB.'
