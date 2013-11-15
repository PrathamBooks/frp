from splinter import Browser

def test_create_item():
    with Browser() as browser:
        # Visit URL
        browser.visit("http://frp-test.prathambooks.org/")
        assert browser.is_text_present("Calligraphy")
