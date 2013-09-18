from splinter import Browser
                  
with Browser() as browser:
    # Visit URL
    url = "http://localhost:5000/product/add"
    browser.visit(url)
    # Logs in
    showmore = browser.find_by_id('showmore')
    showmore.click()
    browser.find_by_id("username").type("noufal")
    browser.find_by_id("password").type("abcd")
    button = browser.find_by_tag("button")
    button.click()

    if browser.is_text_present('Zombie'):
        print "Yes, the product was added!"
    else:
        print "No, it wasn't added"
