from flask import render_template, request, session, g, abort, flash, url_for, redirect
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.lastuser.sqlalchemy import UserManager

from . import app, lastuser
from . import models
from .models import db

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = models.User.query.get(session['user_id'])

@app.route("/")
def index():
    products = models.Product.query.all()
    return render_template('index.html', 
                           products = products)
    
    
@app.route("/product/add", methods=['GET', 'POST'])
@lastuser.requires_login
def product_add():
    if request.method == "POST":
        name = request.form['name'] 
        user = g.user
        description = request.form['description']
        product = models.Product(name, description, user = user)
        db.session.add(product)
        db.session.commit()
        flash("%s added to catalogue"%name)
    return render_template("create_product.html")


@app.route('/login')
@lastuser.login_handler
def login():
    return {'scope': 'id email'}

@app.route('/login/redirect')
@lastuser.auth_handler
def lastuserauth():
    # Save the user object
    db.session.commit()
    print dir(request.form)
    return redirect("/")


@app.route('/logout')
@lastuser.logout_handler
def logout():
    flash("You are now logged out", category='info')
    return "/"
    

@lastuser.auth_error_handler
def lastuser_error(error, error_description=None, error_uri=None):
    if error == 'access_denied':
        flash("You denied the request to login", category='error')
        return redirect("/")
    print error
    print error_description
    print error_uri
    return render_template("autherror.html",
        error=error,
        error_description=error_description,
        error_uri=error_uri)
