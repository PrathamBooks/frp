#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#def test_selenium_basic():
  # Use webdriver.Ie() for Internet Explorer
#
#from selenium import webdriver
#driver = webdriver.Firefox()
#driver.set_window_size(1120, 550)

def test_without_username_home_login(test_browser):
	test_browser.get("http://104.199.138.202")
	test_browser.find_element_by_link_text('LOG IN').click()
	username = test_browser.find_element_by_id("infoEmail")
	password = test_browser.find_element_by_id("pass")
	username.send_keys(" ")
	password.send_keys(" ")
	element = test_browser.find_element_by_xpath("//button[contains(text(),'Login')]")
	element.submit()
	assert 'Email is required' in test_browser.page_source
	#assert 'Pratham Admin' in test_browser.page_source
	print "Logged In"



def test_bad_login(test_browser):
	#test_browser.find_element_by_link_text('LOG IN').click()
	email = test_browser.find_element_by_name('email')
	email.send_keys("pbuserasdf@prathambooks.org")
	password = test_browser.find_element_by_name('password')
	password.send_keys("admin123safsa")
	test_browser.find_element_by_xpath("//button[contains(text(), 'Login')]").submit();
	incorect_em_pw = test_browser.find_elements_by_class_name('alert')
	for i in incorect_em_pw:
		print i.text
		assert "Incorrect Email and Password" in i.text

def test_already_existing_user_signup(test_browser):
  test_browser.find_element_by_link_text('SIGN UP').click()
  email = test_browser.find_element_by_name('email')
  email.send_keys("pbuser@prathambooks.org")
  password = test_browser.find_element_by_name('password')
  password.send_keys("admin123")
  retype_password = test_browser.find_element_by_name('retype_password')
  retype_password.send_keys("admin123")
  test_browser.find_element_by_xpath("//button[contains(text(), 'Go')]").submit();
  incorect_em_pw = test_browser.find_elements_by_class_name('alert')
  for i in incorect_em_pw:
    print i.text
    assert "This Email is already in use. Please try another one." in i.text

def test_donate(test_browser):
  test_browser.find_element_by_link_text('Donate').click()
 
  #test_browser.get("http://104.199.138.202/donate")
  assert "donate-a-book" in test_browser.title

def test_sort_by_filter(test_browser):
  for radio_button in test_browser.find_elements_by_css_selector("input[type='radio']"):
    radio_button.click()

def test_home_login(test_browser):
	#test_browser.get("http://104.199.138.202")
	test_browser.find_element_by_link_text('LOG IN').click()
	username = test_browser.find_element_by_id("infoEmail")
	password = test_browser.find_element_by_id("pass")
	username.send_keys("pbuser@prathambooks.org")
	password.send_keys("admin123")
	element = test_browser.find_element_by_xpath("//button[contains(text(),'Login')]")
	element.submit()
	assert 'You have signed in successfully.' in test_browser.page_source
	assert 'Pratham Admin' in test_browser.page_source
	print "Logged In"
	#select= test_browser.find_element_by_id("profile-btn")
	#select.click()
	#test_browser.find_element_by_link_text('Logout').click()

def test_setup_form(test_browser):
   test_browser.get("http://104.199.138.202/setup")
   #test_browser.find_element_by_link_text('Set Up').click()
   test_browser.find_elements_by_css_selector("input[type='radio'][value='2']")[0].click()
   orginistion=test_browser.find_element_by_name('title')
   orginistion.send_keys("Mirafra Technologies")
   test_browser.find_elements_by_css_selector("input[type='radio'][value='1']")[1].click()
   Office_addr=test_browser.find_element_by_name('address')
   Office_addr.send_keys("Akshay Tech Park, Plot No. 72 & 73,, 2nd Floor, EPIP Zone, Whitefield, Bengaluru, Karnataka 560066")
   contact_number=test_browser.find_element_by_name('contact_number')
   contact_number.send_keys("90022403")
   email=test_browser.find_element_by_name('email')
   email.send_keys("sandeep@gmail.com")
   website=test_browser.find_element_by_name('website')
   website.send_keys("http://www.mirafra.com")
   facebook=test_browser.find_element_by_name('facebook')
   facebook.send_keys("http://facebook.com/mirafra")
   blog=test_browser.find_element_by_name('blog')
   blog.send_keys("http://blog.com/mirafra")
   person1_name=test_browser.find_element_by_name('person1_name')
   person1_name.send_keys("sandeep")
   person1_position=test_browser.find_element_by_name('person1_position')
   person1_position.send_keys("engineer")
   person1_email=test_browser.find_element_by_name('person1_email')
   person1_email.send_keys("sandeep@gmail.com")
   person1_phone=test_browser.find_element_by_name('person1_phone')
   person1_phone.send_keys("956483164")
   test_browser.find_element_by_id("next").click()
   test_browser.find_element_by_link_text('Set Up').click()
   alert = test_browser.switch_to.alert
   alert.accept()
   
def test_setup_formNagitive(test_browser):
   #test_browser.get("http://104.199.138.202/setup")
   #title_color=test_browser.find_element_by_name('title')
   test_browser.find_element_by_id("next").click()
   #assert 'Please select any one option below. *' in test_browser.page_source
   assert ' Error in this section' in test_browser.page_source
   test_browser.find_element_by_xpath("//button[contains(text(),'OK')]").click()
   title_color=test_browser.find_element_by_name('title').value_of_css_property("border-color")
   print "title_color::"
   print title_color
   address_color=test_browser.find_element_by_name('address').value_of_css_property("border-color")
   print "address_color"
   print address_color
   contact_number_color=test_browser.find_element_by_name('contact_number').value_of_css_property("border-color")
   print "contact_number_color::"
   print contact_number_color
   email_color=test_browser.find_element_by_name('email').value_of_css_property("border-color")
   print "email_color::"
   print email_color
   website_color=test_browser.find_element_by_name('website').value_of_css_property("border-color")
   print "website_color::"
   print website_color
   facebook_color=test_browser.find_element_by_name('facebook').value_of_css_property("border-color")
   print "facebook_color::"
   print facebook_color
   blog_color=test_browser.find_element_by_name('blog').value_of_css_property("border-color")
   print "blog_color::"
   print blog_color
   person1_name_color=test_browser.find_element_by_name('person1_name').value_of_css_property("border-color")
   print "person1_name_color::"
   print person1_name_color
   person1_position_color=test_browser.find_element_by_name('person1_position').value_of_css_property("border-color")
   print "person1_position_color::"
   print person1_position_color
   person1_email_color=test_browser.find_element_by_name('person1_email').value_of_css_property("border-color")
   print "person1_email_color::"
   print person1_email_color
   person1_phone_color=test_browser.find_element_by_name('person1_phone').value_of_css_property("border-color")
   print "person1_phone_color::"
   print person1_phone_color
   #test_browser.close()
   #alert = test_browser.switch_to.alert
   #alert.accept()
   
# def test_homepage(test_browser):
# 	test_browser.get("http://104.199.138.202")
# 	assert "donate-a-book" in test_browser.title

  
# def test_language_filter(test_browser):
#   for checkbox in test_browser.find_elements_by_xpath("//*[@type='checkbox']"):
#     checkbox.click()
#     for i in test_browser.find_elements_by_xpath("//*[@class='campaignInfo']"):
#       print "----------------Language-----------------"
#       print checkbox.get_attribute("value")
#       #if checkbox.get_attribute("value") != "All":
#         #assert checkbox.get_attribute("value") in i.text
#       print i.text
      
#     checkbox.click()

# def test_type_filter(test_browser):
#   test_browser.find_element_by_xpath("//*[@data-target='#type']").click()
#   for checkbox in test_browser.find_elements_by_xpath("//*[@type='checkbox']"):
#     checkbox.click()
#     for i in test_browser.find_elements_by_xpath("//*[@class='campaignInfo']"):
#       print "----------------Type-----------------"
#       print checkbox.get_attribute("value")
#       #if checkbox.get_attribute("value") != "All":
#         #assert checkbox.get_attribute("value") in i.text
#       print i.text
#     checkbox.click()

# def test_state_filter(test_browser):
#   test_browser.find_element_by_xpath("//*[@data-target='#state']").click()
#   for checkbox in test_browser.find_elements_by_xpath("//*[@type='checkbox']"):
#     checkbox.click()
#     for i in test_browser.find_elements_by_xpath("//*[@class='campaignInfo']"):
#       print "----------------State-----------------"
#       print checkbox.get_attribute("value")
#       #if checkbox.get_attribute("value") != "All":
#         #assert checkbox.get_attribute("value") in i.text
#       print i.text
#     checkbox.click()

# def test_login(test_browser):
#   test_browser.find_element_by_link_text('LOG IN').click()
#   email = test_browser.find_element_by_name('email')
#   email.send_keys("pbuser@prathambooks.org")
#   password = test_browser.find_element_by_name('password')
#   password.send_keys("admin123")
#   test_browser.find_element_by_xpath("//button[contains(text(), 'Login')]").submit();
#   profile = test_browser.find_element_by_id("profile-btn")
#   print profile.text
#   assert "PRATHAM ADMIN" in profile.text



def test_about_page(test_browser):
  test_browser.find_element_by_link_text('About').click()
  alert = test_browser.switch_to.alert
  alert.accept()
  about_donate_books = test_browser.find_element_by_xpath("//*[@href='#donateBook']")
  assert "Pratham Books' Donate-a-Book" in about_donate_books.text
  about_pratham_books = test_browser.find_element_by_xpath("//*[@href='#prathamBook']")
  about_pratham_books.click()
  assert "About Pratham Books" in about_pratham_books.text
  about_pratham_books = test_browser.find_element_by_xpath("//*[@href='#faq']")
  about_pratham_books.click()
  #assert "Beneficiary FAQs" in test_browser.text
  print test_browser.find_element_by_id('accordion')
  terms = test_browser.find_element_by_xpath("//*[@href='#terms']")
  terms.click()
  privacy = test_browser.find_element_by_xpath("//*[@href='#privacy']")
  privacy.click()
  contact_us = test_browser.find_element_by_xpath("//*[@href='#contact']")
  contact_us.click()
  
def test_logout(test_browser):
  test_browser.find_element_by_id("profile-btn").click()
  test_browser.find_element_by_link_text('Logout').click()
  #assert "LOG IN" in test_browser.find_element_by_link_text('LOG IN')
  
# email.send_keys("pbuser@prathambooks.org")
 

# login_submit = driver.find_element_by_xpath("//button[contains(text(), 'Login')]")
# login_submit.submit()

#	print driver.current_url
#	driver.find_element_by_link_text('DONATE NOW').click()
#	driver.implicitly_wait(15)
#	print driver.current_url
#	driver.find_elements_by_css_selector("input[type='radio'][value='Featured']")[0].click
#
#button_parent = driver.find_element_by_id('sort-by')
#driver.implicitly_wait(15)
#ac(driver).move_to_element(button_parent).perform()
#button_parent.click()
#ac(driver).send_keys(Keys.SPACE).perform()
#for i in driver.find_elements_by_xpath("//*[@type='radio']"):
#	print i.get_attribute("value")
#	driver.implicitly_wait(30)
#	i.click()
#	driver.implicitly_wait(30)
#driver.find_element_by_xpath("//*[@data-target='#type']").click()
#driver.find_element_by_xpath("//*[@data-target='#state']").click()
#driver.find_element_by_link_text('State').click()	
#for i in driver.find_elements_by_xpath("//*[@type='checkbox']"):
#	print i.get_attribute("value")
#	driver.implicitly_wait(30)
#	i.click()
#	i.click()
#	driver.implicitly_wait(30)

#ac(driver).move_to_element(button_parent).perform()
#button_parent.click()
# driver.find_elements_by_css_selector("input[type='radio'][value='Featured']").click
# driver.implicitly_wait(5)
# driver.find_elements_by_css("input[type='radio'][value='Popular']").click
# driver.implicitly_wait(5)
# driver.find_elements_by_css("input[type='radio'][value='Recently Launched']").click
# driver.implicitly_wait(5)
# driver.find_elements_by_css("input[type='radio'][value='Ending Soon']").click
# driver.implicitly_wait(5)
# driver.find_elements_by_css("input[type='radio'][value='Most Funded']").click
# driver.implicitly_wait(5)




# login_link = driver.find_element_by_link_text('LOG IN')
# login_link.click();
# email = driver.find_element_by_name('email')
# password = driver.find_element_by_name('password')
# email.send_keys("pbuser@prathambooks.org")
# password.send_keys("admin123")
# login_submit = driver.find_element_by_xpath("//button[contains(text(), 'Login')]")
# login_submit.submit()
# driver.implicitly_wait(30);
# signup_link = driver.find_element_by_link_text('SIGN UP')
# signup_link.click();

#driver.close()  
