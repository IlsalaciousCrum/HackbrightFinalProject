"""Utility file to seed K(i)nd database data for testing"""

from sqlalchemy import func

from Model import connect_to_db, db, User, UserIntolerance, Intolerance, Diet, IngToAvoid, Party, PartyGuest
from server import app


def load_testdata():
    """Load users from u.users into database."""

    diet1 = Diet(diet_type="pescatarian", description="does not eat meat but does eat fish.")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="lacto vegetarian", description="vegetarian who abstains from eating meat and eggs, but who eats dairy products")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="ovo vegetarian", description="vegetarianism which allows for the consumption of eggs but not dairy products")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="vegan", description="does not eat an animal byproducts")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="vegetarian", description="does not eat meat")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="any", description="does not follow any limiting diet")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="primal", description="it's complex, but basically no gluten, corn, sugar or processed foods")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="paleo", description="it's complex, but basically dairy, no gluten, corn, sugar or processed foods")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="ketogenic", description="high-fat, adequate-protein, low-carbohydrate diet")
    db.session.add(diet1)
    db.session.commit()
    diet1 = Diet(diet_type="whole 30", description="It's complex. No processed foods and few ingredients")
    db.session.add(diet1)
    db.session.commit()

    print "loaded diets"

    intol1 = Intolerance(intol_name="dairy", intol_description="Intolerance or allergy to the milk of a cow")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="egg", intol_description="Intolerance or allergy to eggs")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="gluten", intol_description="Intolerance or allergy to gluten")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="peanut", intol_description="Intolerance or allergy to peanuts and peanut products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="sesame", intol_description="Intolerance or allergy to sesame seeds and sesame products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="seafood", intol_description="Intolerance or allergy to seafood")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="shellfish", intol_description="Intolerance or allergy to shellfish")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="soy", intol_description="Intolerance or allergy to soy products")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="sulfites", intol_description="Intolerance or allergy to sulfites")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="tree nut", intol_description="Intolerance or allergy to tree nuts")
    db.session.add(intol1)
    db.session.commit()
    intol1 = Intolerance(intol_name="wheat", intol_description="Intolerance or allergy to wheat")
    db.session.add(intol1)
    db.session.commit()

    print "loaded intolerances"

    user1 = User(username="Ilsabean", password="Nope", first_name="Ilsa", last_name="Gordon", email="ilsalacious@gmail.com", phone="(650)504-1552", preferred_com="phone", diet_id="6", diet_reason="health")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="Tage", password="nada", first_name="Todd", last_name="Gage", email="todd@bitcollider.net", preferred_com="email", diet_id="6")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="awesomesauce", password="squirrel", first_name="Rachel", last_name="Hackbright", email="rachel@rachel.com", preferred_com="email", diet_id="6", diet_reason="ethical")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="gifmaster", password="nothankyou", first_name="Henry", last_name="Chan", email="henry@henry.com", preferred_com="email", diet_id="6", diet_reason="ethical")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="bestroomie", password="why", first_name="Rene", last_name="Hendrix", email="rene@rene.com", preferred_com="email", diet_id="6")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="roomiespecialist", password="right", first_name="Greg", last_name="Sutter", email="greg@greg.com", preferred_com="email", diet_id="4")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="balloonicorn", password="sure", first_name="Balloon", last_name="Icorn", email="b@hackbright.com", phone="(555)555-5555", preferred_com="text", diet_id="4", diet_reason="weight loss")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="Burglar", password="stealing", first_name="Ham|Burglar", last_name="ham@burglar.com", email="ham@burgled.com", preferred_com="email", diet_id="1")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="ChickenBoo", password="God", first_name="Chicken", last_name="Boo", email="chicken@boo.com", phone="(333)333-3333", preferred_com="text", diet_id="1", diet_reason="ethical")
    db.session.add(user1)
    db.session.commit()
    user1 = User(username="MightyGirl", password="doubtful", first_name="Pat", last_name="Gordon", email="pat@gordon.com", preferred_com="email", diet_id="6")
    db.session.add(user1)
    db.session.commit()

    print "loaded users"

    avoid1 = IngToAvoid(ingredient="red bell pepper", reason="food allergy", user_id="1")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="corn", reason="allergy", user_id="2")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="garlic", reason="intolerant", user_id="3")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="chocolate", reason="dislikes", user_id="4")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="raisin", reason="dislikes but can pick out", user_id="5")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="rutabega", reason="dislikes", user_id="6")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="veal", reason="ethical reasons", user_id="7")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="pork", reason="religious reasons", user_id="8")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="beef", reason="intolerant", user_id="9")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="pork", reason="intolerant", user_id="9")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="buffalo", reason="intolerant", user_id="9")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="bison", reason="intolerant", user_id="9")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="chicken", reason="ethical reasons", user_id="1")
    db.session.add(avoid1)
    db.session.commit()
    avoid1 = IngToAvoid(ingredient="brussel sprouts", reason="dislike", user_id="10")
    db.session.add(avoid1)
    db.session.commit()

    print "loaded ingredients to avoid"

    userintol1 = UserIntolerance(user_id=1, intol_id=1)
    userintol1 = UserIntolerance(user_id=2, intol_id=2)
    db.session.add(userintol1)
    db.session.commit()
    userintol1 = UserIntolerance(user_id=3, intol_id=3)
    db.session.add(userintol1)
    db.session.commit()
    userintol1 = UserIntolerance(user_id=4, intol_id=4)
    db.session.add(userintol1)
    db.session.commit()
    userintol1 = UserIntolerance(user_id=5, intol_id=5)
    db.session.add(userintol1)
    db.session.commit()
    userintol1 = UserIntolerance(user_id=2, intol_id=3)
    db.session.add(userintol1)
    db.session.commit()
    userintol1 = UserIntolerance(user_id=2, intol_id=2)
    db.session.add(userintol1)
    db.session.commit()
    userintol1 = UserIntolerance(user_id=3, intol_id=1)
    db.session.add(userintol1)
    db.session.commit()

    print "loaded user's intolerances"

    party1 = Party(title="Ballonicorn's Birthday", host_id=1)
    db.session.add(party1)
    db.session.commit()
    party1 = Party(title="Graduation", host_id=2)
    db.session.add(party1)
    db.session.commit()
    party1 = Party(title="Thursday", host_id=4)
    db.session.add(party1)
    db.session.commit()
    party1 = Party(title="Artichoke sale", host_id=5)
    db.session.add(party1)
    db.session.commit()
    party1 = Party(title="Everyone", host_id=10)
    db.session.add(party1)
    db.session.commit()

    print "loaded parties"

    PartyGuest1 = PartyGuest(party_id=1, user_id=3)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=1, user_id=4)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=1, user_id=5)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=1, user_id=6)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=2, user_id=5)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=2, user_id=6)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=2, user_id=7)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=3, user_id=9)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=3, user_id=8)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=3, user_id=7)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=4, user_id=1)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=4, user_id=2)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=5, user_id=3)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=5, user_id=4)
    db.session.add(PartyGuest1)
    db.session.commit()
    PartyGuest1 = PartyGuest(party_id=5, user_id=6)
    db.session.add(PartyGuest1)
    db.session.commit()

    print "loaded PartyGuests"


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_testdata()
