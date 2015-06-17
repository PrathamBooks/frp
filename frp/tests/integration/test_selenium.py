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
   test_browser.close()
   alert = test_browser.switch_to.alert
   alert.accept()
   
   
  







