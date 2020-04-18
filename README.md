# Zoom Participants Export

A Python script which exports the names of participants from a Zoom meeting, given the meeting URL.

# Prerequisites

- Make sure to have a valid [Chrome WebDriver](https://chromedriver.chromium.org/) installed.
- Make sure to have [selenium](https://pypi.org/project/selenium/) installed.

# Instructions

- Clone and navigate into the repository directory:

```bash
git clone https://github.com/akshansh2000/zoom-participants-export.git
cd zoom-participants-export/
```

- Create a `config.json` file containing your **Zoom meeting URL** and a **sleep time**. A sample `config.json` is given:

```json
{
  "meeting_url": "<Meeting URL goes here>",
  "sleep_time": 10
}
```

_Note: Do not worry about the `sleep_time` initially. Try running the script first. If it shows a `sleep_time error`, it might mean that your internet connection is slow. Try increasing the `sleep_time` by a couple of seconds, then._

A `config.json` file has been included in the repository for testing. Feel free to edit it.

- Run the script:

```bash
python3 main.py
```

### If everything went perfectly, an output file should now be available as `participants.csv` in the same directory.
