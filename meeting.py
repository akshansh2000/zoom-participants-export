from selenium import webdriver
import sys
import json
import csv
import random
import string
import time


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

                if not {"meeting_url", "sleep_time"}.issubset(set(config.keys())):
                    raise Exception()

                self.meeting_url = config["meeting_url"]
                self.sleep_time = config["sleep_time"]
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

        print(
            "Meeting joined!\n"
            "Collecting participants..."
        )

    def get_participants_list(self):
        """
        * Collects participants and exports them to a CSV
        ! Might raise an exception if the internet is slow
        """

        # * Sleep for a while in order to wait for the partipants list to load
        # ? Any better alternative
        time.sleep(self.sleep_time)

        self.driver.find_elements_by_class_name(
            "footer-button__button.ax-outline"
        )[0].click()

        partipants_list = [name.text for name in self.driver.find_elements_by_class_name(
            "participants-item__display-name"
        ) if name.text != self.random_hash]

        if not partipants_list:
            print(
                "Something went wrong. Perhaps your internet is slow?\n"
                "Try increasing the sleep time in the config.\n"
                "Read the README for more instructions.\n"
                "Exiting..."
            )
            sys.exit(1)

        print(
            "Partipants collected!\n"
            "Leaving meeting..."
        )
