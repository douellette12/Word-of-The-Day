from wod import get_wod, get_wod_info, send_email


def main():
    wod = get_wod()
    short_def, pronunciation, word_type = get_wod_info(wod)
    send_email(wod, word_type, pronunciation, short_def)


if __name__ == "__main__":
    main()
