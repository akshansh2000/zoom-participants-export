from app.meeting import Meeting
from flask import Flask, request, render_template, send_file, Response
import datetime

app = Flask(__name__)


@app.route("/")
def landing_page():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def start_export():
    meeting_url = request.form["meeting_url"]
    meeting = Meeting(meeting_url)

    meeting.init_driver()
    meeting.try_to_join()
    meeting.get_participants_list()
    meeting.leave_meeting()

    return Response(
        meeting.export_data(),
        mimetype="text/csv",
        headers={
            "Content-disposition": "attachment; filename=Attendance-{}.csv".format(
                datetime.datetime.now().strftime("%d/%m/%y-%H:%M")
            )
        },
    )
