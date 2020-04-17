from meeting import Meeting


def main():
    meeting = Meeting()

    meeting.init_driver()
    meeting.try_to_join()


if __name__ == "__main__":
    main()
