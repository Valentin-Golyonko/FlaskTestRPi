from sqlite3 import connect, Error, DatabaseError

from .color_log.log_color import log_verbose, log_info, log_error


def create_db_twee_table(twee_data):
    log_verbose("create_db_twee_table()")

    db = 0
    try:
        db = connect("data/flask_test.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS twee"
                       " (created_at String,"
                       " user_name String,"
                       " full_text String,"
                       " media_url String,"
                       " user_image_url String);")

        db.commit()

        cursor.executemany("INSERT INTO twee"
                           " (created_at, user_name, full_text, media_url, user_image_url)"
                           " VALUES (?, ?, ?, ?, ?)", twee_data)

        db.commit()
        db.close()
        log_info("\tCREATE twee table OK")

        return True

    except Error as er:
        log_error("\tsqlite3.Error: \n%s" % er)
    finally:
        db.close()


def open_db_twee_table():
    log_verbose("open_db_twee_table()")

    twee_from_db = 0
    db = 0
    try:
        db = connect("data/flask_test.sqlite")
        cursor = db.cursor()

        twee_from_db = cursor.execute("SELECT * FROM twee ORDER BY created_at DESC LIMIT 20").fetchall()
        log_info("\tlst twee time: " + str(twee_from_db[0][0]))  # test print

        # for row in cursor.execute("SELECT * FROM twee"):  # test print
        #     Logs.log_info("\trow: %s" % str(row))

        db.close()

        if twee_from_db:
            log_info("\tOpen twee table - OK")
        else:
            log_error("\tError in - open_db_twee_table()\ntwee_from_db = None")

    except DatabaseError as err:
        log_error("\tsqlite3.DatabaseError: \n%s" % err)
    finally:
        db.close()

    return twee_from_db


if __name__ == '__main__':
    # create_db_twee_table()

    open_db_twee_table()
