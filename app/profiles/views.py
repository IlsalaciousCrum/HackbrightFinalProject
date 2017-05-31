from flask import (render_template, redirect, url_for, flash, session,
                   request, jsonify, abort)

from . import profiles

from .. import db

from ..models import (User, Profile, Diet, Intolerance, Party, PartyGuest,
                      IngToAvoid, ProfileIntolerance, Friend)

from flask_login import login_required, current_user

from .forms import (FirstNameForm, LastNameForm, DietForm, DietReasonForm,
                    AddAvoidForm, UpdateAvoidForm, IntoleranceForm,
                    AddNewPartyForm, DeleteFriendForm, ChangeFriendEmailForm,
                    FriendNotesForm, FindaFriendForm, AddGuestToPartyForm)

from datetime import datetime

from ..decorators import email_confirmation_required

from ..email import send_email


@profiles.route('/dashboard', methods=['GET'])
@login_required
@email_confirmation_required
def show_dashboard():
    """Show logged in user's profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    profile = user.profile

    first_name_form = FirstNameForm(request.form)
    first_name_form.first_name.data = profile.first_name
    last_name_form = LastNameForm(request.form)
    last_name_form.last_name.data = profile.last_name
    diet_form = DietForm(request.form)
    diet_form.diet.data = profile.diet_id
    diet_reason_form = DietReasonForm(request.form)
    diet_reason_form.diet_reason.data = profile.diet_reason
    add_avoid_form = AddAvoidForm(request.form)
    update_avoid_form = UpdateAvoidForm(request.form)
    intol_form = IntoleranceForm(request.form)
    profile_intolerances = db.session.query(ProfileIntolerance
                                            ).filter(Intolerance.intol_id ==
                                                     ProfileIntolerance.intol_id,
                                                     ProfileIntolerance.profile_id ==
                                                     profile.profile_id).all()
    intol_form.intolerances.data = [(intol.intol_id)
                                    for intol in profile_intolerances]
    past_parties = db.session.query(Party).filter(Party.user_id ==
                                                  current_user.id,
                                                  Party.datetime_of_party
                                                  < datetime.utcnow()).all()
    upcoming_parties = db.session.query(Party).filter(Party.user_id ==
                                                      current_user.id,
                                                      Party.datetime_of_party >=
                                                      datetime.utcnow()).all()
    return render_template("/profiles/dashboard.html",
                           profile=profile,
                           intol_form=intol_form,
                           first_name_form=first_name_form,
                           last_name_form=last_name_form,
                           diet_form=diet_form,
                           diet_reason_form=diet_reason_form,
                           add_avoid_form=add_avoid_form,
                           update_avoid_form=update_avoid_form,
                           past_parties=past_parties,
                           upcoming_parties=upcoming_parties)


@profiles.route('/friendprofile/<int:friend_id>', methods=['GET'])
@login_required
@email_confirmation_required
def show_friend_profile(friend_id):
    """Show logged in user's friends profile"""

    is_friend = Friend.query.filter(Friend.user_id ==
                                    current_user.id,
                                    Friend.friend_profile_id ==
                                    friend_id).first()
    if is_friend:
        friend_profile = Profile.query.get(friend_id)
        past_parties = db.session.query(Party
                                        ).filter(Party.user_id ==
                                                 current_user.id,
                                                 PartyGuest.friend_profile_id ==
                                                 friend_profile.profile_id,
                                                 Party.datetime_of_party <
                                                 datetime.utcnow()).all()
        upcoming_parties = db.session.query(Party
                                            ).filter(Party.user_id ==
                                                     current_user.id,
                                                     PartyGuest.friend_profile_id ==
                                                     friend_profile.profile_id,
                                                     Party.datetime_of_party >=
                                                     datetime.utcnow()).all()
        party_form = AddGuestToPartyForm(request.form)
        party_form.parties.choices = db.session.query(Party
                                                      ).filter(Party.user_id ==
                                                               current_user.id,
                                                               PartyGuest.friend_profile_id !=
                                                               friend_profile.profile_id,
                                                               Party.datetime_of_party >=
                                                               datetime.utcnow()).all()
        delete_form = DeleteFriendForm(request.form)
        email_form = ChangeFriendEmailForm(request.form)
        notes_form = FriendNotesForm(request.form)
        notes_form.notes.data = is_friend.profile_notes

        if friend_profile.owned_by_user_id == current_user.id:
            first_name_form = FirstNameForm(request.form)
            first_name_form.first_name.data = friend_profile.first_name
            last_name_form = LastNameForm(request.form)
            last_name_form.last_name.data = friend_profile.last_name
            diet_form = DietForm(request.form)
            diet_reason_form = DietReasonForm(request.form)
            diet_reason_form.diet_reason.data = friend_profile.diet_reason
            add_avoid_form = AddAvoidForm(request.form)
            update_avoid_form = UpdateAvoidForm(request.form)
            intol_form = IntoleranceForm(request.form)
            profile_intolerances = db.session.query(ProfileIntolerance
                                                    ).filter(Intolerance.intol_id ==
                                                             ProfileIntolerance.intol_id,
                                                             ProfileIntolerance.profile_id ==
                                                             friend_profile.profile_id).all()
            intol_form.intolerances.data = [(intol.intol_id) for intol in profile_intolerances]
            return render_template("/profiles/friend_profile_editable.html",
                                   profile_id=current_user.profile.profile_id,
                                   friend_profile=friend_profile,
                                   past_parties=past_parties,
                                   upcoming_parties=upcoming_parties,
                                   invite_form=party_form,
                                   profile=current_user.profile,
                                   delete_form=delete_form,
                                   intol_form=intol_form,
                                   first_name_form=first_name_form,
                                   last_name_form=last_name_form,
                                   diet_form=diet_form,
                                   diet_reason_form=diet_reason_form,
                                   add_avoid_form=add_avoid_form,
                                   update_avoid_form=update_avoid_form,
                                   email_form=email_form,
                                   friend_profile_notes=is_friend.profile_notes,
                                   notes_form=notes_form)
        elif is_friend and is_friend.friendship_verified_by_email:
            return render_template("/profiles/friend_profile_fixed.html",
                                   profile_id=current_user.profile.profile_id,
                                   friend_profile=friend_profile,
                                   past_parties=past_parties,
                                   upcoming_parties=upcoming_parties,
                                   invite_form=party_form,
                                   profile=current_user.profile,
                                   delete_form=delete_form,
                                   notes_form=notes_form,
                                   friend_profile_notes=is_friend.profile_notes,)
    else:
        flash("Looks like you are trying to view the profile of someone you are not\
              friends with. Do you want to create your own profile for a friend?", "danger")
        return redirect(request.referrer)


# @profiles.route('/add_a_new_party_form', methods=['GET', 'POST'])
# @login_required
# @email_confirmation_required
# def add_a_new_party():
#     """Loads modal content for creating a new party"""


@profiles.route('/connect_friends', methods=['GET', 'POST'])
@login_required
@email_confirmation_required
def connect_friends():
    """Loads modal content for connecting a new friend and processes the request"""

    find_friend_form = FindaFriendForm(request.form)
    if request.method == 'POST' and find_friend_form.validate():
        existing_user = db.session.query(Profile
                                         ).join(User
                                                ).filter(Profile.email ==
                                                         find_friend_form.friend_email.data,
                                                         Profile.profile_id ==
                                                         User.profile_id).first()
        if existing_user:
            already_connected_friends = Friend.query.filter(Friend.user_id ==
                                                            current_user.id,
                                                            Friend.friend_profile_id ==
                                                            existing_user.profile_id).first()
            if already_connected_friends:
                flash("Looks like you are already connected to %s, you can find\
                      their profile information from the navigation bar above or\
                      on your dashboard." % find_friend_form.friend_email.data,
                      "warning")
                return redirect(request.referrer)
            if existing_user:
                friendship = Friend.create_record(user_id=current_user.id,
                                                  friend_profile_id=existing_user.profile_id)
                token = friendship.generate_email_token()
                send_email(to=existing_user.email,
                           subject=' {0} {1}({2}) wants to connect\
                           on KindTable'.format(current_user.profile.first_name,
                                                current_user.profile.last_name,
                                                current_user.profile.email),
                           template='profiles/email/friend_existing_user',
                           profile=existing_user,
                           friend=current_user.profile,
                           token=token)
                friendship.update({"friend_request_sent": True})
                flash('An connection request email has been sent to %s.'
                      % existing_user.email, "success")
                return redirect(request.referrer)
            if already_connected_friends.friend_request_sent is True:
                flash("Looks like you have already sent this person a friend\
                      request. Maybe check with them personally or create a friend\
                      profile for them yourself?", "danger")
                return redirect(request.referrer)
        else:
            new_friend_profile = Profile.create_record(email=find_friend_form.friend_email.data)
            friendship = Friend.create_record(user_id=current_user.id,
                                              friend_profile_id=new_friend_profile.profile_id)
            token = friendship.generate_email_token()
            send_email(to=new_friend_profile.email,
                       subject=' %s %s wants to connect on KindTable',
                       template='profiles/email/friend_new_user',
                       friend=current_user.profile, token=token)
            flash('An connection request email has been sent to %s.'
                  % new_friend_profile.email, "success")
            return redirect(request.referrer)
    return render_template("profiles/find_a_friend.html",
                           find_friend_form=find_friend_form)


@profiles.route('/non_reg_confirm_friendship/<token>', methods=['GET'])
@login_required
@email_confirmation_required
def confirm_friendship_with_existing_user(token):
    """Validates an email token and confirms friendship between
    two existing users"""

    friend_dict = Friend.process_email_token(token)
    print friend_dict
    if not friend_dict:
        abort(404)
    else:
        new_friend = User.query.get(friend_dict['user_id'])
        Friend.create_record(user_id=current_user.id,
                             friend_profile_id=new_friend.profile_id,
                             friendship_verified_by_email=True)
        flash("Congratulations! You are now friends!", "success")
        return redirect('profiles/friendprofile/%s' % new_friend.profile_id)


@profiles.route('/reg_confirm_friendship/<token>', methods=['GET'])
@login_required
@email_confirmation_required
def confirm_friendship_with_new_user(token):
    """Validates an email token and confirms friendship between
    two existing users"""

    friendship = Friend.process_email_token(token)
    if not friendship:
        abort(404)
    else:
        new_friend = friendship.user.profile
        flash("Congratulations! You are now friends!", "success")
        return redirect('profiles/friendprofile/%s' % new_friend.profile_id)


@profiles.route('/party_profile/<int:party_id>')
@login_required
@email_confirmation_required
def show_party_profile(party_id):
    """Show the party profile"""

    session_token = session.get("session_token")
    user = User.query.filter_by(session_token=session_token).first()
    this_user = user.profile
    friends = user.friends
    parties = user.parties
    session['party_id'] = party_id
    diets = Diet.query.order_by(Diet.diet_type).all()
    party = Party.query.get(party_id)
    intol_list = Intolerance.query.order_by(Intolerance.intol_name).all()

    return render_template("profiles/party_profile.html", party=party,
                           this_user=this_user,
                           diets=diets,
                           intol_list=intol_list,
                           friends=friends,
                           parties=parties)


# Only JSON routes below for AJAX calls

@profiles.route('/changefirstname.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefirstname():
    """Takes an Ajax request and changes a profiles first name"""

    form = FirstNameForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"first_name": form.first_name.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'First name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changelastname.json', methods=['POST'])
@login_required
@email_confirmation_required
def changelastname():
    """Takes an Ajax request and changes a profiles last name"""

    form = LastNameForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.profile_id.data)
        profile.update({"last_name": form.last_name.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Last name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changediet.json', methods=['POST'])
@login_required
@email_confirmation_required
def changediet():
    """Takes an Ajax request and changes diet"""

    form = DietForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile.update({"diet_id": form.diet.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changedietreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def changedietreason():
    """Takes an Ajax request and changes diet reason"""

    form = DietReasonForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile.update({"diet_reason": form.diet_reason.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet reason updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/cleardietreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def cleardietreason():
    """Takes an Ajax request and clear's the diet reason"""

    form = DietReasonForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile.update({"diet_reason": None, "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Diet reason updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/intol.json', methods=['POST'])
@login_required
@email_confirmation_required
def intol():
    """Takes an Ajax request and updates intolerances"""

    form = IntoleranceForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        query = db.session.query(ProfileIntolerance
                                 ).filter(ProfileIntolerance.profile_id ==
                                          profile.profile_id).all()
        profile_intolerances = [(intol.intol_id) for intol in query]
        for intolerance in form.intolerances.data:
            if intolerance in profile_intolerances:
                pass
            elif intolerance not in profile_intolerances:
                ProfileIntolerance.create_record(profile_id=profile.profile_id,
                                                 intol_id=intolerance)
                profile.update({"last_updated": datetime.utcnow()})
        for profile_intolerance in profile_intolerances:
            if profile_intolerance not in form.intolerances.data:
                intol = db.session.query(ProfileIntolerance
                                         ).filter(ProfileIntolerance.intol_id ==
                                                  profile_intolerance,
                                                  ProfileIntolerance.profile_id ==
                                                  profile.profile_id).one()
                intol.remove_intolerance()
                profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Intolerances updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/addavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def addavoid():
    """Takes an Ajax request and adds an ingredient to avoid"""
    print 1
    form = AddAvoidForm(request.form)
    print 2
    profile = Profile.query.get(form.profile_id.data)
    print 3
    if form.validate() and profile.owned_by_user_id == current_user.id:
        print 4
        already_added = db.session.query(IngToAvoid
                                         ).filter(IngToAvoid.ingredient ==
                                                  form.add_avoid_ingredient.data).all()
        print 5
        if already_added:
            print 6
            flash("We already know about that ingredient to avoid.\
                  Would you like to add a different one?", "warning")
            print 7
            return redirect(request.referrer)
        else:
            print 8
            IngToAvoid.create_record(ingredient=form.add_avoid_ingredient.data,
                                     reason=form.add_avoid_reason.data,
                                     profile_id=profile.profile_id)
            print 9
            profile.update({"last_updated": datetime.utcnow()})
            print 10
            return jsonify(data={'message': 'Avoid added'})
    else:
        print 11
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/getavoid.json', methods=['GET'])
@login_required
@email_confirmation_required
def getavoid():
    """Takes an Ajax request and returns avoidance information"""

    avoid_id = request.args.get("id")
    avoidance = IngToAvoid.query.get(avoid_id)
    return jsonify(data={'ingredient': avoidance.ingredient,
                         'reason': avoidance.reason})


@profiles.route('/updateavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def updateavoid():
    """Takes an Ajax request and updates an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        if form.update_avoid_ingredient:
            avoid.update({'ingredient': form.update_avoid_ingredient.data})
        if form.update_avoid_reason:
            avoid.update({'reason': form.update_avoid_reason.data})
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/deleteavoidreason.json', methods=['POST'])
@login_required
@email_confirmation_required
def deleteavoidreason():
    """Takes an Ajax request and removes an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        avoid.update({'reason': None})
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/deleteavoid.json', methods=['POST'])
@login_required
@email_confirmation_required
def deleteavoid():
    """Takes an Ajax request and removes an existing ingredient to avoid"""

    form = UpdateAvoidForm(request.form)
    profile = Profile.query.get(form.profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        avoid = IngToAvoid.query.get(form.avoid_id.data)
        avoid.remove_avoidance()
        profile.update({"last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Ingredients to avoid updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/addtoparty.json', methods=['POST'])
@login_required
@email_confirmation_required
def add_to_party():
    """Takes an Ajax request and adds a guest to parties"""

    form = AddToPartiesForm(request.form)
    if form.validate():
        pass
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/delete_friend.json', methods=['POST'])
@login_required
@email_confirmation_required
def delete_friend():
    """Takes an Ajax request and deletes a friend"""

    form = DeleteFriendForm(request.form)
    if form.validate():
        friend_profile = Profile.query.get(form.friend_profile_id.data)
        friendship = db.session.query(Friend).filter(Friend.user_id ==
                                                     current_user.id,
                                                     Friend.friend_profile_id ==
                                                     form.friend_profile_id.data).all()
        if friend_profile.owned_by_user_id == current_user.id:
            friendship.remove_friendship()
            friend_profile.remove_profile()
        else:
            friendship.remove_friendship()
        flash("Friend removed from your account.")
        return redirect(url_for('profiles.show_dashboard'))
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changefriendemail.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefriendemail():
    """Takes an Ajax request and changes a friend's email address"""

    form = ChangeFriendEmailForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    if form.validate() and profile.owned_by_user_id == current_user.id:
        profile = Profile.query.get(form.friend_profile_id.data)
        profile.update({"email": form.email.data,
                        "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'First name updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/changefriendnotes.json', methods=['POST'])
@login_required
@email_confirmation_required
def changefriendnotes():
    """Takes an Ajax request and changes the note on the Friend table"""

    form = FriendNotesForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    friendship = Friend.query.filter(Friend.friend_profile_id ==
                                     profile.profile_id, Friend.user_id ==
                                     current_user.id).one()
    if form.validate():
        friendship.update({"profile_notes": form.notes.data,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/clearfriendnote.json', methods=['POST'])
@login_required
@email_confirmation_required
def clearfriendnotes():
    """Takes an Ajax request and clears the note on the Friend table"""

    form = FriendNotesForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    friendship = Friend.query.filter(Friend.friend_profile_id ==
                                     profile.profile_id, Friend.user_id ==
                                     current_user.id).one()
    if form.validate():
        friendship.update({"profile_notes": None,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/findafriend.json', methods=['POST'])
@login_required
@email_confirmation_required
def findafriend():
    """Takes an Ajax request and sends friend requests"""

    form = FindaFriendForm(request.form)
    friendship = db.session.query(Friend).join(Profile
                                               ).filter(Profile.email ==
                                                        form.email.data,
                                                        Friend.user_id ==
                                                        current_user.id).first()
    if form.validate():
        friendship.update({"profile_notes": None,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)


@profiles.route('/add_new_party.json', methods=['POST'])
@login_required
@email_confirmation_required
def add_new_party():
    """Takes an Ajax request and adds a new party"""

    form = FriendNotesForm(request.form)
    profile = Profile.query.get(form.friend_profile_id.data)
    friendship = Friend.query.filter(Friend.friend_profile_id ==
                                     profile.profile_id, Friend.user_id ==
                                     current_user.id).one()
    if form.validate():
        friendship.update({"profile_notes": None,
                           "last_updated": datetime.utcnow()})
        return jsonify(data={'message': 'Notes updated'})
    else:
        for field, error in form.errors.items():
            flash(u"Error in %s -  %s" % (
                  getattr(form, field).label.text,
                  error[0]), 'danger')
        return redirect(request.referrer)
