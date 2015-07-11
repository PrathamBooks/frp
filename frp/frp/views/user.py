# -*- coding: utf-8 -*-

import os
import sets
import json
from datetime import *
import random
import pyexcel_xls
from flask import (render_template,
                   g,
                   url_for,
                   redirect,
                   session,
                   flash,
                   views,
                   request,
                   jsonify,
                   current_app,
                   get_flashed_messages)
from flask.ext.oauth import OAuth
from flask.ext import excel
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_login import login_user
from flask_user.forms import RegisterForm

from .. import app
from ..models import (Campaign,ORG_STATUS_CHOICES,USER_STATUS,Comment,Donation,User,UserAuth,Memory)
from ..forms import (BeneficiarySignupForm,
                     DonorForm,
                     FilterForm,
                     ProfileForm,
                     MemoryForm,
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
  donation_id, tracking_id, order_status = donate_service.ccavResponse(request.form['encResp']) 
  donation = Donation.query.get(int(donation_id))
  campaign = donation.campaign  
  db.session.delete(donation)
  db.session.commit()
  return render_template("donateFailure.html", campaign=campaign)

def send_mail(old_percent,curr_percent,campaign,donation):
  start_date = "{:%B %d, %Y}".format(campaign.start_date())
  mailer.send_email(to=donation.donor.email,
    subject="Thank you for your donation", 
    template="thank-you.html", 
    profile_name=donation.donor.profile_name(),
    title=campaign.title)

  mailer.send_email(to=campaign.emails(),
    subject="New Donation Received ",
    template="new_donation.html",
    profile_name=campaign.created_by.profile_name(),
    amount=donation.amount,
    donor=donation.donor_name(),
    title=campaign.title,
    start_date=start_date)

  app.logger.warning("old_percent = " + str(old_percent) + " curr_percent = " + str(curr_percent))
  if (old_percent < 100 <= curr_percent):
    mailer.send_email(to=campaign.emails(),
      subject="You've hit a century! Congrats",
      template="congrats.html",
      profile_name=campaign.created_by.profile_name(),
      title=campaign.title,
      start_date=start_date)
    app.logger.warning("Sent 100% email")
    return

  if (old_percent == 0):
    mailer.send_email(to=campaign.emails(),
      subject="First Donation Recieved",
      template="new_donation.html",
      profile_name=campaign.created_by.profile_name(),
      amount=donation.amount,
      donor=donation.donor_name(),
      title = campaign.title,
      start_date=start_date)
    return

  percent_arr = [25,50,75]
  index=0
  while index < len(percent_arr):
      if (old_percent < percent_arr[index] <= curr_percent):
          mailer.send_email(to=campaign.emails(),
                  subject="Yay! You've reached "+ str(percent_arr[index])+"% of your target!",
                  template="campaign_milestone.html",
                  number=index+1,
                  profile_name=campaign.created_by.profile_name(),
                  percent=percent_arr[index],
                  title=campaign.title,
                  start_date=start_date)
          return
      index+=1

@app.route('/billing/success', methods=['GET', 'POST'])
def donate_success():
  donation_id, tracking_id, order_status = donate_service.ccavResponse(request.form['encResp'])
  donation = Donation.query.get(int(donation_id))
  campaign = donation.campaign
  if (order_status == 'Success'):
          old_percent = campaign.percent_funded()
          curr_percent = int(round(((campaign.total_donations() + donation.amount)  * 100.0) / campaign.target()))
          send_mail(old_percent=old_percent,curr_percent=curr_percent,campaign=campaign,donation=donation)
	  app.logger.warning('Donation id ' + str(donation_id) + ' successful. Tracking id is ' + str(tracking_id))

	  if (curr_percent >= 100):
	      campaign.status = 'Closed'
	      db.session.add(campaign)

	  donation.confirmation = tracking_id
	  db.session.add(donation)
	  try:
	    db.session.commit()

	  except Exception as e:
	    app.logger.warning("Unable to save donation with id " + donation_id + " tracking num " + tracking_id)
	    return render_template('donateSuccess.html', campaign=campaign)

	  return render_template('donateSuccess.html', campaign=campaign)
  db.session.delete(donation)
  app.logger.warning('Donation id ' + str(donation_id) + ' failed. Tracking id is ' + str(tracking_id))
  db.session.commit()
  return render_template("donateFailure.html", campaign=campaign)
   
@app.route("/campaign/edit/<id>", methods=['GET'])
@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
def campaign_edit(id):
    campaign = Campaign.query.get(id)
    if (campaign):
        form = BeneficiarySignupForm()
        form.set_edit_data(campaign)
        return render_template('start.html', form=form, action=url_for('campaign', id=campaign.id))
    return render_template("404.html", error="Campaign with id " + str(id) + " does not exist",
            error_description="",
            error_uri=request.url)

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
                        subject="Congrats! You successfully created a campaign on Donate-a-Book!",
                        template="new_campaign.html",
                        profile_name=current_user.profile_name())
                return redirect(url_for('campaign_success'))
            else:
                flash('Oops something went wrong, please try again')

        print form.errors
        return render_template('beneficiary_form.html', form=form)

@app.route('/after_register')
def after_register():
  # clear the flashes so that the message from flask_user does not show up on
  # the web page
  session['_flashes'] = []
  return render_template('after_register.html')

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

@app.route("/donate", methods=['GET'])
def discover():
    campaigns_data = Campaign.all_campaigns_data('Approved','Closed')
    random.shuffle(campaigns_data)
    filter_form = FilterForm(request.form)
    category = request.args.get('category')
    if (category == 'featured'):
        category = 'Featured'
    if (category == 'popular'):
        category = 'Popular'
    if (category == 'recently-launched'):
        category = 'Recently Launched'
    if (category == 'ending-soon'):
        category = 'Ending Soon'
    if (category == 'most-funded'):
        category = 'Most Funded'
    if (not category):
        category = 'Recently Launched'
    return render_template('discover.html', campaigns_data=campaigns_data,
            form=filter_form, category=category)

@app.route("/search", methods=['GET'])
def search():
    search_string = request.args.get('search-string')
    campaigns_data = Campaign.search(search_string)
    random.shuffle(campaigns_data)
    filter_form = FilterForm()
    return render_template('discover.html', campaigns_data=campaigns_data,
            form=filter_form, category='Recently Launched', search_string=search_string)

@app.route("/donate/<campaign_id>", methods=['GET', 'POST'])
@login_required
def donate(campaign_id):
  if current_user.has_roles('admin'):
    return redirect("/admin/donate/"+str(campaign_id))
  else:  
    campaign = Campaign.query.get(campaign_id)
    admin_fields_enable = False
    if request.method == 'GET':
        form = DonorForm()
        if current_user.is_active():
            form.set_data(current_user)
        return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)
    elif request.method == 'POST':
        form = DonorForm(request.form)
        if form.validate():
            result = donate_service.create_donation(form, campaign)
            if not result['error']:
                return donate_service.ccavRequest(form, result['donation'])
            else:
                print result
                flash('Oops something went wrong, please try again')

        app.logger.warning(form.errors)
        return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)

@app.route("/change_featured",methods=['POST'])
def change_featured():
    id = request.form['campaign_id']
    campaign = Campaign.query.get(id)
    campaign.featured = not campaign.featured
    db.session.add(campaign)

    try:
      db.session.commit()
    except Exception as e:
      app.logger.warning(e)
      return "Commit Failed", 500

    campaign_data = campaign.verbose_fields()
    return jsonify(campaign_data)

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
        mailer.send_email(to=campaign.emails(),
                subject="Your D-A-B Campaign is now Live!",
                template="campaign_created.html",
                profile_name=campaign.created_by.profile_name(),
                id=campaign.id)
    else:
        mailer.send_email(to=campaign.emails(),
                subject="Your D-A-B Campaign is " + status,
                template="campaign_state_change.html",
                profile_name=campaign.created_by.profile_name(),
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
        if form.website.data:
            form.website.data = form.website.data.strip() 
        if form.facebook.data:
            form.facebook.data = form.facebook.data.strip() 
        if form.blog.data:
            form.blog.data = form.blog.data.strip() 
        if form.validate():
            print "validated form"
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

app.add_url_rule('/setup',
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

@app.route("/admin/add_user",methods=['GET', 'POST'])
@login_required
#@roles_required('admin')    # Limits access to users with the 'admin' role
def admin_add_user():
    if request.method == "GET":
        form = RegisterForm()
        return render_template('flask_user/add_user.html', form=form)
    else:
        form = RegisterForm(request.form)
        if (form.validate()):
            user = User(status=USER_STATUS.ACTIVE, active=True, email=form.email.data, confirmed_at=datetime.now())
            db.session.add(user)

            user_auth = UserAuth(password=current_app.user_manager.hash_password(form.password.data),
                    user=user, active=True)
            db.session.add(user_auth)
            try:
                db.session.commit()
            except Exception as e:
                app.logger.warning("Failed to add user " + form.email.data)
                app.logger.warning(e)
                return render_template('flask_user/add_user.html', form=form)

            return redirect(url_for('user_add_success', id=user.id))

        return render_template('flask_user/add_user.html', form=form)

@app.route("/admin/user_add_success/<id>", methods=['GET'])
@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
def user_add_success(id):
    user = User.query.get(id)
    return render_template("flask_user/user_add_success.html", user=user)

@app.route("/admin/dashboard",methods=['GET', 'POST'])
@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
def admin_dashboard():
    campaigns_data = Campaign.all_campaigns_data()
    return render_template('adminDashboard.html',campaigns_data=campaigns_data)

@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
@app.route("/download/donations",methods=['GET'])
def download_donations():
    donations = Donation.query.all()
    donations_data = map(lambda x:x.donation_details(),donations)
    header = ["Donor Name"," Donor City","Donor State","Donor Address","Identification_Type","Identification","Donor Email", "Date", "Campaign Title", "Amount Donated",
            "Anonymous Donor", "80 G Cert Requested", "Confirmation Number"]
    donations_data.insert(0,header)
    return excel.make_response_from_array(donations_data, "xls")


@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
@app.route("/download/campaigns",methods=['GET'])
def download_campaigns():
    campaigns = Campaign.query.all()
    campaigns_data = map(lambda x:x.campaign_details(),campaigns)
    header = ['Title','Start Date','Remaining Days','Number of Donors','Target amount','Books', 'LIC', 'Funds Raised','Status','Name','Organization Email_Id','Organization Phone Numbers','Person Email_Id','Person Phone Number','Language']
    campaigns_data.insert(0,header)
    return excel.make_response_from_array(campaigns_data, "xls")


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
        if (donation.confirmation):
            campaigns.append(donation.campaign)
            if donation.campaign.is_active():
                active_donation+=1
                total_active_children += donation.campaign.total_impact_on_children
                total_active_amt+= donation.amount

            else:
                closed_donation+=1
                total_closed_children += donation.campaign.total_impact_on_children
                total_closed_amt+= donation.amount

    cost_per_book = app.config.get('COST_PER_BOOK')

    return render_template('donorDashboard.html',
            campaigns=campaigns,total_active_amt=total_active_amt,
            total_closed_amt=total_closed_amt,active_donation=active_donation,
            books_active= int(total_active_amt/cost_per_book),books_closed=int(total_closed_amt/cost_per_book),
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
    cost_per_book = app.config.get('COST_PER_BOOK')
    num_books_recvd_active = int(total_active_amt/cost_per_book)
    num_books_recvd_closed = int(total_closed_amt/cost_per_book)
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
        return ORG_STATUS_CHOICES[status - 1]
    return dict(statusString=statusString)

@app.route("/campaign/<id>", methods=['GET', 'POST'])
def campaign(id):
    campaign = Campaign.query.get(id)
    if request.method == 'GET' or request.method == 'HEAD':
        return render_template('campaign.html', campaign=campaign)
    else:
        form = BeneficiarySignupForm(request.form)
        if form.validate():
            image = request.files['imageUpload']
            filename = secure_filename(image.filename)
            if filename and allowed_file(filename):
                full_save_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'tmp', filename)
                image.save(full_save_path)

            result = signup_service.edit_beneficiary(campaign, form, filename)
            if not result['error']:
                flash('You successfully edited the campaign')
                return render_template('campaign.html', campaign=campaign)
            else:
                flash('Oops something went wrong, please try again')
        return render_template('beneficiary_form.html', form=form)

# This code has been added for alternate workflow for donations that directly come to PB
@app.route("/admin/donate/<campaign_id>", methods=['GET', 'POST'])
@login_required
@roles_required('admin')    # Limits access to users with the 'admin' role
def donate_admin(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    admin_fields_enable = True
    if request.method == 'GET':
        form = DonorForm()
        if current_user.is_active():
            form.set_data(current_user)
            return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)
    elif request.method == 'POST':
        form = DonorForm(request.form)
        if form.validate():
            amount = form.amount_choice.data
            if not amount:
                amount = form.customize_amount.data
            donor = User.query.filter_by(email=form.user_email.data).first()
            if donor:
              donation = Donation(amount=amount,
                      donor=donor,
                      first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      campaign=campaign,
                      address=form.address.data,
                      state=form.state.data,
                      city=form.city.data,
                      confirmation=form.confirmation.data,
                      identification_type="PAN Card",
                      identification=form.pan_number.data,
                      tax_exemption_certificate=form.tax_exemption_certificate.data,
                      ann_choice=form.ann_choice.data)
              db.session.add(donation)
              db.session.commit()
              curr_percent = campaign.percent_funded()
              old_percent = curr_percent - int(round(donation.amount  * 100) /campaign.target())
              send_mail(old_percent=old_percent,curr_percent=curr_percent,campaign=campaign,donation=donation)
              flash('Successfully donated for this campaign')
              return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)
            else:
              flash('Unable to find donor in the system with the given email. Please try another email.')
              return render_template("donor_form.html", form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)
        else:
            print form.errors
            return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)



# This code has been added for testing porpose only 
@app.route("/donate_1/<campaign_id>", methods=['GET', 'POST'])
@login_required
def donate_1(campaign_id):
    if current_app.config.get('DEBUG', True):
        campaign = Campaign.query.get(campaign_id)
        admin_fields_enable = False
        if request.method == 'GET':
            form = DonorForm()
            if current_user.is_active():
                form.set_data(current_user)
                return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)
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
                        address=form.address.data,
                        state=form.state.data, 
                        city=form.city.data, 
                        confirmation=12345,
                        identification_type="PAN Card",
                        identification=form.pan_number.data,
                        tax_exemption_certificate=form.tax_exemption_certificate.data,
                        ann_choice=form.ann_choice.data)
                db.session.add(donation)
                db.session.commit()
                curr_percent = campaign.percent_funded()
                old_percent = curr_percent - int(round(donation.amount  * 100) /campaign.target())
                send_mail(old_percent=old_percent,curr_percent=curr_percent,campaign=campaign,donation=donation)
                return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)
            else:
                print form.errors
                return render_template('donor_form.html', form=form, campaign=campaign, admin_fields_enable=admin_fields_enable)


@app.route("/memories",methods=['GET', 'POST'])
def memories():
    all_memories = Memory.query.filter_by(can_share=True).all()
    if request.method == 'GET':
        form = MemoryForm()
        return render_template('memories.html', form=form, memories=all_memories)
    else:
        form = MemoryForm(request.form)
        user = current_user if current_user.is_active() else None
        if form.validate():
            memory = Memory(name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    email=form.email.data,
                    can_share=form.can_share.data,
                    memory_by=user,
                    words=form.words.data)
            db.session.add(memory)
            db.session.commit()
            all_memories = Memory.query.filter_by(can_share=True).all()
            return render_template("memories.html", memories=all_memories)
        else:
            return render_template("memories.html", memories=all_memories, form=form)


