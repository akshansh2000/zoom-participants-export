from meeting import Meeting
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def main():
    meeting = Meeting()

    meeting.init_driver()
    meeting.try_to_join()
    meeting.get_participants_list()
    meeting.leave_meeting()
    meeting.export_data()
