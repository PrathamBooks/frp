# -*- coding: utf-8 -*-

import os
import uuid
from flask import (render_template,
                   g,
                   url_for,
                   redirect,
                   session,
                   flash,
                   views,
                   abort,
                   request)
from flask.ext.oauth import OAuth

from .. import app
from ..forms import (DonorSignupForm,
                     LoginForm,
                     ProfileForm)
from ..forms import beneficiary_signup_forms
from ..service import signup as signup_service
from ..service import campaign as campaign_service
from ..service import user as user_service
from ..service.decorators import login_required

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
    return session.get('facebook_token')


def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)
    session.pop('email', None)


# Signup views
@app.route('/signup')
def signup():
    return render_template('signup.html')


# @app.route('/signup/beneficary/')
# def beneficiary_signup():
#     form = BeneficarySignupForm()
#     return render_template(
#         'signup_as_beneficary_step{}.html'.format(1),
#         form=form)

def save_file_to_disk(file_object):
    if not file_object:
        return None
    directory = os.path.join(app.config['UPLOAD_DIRECTORY'], uuid.uuid4().hex)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_object.filename)
    file_object.save(file_path)
    return file_path


class SignupAsBeneficary(views.MethodView):

    def validate_and_get_redirect_step(self, step):
        accepted_keys = [
            'beneficary_signup_step{}_data'.format(step-1),
            'beneficary_signup_step{}_data'.format(step)]
        if step == 1 or accepted_keys[0] in session or accepted_keys[1] in session:
            return
        if step == 2:
            return url_for('signup_as_beneficary', step=1)

        for st in range(step-1, 0, -1):
            key = 'beneficary_signup_step{}_data'.format(st)
            if key in session or st == 1:
                url = url_for('signup_as_beneficary', step=st+1)
                return url

    @login_required
    def get(self, step=1):
        if step not in range(1, 5):
            step = 1
        redirect_url = self.validate_and_get_redirect_step(step)
        if redirect_url:
            return redirect(redirect_url)

        form = getattr(
            beneficiary_signup_forms,
            "BeneficarySignupForm{}".format(step))(request.form)
        if session.get('beneficary_signup_step{}_data'.format(step)):
            session_data = session.get(
                'beneficary_signup_step{}_data'.format(step)
            )
            for field_name, value in session_data.items():
                field = getattr(form, field_name, None)
                if field:
                    field.data = value

        preview_data = {}
        if step == 4:
            preview_data = session.get('beneficary_signup_step1_data')
            preview_data.update(
                session.get('beneficary_signup_step2_data', {}))
            preview_data.update(
                session.get('beneficary_signup_step3_data', {}))
            preview_data.update(
                session.get('beneficary_signup_step4_data', {}))
            preview_data.update(
                {
                    'category_text': beneficiary_signup_forms.get_category_text(
                        preview_data.get('category')
                    ),
                    'organization_status_text': beneficiary_signup_forms
                    .get_org_status_text(
                        preview_data.get('organization_status')
                    ),
                    'gross_total': preview_data.get('product_offerings1', 0) +
                    preview_data.get('product_offerings2', 0) +
                    preview_data.get('product_offerings3', 0) +
                    preview_data.get('product_offerings4', 0)
                }
            )
            print preview_data

        return render_template(
            'signup_as_beneficary_step{}.html'.format(step),
            form=form, step=step, preview_data=preview_data)

    @login_required
    def post(self, step=1):
        if step not in range(1, 6):
            step = 1

        form = getattr(
            beneficiary_signup_forms,
            "BeneficarySignupForm{}".format(step))(request.form)
        if form.validate():
            form_data = form.data
            if step == 3:
                image_file = request.files.get('image_file')
                video_file = request.files.get('video_file')
                form_data['image_file_path'] = save_file_to_disk(image_file)
                form_data['video_file_path'] = save_file_to_disk(video_file)

            session['beneficary_signup_step{}_data'.format(step)] = form_data

            if step == 4:
                data = session.get('beneficary_signup_step1_data')
                data.update(
                    session.get('beneficary_signup_step2_data', {}))
                data.update(
                    session.get('beneficary_signup_step3_data', {}))
                data.update(
                    session.get('beneficary_signup_step4_data', {}))
                data.update(
                    {
                        'gross_total': data.get('product_offerings1', 0) +
                        data.get('product_offerings2', 0) +
                        data.get('product_offerings3', 0) +
                        data.get('product_offerings4', 0)
                    }
                )
                campaign_service.create_campaign_from_webform(data=data)
                return render_template('beneficiary_sucess.html')
            return redirect(url_for('signup_as_beneficary', step=step+1))
        return render_template(
            'signup_as_beneficary_step{}.html'.format(step),
            form=form, step=step)

app.add_url_rule(
    '/signup/beneficary/<int:step>/',
    view_func=SignupAsBeneficary.as_view('signup_as_beneficary'))


@app.route('/signup/donor', methods=['GET', 'POST'])
def signup_as_donor():
    if request.method == 'GET':
        form = DonorSignupForm()
        return render_template('signup_as_donor.html', form=form)
    elif request.method == 'POST':
        form = DonorSignupForm(request.form)
        if form.validate():
            # Create the new user and create userinfo
            signup_service.create_donor_from_webform(form)
            return redirect(url_for('profile'))
        else:
            return render_template('signup_as_donor.html', form=form)


# Login views
@app.route('/login/facebook', methods=['GET', 'POST'])
def login_via_facebook():
    return facebook.authorize(
        callback=url_for('facebook_authorized',
                         next=request.args.get('next'),
                         _external=True))


@app.route("/login/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    data = facebook.get('me')

    signup_service.create_donor_from_facebook(data.data)
    session['email'] = data.data.get('email')
    return redirect(url_for('profile'))


@app.route('/login')
def login():
    if session.get('logged_in'):
        return redirect(url_for('profile'))
    return render_template('login.html')


@app.route('/login/webform', methods=['GET', 'POST'])
def login_via_webform():
    # IF logged in redirect
    if session.get('logged_in'):
        return redirect(url_for('profile'))

    form = LoginForm()
    if request.method == "GET":
        return render_template('login_form.html', form=form)
    elif request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            if user_service.is_valid_login(form.email.data,
                                           form.password.data):
                return redirect(url_for('profile'))
            else:
                flash('Invalid credentials')
                return render_template('login_form.html', form=form)
        else:
            return render_template('login_form.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


class EditProfile(views.MethodView):
    @login_required
    def get(self):
        form = ProfileForm()
        # We don't need password, email field
        form.delete_fields('password', 'email')
        form.set_data(g.user)
        return render_template('edit_profile.html', form=form)

    @login_required
    def post(self):
        form = ProfileForm(request.form)
        form.delete_fields('password', 'email')
        if form.validate():
            user_service.update_profile(form)
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', form=form)


app.add_url_rule('/profile/edit',
                 view_func=EditProfile.as_view('edit_profile'))


@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))
