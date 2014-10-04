# -*- coding: utf-8 -*-

import flask
from flask.ext.oauth import OAuth

from .. import app
from ..forms import DonorSignupForm, LoginForm, BeneficarySignupForm
from ..service import signup as signup_service
from ..service import user as user_service
from ..service.decorators import login_required


request = flask.request
# Facebook requirements
oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    request_token_url=None,
    base_url='https://graph.facebook.com/',
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config.get('FACEBOOK_CONSUMER_KEY'),
    consumer_secret=app.config.get('FACEBOOK_CONSUMER_SECRET'),
    request_token_params={'scope': 'email, '})


@facebook.tokengetter
def get_facebook_token():
    return flask.session.get('facebook_token')


def pop_login_session():
    flask.session.pop('logged_in', None)
    flask.session.pop('facebook_token', None)
    flask.session.pop('email', None)


# Signup views
@app.route('/signup')
def signup():
    return flask.render_template('signup.html')


@app.route('/signup/beneficary')
def signup_as_beneficary():
    form = BeneficarySignupForm()
    return flask.render_template('signup_as_beneficary.html', form=form)


@app.route('/signup/donor', methods=['GET', 'POST'])
def signup_as_donor():
    if request.method == 'GET':
        form = DonorSignupForm()
        return flask.render_template('signup_as_donor.html', form=form)
    elif request.method == 'POST':
        form = DonorSignupForm(request.form)
        if form.validate():
            # Create the new user and create userinfo
            signup_service.create_donor_from_webform(form)
            return flask.redirect(flask.url_for('profile'))
        else:
            return flask.render_template('signup_as_donor.html', form=form)


# Login views
@app.route('/login/facebook', methods=['GET', 'POST'])
def login_via_facebook():
    return facebook.authorize(
        callback=flask.url_for('facebook_authorized',
                               next=request.args.get('next'),
                               _external=True))


@app.route("/login/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or flask.url_for('index')
    if resp is None or 'access_token' not in resp:
        return flask.redirect(next_url)

    flask.session['logged_in'] = True
    flask.session['facebook_token'] = (resp['access_token'], '')
    data = facebook.get('me')

    signup_service.create_donor_from_facebook(data.data)
    flask.session['email'] = data.data.get('email')
    return flask.redirect(flask.url_for('profile'))


@app.route('/login')
def login():
    return flask.render_template('login.html')


@app.route('/login/webform', methods=['GET', 'POST'])
def login_via_webform():
    # IF logged in redirect
    if flask.session.get('logged_in'):
        return flask.redirect(flask.url_for('profile'))

    form = LoginForm()
    if request.method == "GET":
        return flask.render_template('login_form.html', form=form)
    elif request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            if user_service.is_valid_login(form.email.data, form.password.data):
                return flask.redirect(flask.url_for('profile'))
            else:
                flask.flash('Invalid credentials')
                return flask.render_template('login_form.html', form=form)
        else:
            return flask.render_template('login_form.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return flask.render_template('profile.html')


@app.route("/logout")
def logout():
    pop_login_session()
    return flask.redirect(flask.url_for('index'))
