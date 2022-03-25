from re import search
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json, os, psycopg2
from . import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET', 'POST'])
#@login_required
def admin_page(): 
 
    classes = db.get_sellerclasses()

    return render_template("admin.html", user=current_user, classes=classes)


@admin.route('/admin-class', methods=['GET', 'POST'])
#@login_required
def add_class():  

    if request.method == 'POST':
        title = request.form.get('title')
        id = request.form.get('id')
        minsell = request.form.get('minsell')
        minrate = request.form.get('minrate')
        percent = request.form.get('percent')
        cargo =  request.form.get('cargo')

        seller_class = db.get_sellerclass_by_title(title)

        if seller_class:
            flash('Title already exists', category='error')

        else:
            db.add_sellerclass(id, title, minsell, minrate, cargo, percent)
            flash('Added successfully', category='success')

    return render_template("add-class.html", user=current_user)

@admin.route('/change-class', methods=['GET', 'POST'])
#@login_required
def change_class():  

    if request.method == 'POST':

        search_title = request.form.get('titleold')
        current = db.get_sellerclass_by_title(search_title)

        if current is None:
            flash('Class does not exist','error')
            return render_template("change-class.html", user=current_user)

        else:    
                title = request.form.get('title')
                id = request.form.get('id')
                minsell = request.form.get('minsell')
                minrate = request.form.get('minrate')
                percent = request.form.get('percent')
                cargo =  request.form.get('cargo')

                if title == "":
                    title = current.title
                if id == "":
                    id = current.classid
                if minsell == "":
                    minsell = current.minsell
                if minrate == "":
                    minrate = current.minrate
                if percent == "":
                    percent = current.percent
                if cargo == "":
                    cargo = current.cargo

                db.update_sellerclass(id, search_title, title, minsell, minrate, cargo, percent)
                flash('Changed successfully', category='success')

    return render_template("change-class.html", user=current_user)

@admin.route('/delete-class', methods=['GET', 'POST'])
#@login_required
def delete_class():  

    if request.method == 'POST':

        search_title = request.form.get('title')
        current = db.get_sellerclass_by_title(search_title)

        if current is None:
            flash('Class does not exist','error')
            return render_template("delete-class.html", user=current_user)

        else:    
                db.delete_sellerclass(search_title)
                flash('Deleted successfully', category='success')

    return render_template("delete-class.html", user=current_user)

@admin.route('/delete-user', methods=['GET', 'POST'])
#@login_required
def delete_user():  

    if request.method == 'POST':

        username = request.form.get('username')
        seller = db.get_seller_by_username(username)
        buyer = db.get_buyer(username)

        print(username)

        if seller:
            db.delete_seller(username)
            seller = db.get_seller_by_username(username)

            if seller is None:
                flash('Seller deleted','success')
            else:
                flash('Seller could not be deleted','error')

            return render_template("delete-class.html", user=current_user)

        if buyer:    

            db.delete_buyer(username)
            buyer = db.get_buyer(username)

            if buyer is None:
                flash('Buyer deleted','success')
            else:
                flash('Buyer could not be deleted','error')

            return render_template("delete-class.html", user=current_user)

        else:
            flash('No user found','error')

    return render_template("delete-user.html", user=current_user)


@admin.route('/change-sellerinfo', methods=['GET', 'POST'])
#@login_required
def change_sellerinfo():  

    if request.method == 'POST':

        search_username = request.form.get('username')
        current = db.get_seller_by_username(search_username)

        if current is None:
            flash('Seller does not exist','error')
            return render_template("change-sellerinfo.html", user=current_user)

        else:    
                numofproducts = request.form.get('numofproducts')
                numofsells = request.form.get('numofsells')
                totalbids = request.form.get('totalbids')
                rating = int(request.form.get('rating'))

                if rating > 5 or rating < 0:
                    flash('Rating has to be between 0 and 5','error')
                    return render_template("change-sellerinfo.html", user=current_user)

                sellerclass_title = request.form.get('sellerclass')
                sellerclassid = ""

                if numofproducts == "":
                    numofproducts = current.numofproducts
                if numofsells == "":
                    numofsells = current.numofsells
                if totalbids == "":
                    totalbids = current.totalbids
                if rating == "":
                    rating = current.rating
                if sellerclass_title == "":
                    sellerclassid = current.sellerclassid
                else:
                    sellerclass = db.get_sellerclass_by_title(sellerclass_title)
                    if sellerclass is None:
                        flash('Seller Class does not exist','error')
                        return render_template("change-sellerinfo.html", user=current_user)
                    sellerclassid = sellerclass.classid

                db.update_sellerinfo(numofproducts, numofsells, totalbids, rating, sellerclassid, current.userid)
                flash('Changed successfully', category='success')

    return render_template("change-sellerinfo.html", user=current_user)