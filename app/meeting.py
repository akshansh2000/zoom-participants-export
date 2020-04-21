from selenium import webdriver
import sys
import json
import csv
import random
import string
import time
import os


class Meeting:
    """
    * Stores all the meeting data and houses the meeting functions
    """

    def __init__(self, meeting_url):
        """
        * Reads the config file and imports meeting data
        ! Raises exception in case of no file found / invalid file
        """

        super().__init__()

        self.email = "thisisalsounique@tutanota.com"
        self.password = "thisisforTutanota@283"
        self.sleep_time = 12
        self.meeting_url = meeting_url

        self.init_driver()

    def init_driver(self):
        """
        * Initialises webdriver and sets options for headless Chrome
        """

        options = webdriver.ChromeOptions()
        options.headless = True
        options.binary_location = os.environ["GOOGLE_CHROME_BIN"]
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(self.sleep_time)
        self.driver.set_window_size(3840, 2160)

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

        self.partipants_list = [
            name.get_attribute("aria-label").split()
            for name in self.driver.find_elements_by_class_name(
                "item-pos.participants-li"
            )
        ]

        if not self.partipants_list:
            sys.exit(1)

    def leave_meeting(self):
        """
        * Leaves the ongoing meeting and closes the browser window
        """

        self.driver.find_element_by_class_name(
            "footer__leave-btn.ax-outline"
        ).click()
        self.driver.find_element_by_class_name(
            "zm-btn.zm-btn-legacy.zm-btn--primary.zm-btn__outline--blue"
        ).click()

        self.driver.close()

    def export_data(self):
        """
        * Exports data to a 'participants.csv' file
        """

        for idx, row in enumerate(self.partipants_list):
            self.partipants_list[idx] = row[0: row.index("audio") - 1]

        self.partipants_list.sort()

        return_object = ""
        for idx, row in enumerate(self.partipants_list):
            if row[-1] not in ["(Me)", "(Host)"]:
                return_object += " ".join(row) + "\n"

        return return_object
