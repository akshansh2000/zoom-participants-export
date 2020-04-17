from selenium import webdriver
import sys
import json
import csv


class Meeting:
    """
    ? Stores all the meeting data and houses the meeting functions
    """

    def __init__(self):
        super().__init__()

        try:
            with open("config.json", "r") as config:
                config = json.load(config)

                if not {"meeting_id", "password"}.issubset(set(config.keys())):
                    raise Exception()

                self.meeting_id = config["meeting_id"]
                self.password = config["password"]
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
        options = webdriver.ChromeOptions()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)

    def try_to_join(self):
        pass