from flask import Flask, render_template, request, session, g, abort, flash, url_for, redirect
from werkzeug import check_password_hash, generate_password_hash

import settings
import models

app = Flask(__name__)
app.config.from_object(settings)

__VERSION__ = "0.1"

@app.context_processor
def inject_user():
    return dict(version=__VERSION__)

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
def product_add():
    if request.method == "GET":
        if not g.user:
            abort(401)
    if request.method == "POST":
        name = request.form['name'] 
        user = g.user
        description = request.form['description']
        product = models.Product(name, description, user = user)
        models.db.session.add(product)
        models.db.session.commit()
        flash("%s added to catalogue"%name)
    return render_template("create_product.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if g.user:
        flash("You're already logged in")
        return redirect("/")
    if request.method == "POST":
        user = models.User.query.get(request.form['name'])
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.name
            flash("Welcome %s"%user.name)
            return redirect("/")
    return render_template("login_form.html")


@app.route("/logout")
def logout():
    del session['user_id']
    return redirect("/")
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        print request.form['name']
        print request.form['email']
        print request.form['password']

        user = models.User(name = request.form['name'],
                           email = request.form['email'],
                           password = generate_password_hash(request.form['password']))
        models.db.session.add(user)
        models.db.session.commit()
        session['user_id'] = user.name

        
        flash("Thanks for registering")
        return redirect(url_for('register'))
    return render_template("register_user.html")


     


if __name__ == "__main__":
    app.run()
