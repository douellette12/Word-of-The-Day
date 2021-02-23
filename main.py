from wod import get_wod, get_wod_info, send_email, db_conn, insert_row


def main():
    wod = get_wod()
    short_def, pronunciation, word_type = get_wod_info(wod)
    conn, cursor = db_conn()
    insert_row(conn, cursor, datetime.date.today(), wod, word_type, pronunciation, short_def)
    send_email(wod, word_type, pronunciation, short_def)


if __name__ == "__main__":
    main()
