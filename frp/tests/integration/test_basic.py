from splinter import Browser
                  

def test_create_item():
    with Browser() as browser:
        # Visit URL
        browser.visit("http://localhost:5000/product/add")
        browser.visit("http://localhost:5000/product/add")
        browser.find_by_id("name").type("Zombie")
        browser.find_by_id("description").type("underdog")
        button = browser.find_by_tag("button")
        button.click()

        if browser.is_text_present('Zombie'):
            print "Yes, the product was added!"
        else:
            print "No, it wasn't added"
