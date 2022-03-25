from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.get_seller_by_email(email)  
        user2 = db.get_buyer_by_email(email)  

        if user:
            if user.password == password:
                flash('Logged in successfully as seller!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password for seller, try again.', category='error')

        elif user2:
            if user2.password == password:

                flash('Logged in successfully as buyer!', category='success')
                login_user(user2, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password for buyer, try again.', category='error')
        else:    
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        last_name =  request.form.get('lastName')
        phone = request.form.get('phone')
        username = request.form.get('username')
        user_type = int(request.form.get('userType'))

        #CHECK IF USERNAME AND EMAIL ARE UNIQUE
        
        seller_mail = db.get_seller_by_email(email)  
        seller_username = db.get_seller_by_username(username)  
        buyer_mail = db.get_seller_by_email(email)  
        buyer_username = db.get_seller_by_username(username)  


        if seller_mail or buyer_mail:
            flash('E-mail already registered.', category='error')
        elif seller_username or buyer_username:
            flash("Username already exists", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(phone) < 10:
            flash('Phone number not valid.', category='error')
        elif user_type == 0:
            flash('Select a user type', category='error')

       #ADD TO DATABASE     
        else:
            if user_type == 2:
                db.add_seller(username, password1, first_name, last_name, phone, email, 1)
                flash('Seller account created!', category='success')

            elif user_type == 1:
                print(password1)
                db.add_buyer(username, password1, first_name, last_name, phone, email)
                flash('Buyer account created!', category='success')

            return redirect(url_for('auth.home'), user=current_user)

    return render_template("sign-up.html", user=current_user)
