from selenium import webdriver
import sys
import json
import csv
import random
import string


class Meeting:
    """
    * Stores all the meeting data and houses the meeting functions
    """

    def __init__(self):
        """
        * Reads the config file and imports meeting data
        ! Raises exception in case of no file found / invalid file
        """

        super().__init__()

        self.email = "thisisalsounique@tutanota.com"
        self.password = "thisisforTutanota@283"

        try:
            with open("config.json", "r") as config:
                config = json.load(config)

                if not "meeting_url" in config.keys():
                    raise Exception()

                self.meeting_url = config["meeting_url"]
        except:
            print(
                "Please create a valid config file in order to join a meeting.\n"
                "Read the README for more instructions.\n"
                "Exiting..."
            )
            sys.exit(1)

        print(
            "config: valid\n"
            "Trying to join meeting..."
        )

    def init_driver(self):
        """
        * Initialises webdriver and sets options for headless Chrome
        """

        options = webdriver.ChromeOptions()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def try_to_join(self):
        """
        * Tries to join meeting as per meeting data
        ! Raises exception if meeting data invalid
        """

        self.driver.get(self.meeting_url)

        join_from_browser_link = self.driver.find_element_by_xpath(
            "//div[@class='desc24 webclient hideme']//a"
        ).get_attribute("href")

        self.driver.get(join_from_browser_link)

        self.driver.find_element_by_id("email").send_keys(self.email)
        self.driver.find_element_by_id("password").send_keys(self.password)

        self.driver.find_element_by_xpath("//div[@class='signin']").click()

        self.random_hash = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=16,
            )
        )

        self.driver.find_element_by_id("inputname").clear()
        self.driver.find_element_by_id("inputname").send_keys(self.random_hash)
        self.driver.find_element_by_id("joinBtn").click()

        print("Meeting joined!")
