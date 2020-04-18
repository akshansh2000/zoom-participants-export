from meeting import Meeting


def main():
    meeting = Meeting()

    meeting.init_driver()
    meeting.try_to_join()
    meeting.get_participants_list()
    meeting.leave_meeting()


if __name__ == "__main__":
    main()
