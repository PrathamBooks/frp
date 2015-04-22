# -*- coding: utf-8 -*-

import os
import sets
import json
from flask import (render_template,
                   g,
                   url_for,
                   redirect,
                   session,
                   flash,
                   views,
                   request,
                   jsonify,
                   current_app)
from flask.ext.oauth import OAuth
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_login import login_user

from .. import app
from ..models import (Campaign, ORG_STATUS_CHOICES,Comment,Donation,User)
from ..forms import (BeneficiarySignupForm,
                     DonorForm,
                     FilterForm,
                     ProfileForm,
                     BillingInfo,
                     LANGUAGE_CHOICES,
                     STATES,
                     BENEFICIARY_CATEGORY)
from ..service import signup as signup_service
from ..service import user as user_service
from ..service import donate as donate_service
from flask_user import current_user, login_required, roles_required
from ..helpers import allowed_file
from ..models import db, BaseNameMixin, BaseMixin
from ..mailer import Mailer

mailer = Mailer()
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
    request_token_params={'scope': 'email'})

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)
    session.pop('email', None)

@app.route('/campaign/success')
@login_required
def campaign_success():
    return render_template('campaignSuccess.html')


@app.route('/billing/failure', methods=['GET', 'POST'])
def donate_failure():
  donation_id, tracking_id = donate_service.ccavResponse(request.form['encResp']) 
  donation = Donation.query.get(int(donation_id))
  campaign = donation.campaign  
  db.session.delete(donation)
  app.logger.warning('Donation id ' + str(donation_id) + ' failed. Tracking id is ' + str(tracking_id))
  db.session.commit()
  return render_template("donateFailure.html", campaign=campaign)

def send_mail(old_percent,curr_percent,campaign,donation):
  start_date = "{:%B %d, %Y}".format(campaign.start_date())
  mailer.send_email(to=donation.donor.email,
    subject="Thank you for your donation", 
    template="thank-you.html", 
    first_name=donation.donor.first_name,
    last_name=donation.donor.last_name,
    title=campaign.title)

  mailer.send_email(to=campaign.created_by.email,
    subject="New Donation Recieved ",
    template="new_donation.html",
    first_name=campaign.created_by.first_name,
    amount=donation.amount,
    donor=donation.donor_name(),
    title=campaign.title,
    start_date=start_date )

  if (old_percent < 100 <= curr_percent):
    mailer.send_email(to=campaign.created_by.email,
      subject="You’ve hit a century! Congrats",
      template="congrats.html",
      first_name=campaign.created_by.first_name,
      title=campaign.title,
      start_date=start_date)
    return

  if (old_percent == 0 ):
    mailer.send_email(to=campaign.created_by.email,
      subject="First Donation Recieved", 
      template="new_donation.html",
      first_name=campaign.created_by.first_name,
      amount=donation.amount,
      donor=donation.donor.first_name + ' ' + donation.donor.last_name,
      title = campaign.title,
      start_date=start_date)
    return

  percent_arr = [25,50,75]
  index=0
  while index < len(percent_arr):
      if (old_percent < percent_arr[index] <= curr_percent):
          mailer.send_email(to=campaign.created_by.email,
                  subject='Yay! You’ve reached '+ str(percent_arr[index])+'% of your target!',
                  template="campaign_milestone.html",
                  first_name=campaign.created_by.first_name,
                  number=index+1,
                  percent=percent_arr[index],
                  title=campaign.title,
                  start_date=start_date)
          return
      index+=1

@app.route('/billing/success', methods=['GET', 'POST'])
def donate_success():
  donation_id, tracking_id = donate_service.ccavResponse(request.form['encResp'])
  donation = Donation.query.get(int(donation_id))
  campaign = donation.campaign
  curr_percent = campaign.percent_funded()
  old_percent = curr_percent - int(round(donation.amount  * 100) /campaign.target())
  send_mail(old_percent=old_percent,curr_percent=curr_percent,campaign=campaign,donation=donation)
  donation.confirmation = tracking_id
  db.session.add(donation)
  try:
    db.session.commit()
    return render_template('donateSuccess.html', campaign=campaign)

  except Exception as e:
    app.logger.warning("Unable to save donation with id " + donation_id + " tracking num " + tracking_id)
    return render_template('donateSuccess.html', campaign=campaign)


@app.route('/signup/beneficiary', methods=['GET', 'POST'])
@login_required
def signup_as_beneficiary():
    if request.method == 'GET':
        form = BeneficiarySignupForm()
        if (current_user.organization_created):
            form.set_data(current_user.organization_created[0])
        return render_template('beneficiary_form.html', form=form)

    elif request.method == 'POST':
        form = BeneficiarySignupForm(request.form)
        if form.validate():
            image = request.files['imageUpload']
            filename = secure_filename(image.filename)
            if filename and allowed_file(filename):
                full_save_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'tmp', filename)
                image.save(full_save_path)

            result = signup_service.create_beneficiary(form, filename)
            if not result['error']:
                mailer.send_email(to=current_user.email,
                        subject="Congrats! Your registration on D-A-B is Successful!",
                        template="new_user.html", 
                        first_name=current_user.first_name)
                return redirect(url_for('campaign_success'))
            else:
                flash('Oops something went wrong, please try again')

        print form.errors
        return render_template('beneficiary_form.html', form=form)

# Login views
@app.route('/login/facebook', methods=['GET', 'POST'])
def login_via_facebook():
    if request.args.get('next'):
        return facebook.authorize(
            callback=url_for('facebook_authorized',
                         next=request.args.get('next'),
                         _external=True))
    else:
        return facebook.authorize(
            callback=url_for('facebook_authorized',
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

    user = signup_service.create_donor_from_facebook(data.data)
    login_user(user=user)
    return redirect(next_url)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


class EditProfile(views.MethodView):
    @login_required
    def get(self):
        form = ProfileForm()
        # We don't need password, email field
        form.set_data(current_user)
        return render_template('edit_profile.html', form=form)

    @login_required
    def post(self):
        form = ProfileForm(request.form)
        if form.validate():
            user_service.update_profile(form)
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', form=form)


app.add_url_rule('/profile/edit',
                 view_func=EditProfile.as_view('edit_profile'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/discover", methods=['GET'])
def discover():
    campaigns_data = Campaign.all_campaigns_data(status='Approved')
    filter_form = FilterForm(request.form)
    languages = request.args.getlist('languages')
    states = request.args.getlist('states')
    category = request.args.get('category')
    if (category == 'popular'):
        campaigns_data = sorted(campaigns_data, key=lambda x:x['num_donors'], reverse=True)
    if (category == 'recently-launched'):
        campaigns_data = sorted(campaigns_data, key=lambda x:x['days_remaining'], reverse=True)
    if (category == 'ending-soon'):
        campaigns_data = sorted(campaigns_data, key=lambda x:x['days_remaining'], reverse=False)
    if (category == 'most-funded'):
        campaigns_data = sorted(campaigns_data, key=lambda x:x['total_donations'], reverse=True)
    # Convert numbers to text strings, -1 because select values start from
    # 1 while array indexing starts from 0
    types = map(
            lambda x: ORG_STATUS_CHOICES[int(x) - 1][1], 
            request.args.getlist('types')
            )
    return render_template('discover.html', campaigns_data=campaigns_data,
            form=filter_form, languages=languages, states=states, types=types)

@app.route("/search", methods=['GET'])
def search():
    search_string = request.args.get('search-string')
    campaigns_data = Campaign.search(search_string)
    filter_form = FilterForm()
    languages = request.args.getlist('languages')
    states = request.args.getlist('states')
    # Convert numbers to text strings, -1 because select values start from
    # 1 whame array indexing starts from 0
    types = map(
            lambda x: ORG_STATUS_CHOICES[int(x) - 1][1], 
            request.args.getlist('types')
            )
    return render_template('discover.html', campaigns_data=campaigns_data,
            form=filter_form, languages=languages, states=states, types=types)

@app.route("/donate/pay", methods=['POST'])
@login_required
def pay():
  form = BillingInfo(request.form)
  donation = Donation.query.get(form.donation_id.data)
  return donate_service.ccavRequest(form, donation)

@app.route("/donate/<campaign_id>", methods=['GET', 'POST'])
@login_required
def donate(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if request.method == 'GET':
        form = DonorForm()
        if current_user.is_active():
            form.set_data(current_user)
        return render_template('donor_form.html', form=form, campaign=campaign)
    elif request.method == 'POST':
        form = DonorForm(request.form)
        if form.validate():
            result = donate_service.create_donation(form, campaign)
            if not result['error']:
                app.logger.warning('Trying to display billing page in views')
                return result['billing_info_page']
            else:
                print result
                flash('Oops something went wrong, please try again')

        app.logger.warning(form.errors)
        return render_template('donor_form.html', form=form, campaign=campaign)

@app.route("/change_status",methods=['POST'])
def change_status():
    id = request.form['campaign_id']
    status = request.form['updated_status']
    campaign = Campaign.query.get(id)
    old_status = campaign.status
    if (status != old_status):
        campaign.status = status
        if (status == "Approved"):
            campaign.approved_date_set()

        db.session.add(campaign)
        try:
          db.session.commit()
        except Exception as e:
          print e
          return "Commit Failed", 500
    start_date = "{:%B %d, %Y}".format(campaign.start_date())
    if (status == "Approved"):
        mailer.send_email(to=campaign.created_by.email,
                subject="Your D-A-B Campaign is now Live!",
                template="campaign_created.html",
                first_name=campaign.created_by.first_name,
                id=campaign.id)
    else:
        mailer.send_email(to=campaign.created_by.email,
                subject="Your D-A-B Campaign is " + status,
                template="campaign_state_change.html",
                first_name=campaign.created_by.first_name,
                title=campaign.title,
                start_date=start_date,
                old_status=old_status,
                status=status)


    campaign_data = campaign.verbose_fields()
    return jsonify(campaign_data)

class Start(views.MethodView):
    def get(self):
        form = BeneficiarySignupForm()
        if (current_user.is_active() and current_user.organization_created):
            form.set_data(current_user.organization_created[0])
        return render_template('start.html', form=form)

    @login_required
    def post(self):
        form = BeneficiarySignupForm(request.form)
        if form.validate():
            image = request.files['imageUpload']
            filename = secure_filename(image.filename)
            if filename and allowed_file(filename):
                full_save_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'tmp', filename)
                image.save(full_save_path)

            result = signup_service.create_beneficiary(form, filename)
            if not result['error']:
                return redirect(url_for('campaign_success'))
            else:
                flash('Oops something went wrong, please try again')

        print form.errors
        return render_template('start.html', form=form)

app.add_url_rule('/start',
                 view_func=Start.as_view('start'))


@app.route("/comment",methods=['POST','GET'])
@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
def add_comment():
    if request.method == "POST":
      id = request.form['campaign_id']
      new_comment = request.form['comment']
      campaign = Campaign.query.get(id)
      comment = Comment(comment_by=current_user, campaign_comment=campaign, comment=new_comment)
      db.session.add(comment)
      try:
        db.session.commit()
      except Exception as e:
        print e
        return "Commit Failed", 500

      comments = campaign.get_comments()
      return jsonify({"comments":comments})

    if request.method == "GET":
      id = request.args['campaign_id']
      campaign = Campaign.query.get(id)
      comments = campaign.get_comments()
      return jsonify({"comments":comments})

@app.route("/admin/dashboard",methods=['GET'])
@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
def admin_dashboard():
    campaigns_data = Campaign.all_campaigns_data()
    return render_template('adminDashboard.html',campaigns_data=campaigns_data)

@app.route("/profile/donor_transactions")
@login_required
def donor_transactions():
    donations=current_user.donations
    return render_template('donor_transactions.html', donations=donations)

@app.route("/profile/donor_dashboard")
@login_required
def donor_dashboard():
    donations=current_user.donations
    campaigns = []
    active_donation=closed_donation=total_active_amt=total_closed_amt=0
    total_active_children = total_closed_children = 0
    for donation in donations:
        campaigns.append(donation.campaign)
        if donation.campaign.is_active():
            active_donation+=1
            total_active_children += donation.campaign.total_impact_on_children
            total_active_amt+= donation.amount

        else:
            closed_donation+=1
            total_closed_children += donation.campaign.total_impact_on_children
            total_closed_amt+= donation.amount

    return render_template('donorDashboard.html',
            campaigns=campaigns,total_active_amt=total_active_amt,
            total_closed_amt=total_closed_amt,active_donation=active_donation,
            books_active= int(total_active_amt/50),books_closed=int(total_closed_amt/50),
            closed_donation=closed_donation, total_active_children=total_active_children,
            total_closed_children=total_closed_children)

@app.route("/profile/beneficiary_dashboard")
@login_required
def beneficiary_dashboard():
    campaigns = current_user.campaigns
    active_campaigns=0
    closed_campaigns=0
    active_donors = []
    closed_donors = []
    total_active_amt=0
    total_closed_amt=0

    for campaign in campaigns:
        if campaign.is_active():
            active_campaigns+=1
            active_donors+=campaign.donor_list()
            total_active_amt+= sum(campaign.donations)

        else:
            closed_campaigns+=1
            closed_donors+=campaign.donor_list()
            total_closed_amt+= sum(campaign.donations)

    n_active_donors = len(sets.Set(active_donors))
    n_closed_donors = len(sets.Set(closed_donors))
    num_books_recvd_active = int(total_active_amt/50)
    num_books_recvd_closed = int(total_closed_amt/50)
    return render_template('beneficiaryDashboard.html',campaigns=campaigns,
            active_campaigns=active_campaigns,
            closed_campaigns=closed_campaigns,
            total_active_amt=total_active_amt,
            total_closed_amt=total_closed_amt,
            n_active_donors=n_active_donors,
            n_closed_donors=n_closed_donors,
            num_books_recvd_active=num_books_recvd_active,
            num_books_recvd_closed=num_books_recvd_closed
            )


@app.context_processor
def convertStatusTypeToString():
    def statusString(status):
        return ORG_STATUS_CHOICES[status]
    return dict(statusString=statusString)

@app.route("/campaign/<id>", methods=['GET'])
def campaign(id):
    campaign = Campaign.query.get(id)
    donation = campaign.donations[0]
    return render_template('campaign.html', campaign=campaign)

# This code has been added for testing porpose only 
@app.route("/donate_1/<campaign_id>", methods=['GET', 'POST'])
@login_required
def donate_1(campaign_id):
    if current_app.config.get('DEBUG', True):
        campaign = Campaign.query.get(campaign_id)
        if request.method == 'GET':
            form = DonorForm()
            if current_user.is_active():
                form.set_data(current_user)
                return render_template('donor_form.html', form=form, campaign=campaign)
        elif request.method == 'POST':
            form = DonorForm(request.form)
            if form.validate():
                amount = form.amount_choice.data
                if not amount:
                    amount = form.customize_amount.data
                donor = current_user if current_user.is_active() else admin_user()
                donation = Donation(amount=amount, 
                        donor=donor, 
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        campaign=campaign, 
                        state=form.state.data, 
                        city=form.city.data, 
                        identification=form.pan_number.data,
                        tax_exemption_certificate=form.tax_exemption_certificate.data,
                        ann_choice=form.ann_choice.data)
                db.session.add(donation)
                db.session.commit()
                curr_percent = campaign.percent_funded()
                old_percent = curr_percent - int(round(donation.amount  * 100) /campaign.target())
                send_mail(old_percent=old_percent,curr_percent=curr_percent,campaign=campaign,donation=donation)
                return render_template('donor_form.html', form=form, campaign=campaign)
