def test_homepage(test_browser):
	test_browser.get("http://104.199.138.202")
	assert "donate-a-book" in test_browser.title

def test_donate(test_browser):
  test_browser.find_element_by_link_text('DONATE NOW').click()
  #test_browser.get("http://104.199.138.202/donate")
  assert "donate-a-book" in test_browser.title

def test_sort_by_filter(test_browser):
  for radio_button in test_browser.find_elements_by_css_selector("input[type='radio']"):
    radio_button.click()
  
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

def test_login(test_browser):
  test_browser.find_element_by_link_text('LOG IN').click()
  email = test_browser.find_element_by_name('email')
  email.send_keys("pbuser@prathambooks.org")
  password = test_browser.find_element_by_name('password')
  password.send_keys("admin123")
  test_browser.find_element_by_xpath("//button[contains(text(), 'Login')]").submit();
  profile = test_browser.find_element_by_id("profile-btn")
  print profile.text
  assert "PRATHAM ADMIN" in profile.text

def test_logout(test_browser):
  test_browser.find_element_by_id("profile-btn").click()
  test_browser.find_element_by_link_text('Logout').click()
  #assert "LOG IN" in test_browser.find_element_by_link_text('LOG IN')

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

def test_about_page(test_browser):
  test_browser.find_element_by_link_text('About').click()
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
