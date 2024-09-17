# %%
import time

import yaml
from chromedriver_py import binary_path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client


# %%
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return chrome_options


def get_avail_string(
    driver,
    url="https://www.lenovo.com/us/en/laptops/legion-laptops/legion-7-series/Legion-7-16ITH6/p/LEN101G0002",
):
    driver.get(url)

    # check if item is temporarily unavailable
    try:
        check_avail = driver.find_element_by_xpath(
            "//*[contains(text(), 'TEMPORARILY UNAVAILABLE')]"
        )
    except NoSuchElementException:
        check_avail = None

    return check_avail


def check_cart_button(
    driver,
    url="https://www.lenovo.com/us/en/laptops/legion-laptops/legion-7-series/Legion-7-16ITH6/p/LEN101G0002",
):
    driver.get(url)

    l7_cart = driver.find_element_by_xpath(
        '//*[@id="addToCartFormTop82K60004US"]/button'
    )
    l7_cart_flag = l7_cart.is_enabled()

    return l7_cart_flag


def message_avail(twilio_creds):
    account_sid = twilio_creds["project_info"]["account_sid"]
    auth_token = twilio_creds["project_info"]["auth_token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="The Legion 7 is available now! \n Go buy it at: https://www.lenovo.com/us/en/laptops/legion-laptops/legion-7-series/Legion-7-16ITH6/p/LEN101G0002",
        from_=twilio_creds["project_info"]["phone_number"],
        to="+15852811928",
    )


def message_unavail(twilio_creds):
    account_sid = twilio_creds["project_info"]["account_sid"]
    auth_token = twilio_creds["project_info"]["auth_token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="The Legion 7 is NOT available yet",
        from_=twilio_creds["project_info"]["phone_number"],
        to="+15852811928",
    )


def message_maybe(twilio_creds):
    account_sid = twilio_creds["project_info"]["account_sid"]
    auth_token = twilio_creds["project_info"]["auth_token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="The Legion 7 may be available now! \n Manually check it at: https://www.lenovo.com/us/en/laptops/legion-laptops/legion-7-series/Legion-7-16ITH6/p/LEN101G0002",
        from_=twilio_creds["project_info"]["phone_number"],
        to="+15852811928",
    )


# %%
if __name__ == "__main__":
    while True:
        chrome_options = set_chrome_options()

        driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)

        add_to_cart = check_cart_button(driver)

        driver.quit()

        twilio_creds = yaml.load(open("secrets.yml"), Loader=yaml.FullLoader)

        if add_to_cart:
            message_avail(twilio_creds)
        else:
            message_unavail(twilio_creds)
        time.sleep(3600)
