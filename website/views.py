from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json, os, psycopg2
from . import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length


views = Blueprint('views', __name__)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

class UpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[InputRequired(), Length(min=7, max=64)], id='password1')
    show_password1 = BooleanField('Show password', id='check1')
    newpassword = PasswordField('New Password', validators=[InputRequired(), Length(min=7, max=64)], id='password2')
    show_password2 = BooleanField('Show password', id='check2')
    confirm = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=7, max=64)], id='password3')
    show_password3 = BooleanField('Show password', id='check3')

class UpdateInfo(FlaskForm):
    name = StringField('New name', validators=[Length(max=64)])
    surname = StringField('New surname', validators=[Length(max=64)])
    phone = StringField('New phone', validators=[Length(max=64)])

class ClassInfo(FlaskForm):
    name = StringField('New name', validators=[Length(max=64)])
    surname = StringField('New surname', validators=[Length(max=64)])
    phone = StringField('New phone', validators=[Length(max=64)])

@login_manager.user_loader
def load_user(the_user):
    if db.get_seller_by_username(the_user):
        return db.get_seller_by_username(the_user)
    else:
        return db.get_buyer(the_user)    

@app.route("/logout")
@login_required
def logout():
    if not current_user.is_authenticated:
        flash('You have not logged in. You cannot log out', 'error')
    else:
        logout_user()
        flash('You have successfully logged out.', 'success')
        return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    if db.get_seller_by_username(current_user.username):
        seller_info = db.get_sellerinfo(current_user.userid)
        seller_class = db.get_sellerclass(current_user.username)
        return render_template("profile.html", user=current_user, seller_info=seller_info, seller_class = seller_class)
    else:
        return render_template("profile.html", user=current_user, seller_info=None, seller_class = None)


@app.route('/')
def index():

    seller_count = db.get_seller_count()
    buyer_count = db.get_buyer_count()
    product_count = db.get_product_count()

    return render_template('home.html',user=current_user, seller=seller_count,
    buyer = buyer_count, product=product_count)

@app.route("/update-password", methods=['GET','POST'])
@login_required
def update_profile():
    
    if not current_user.is_authenticated:
        return redirect("/home")
    update = UpdateForm()

    if update.validate_on_submit():

        if str(update.newpassword.data) != str(update.confirm.data):
            flash(f"New passwords don't match. Try again.",'error')
            return redirect("/update-password")

        user = db.get_seller_by_username(current_user.username)
        user_buyer = db.get_buyer(current_user.username)

        if user is None:
            user = user_buyer

        if update.oldpassword.data == user.password:

            if user_buyer:
                db.update_buyer_password(update.newpassword.data, user.username)
            else:
                db.update_seller_password(update.newpassword.data, user.username)


            flash(f"Your password has changed successfully.",'success')
            logout_user()

            return redirect("/login")
        else:
            flash(f"The old password you entered is incorrect. Try again.",'error')
            return redirect("/update-password")
            
    return render_template("update-password.html", title = "Change Password", user=current_user, update = update)

@app.route("/update-info", methods=['GET','POST'])
@login_required
def update_info():
    
    if not current_user.is_authenticated:
        return redirect("/home")

    update = UpdateInfo()

    seller = db.get_seller_by_username(current_user.username)

    if update.validate_on_submit():

        if update.name.data == "":
            update.name.data = current_user.name
        if update.surname.data == "":
            update.surname.data = current_user.surname
        if update.phone.data == "":
            update.phone.data = current_user.phone


        print(update.name.data)
        print(update.surname.data)
        print(update.phone.data)

        if seller:
            db.update_seller(current_user.username, update.name.data, update.surname.data, update.phone.data)
        else:    
            db.update_buyer(current_user.username, update.name.data, update.surname.data, update.phone.data)
        
        flash(f"Updated",'success')
        return render_template("home.html", user=current_user)

            
    return render_template("update-info.html", user=current_user, update = update)


@views.route('/sellers', methods=['GET', 'POST'])
def sellers():

    sells= db.get_sellers_by_sold()
    rating = db.get_sellers_by_rating()

    return render_template("sellers.html", sells = sells, rating=rating, user=current_user)


@views.route('/buyers', methods=['GET', 'POST'])
def buyers():
    buyers = db.get_buyers()
    return render_template("buyers.html", buyers=buyers, user=current_user)


@views.route('/product', methods=['GET', 'POST'])
def product():

    brand = db.get_product_by_brand()
    category = db.get_product_by_category()
    year = db.get_product_by_year()
    
    return render_template("product.html", brand = brand, category = category, year = year, user=current_user)
