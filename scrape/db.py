import sqlite3


class SQLite:
    def __init__(self, file="application.db"):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        print("Closing the connection")
        self.conn.close()


class NotFoundError(Exception):
    pass


class NotAuthorizedError(Exception):
    pass


def event_lst_to_json(item):
    return {
        "id": item[0],
        "published": item[1],
        "title": item[2],
        "content": item[3],
        "public": bool(item[4]),
    }


def fetch_events():
    try:
        with SQLite("application.db") as cur:

            # execute the query
            cur.execute("SELECT * FROM events where public=1")

            # fetch the data and turn into a dict
            return list(map(event_lst_to_json, cur.fetchall()))
    except Exception as e:
        print(e)
        return []


def fetch_event(id: str):
    try:
        with SQLite("application.db") as cur:

            # execute the query and fetch the data
            cur.execute(f"SELECT * FROM events where id=?", [id])
            result = cur.fetchone()

            # return the result or raise an error
            if result is None:
                raise NotFoundError(f"Unable to find event with id {id}.")

            data = event_lst_to_json(result)
            if not data["public"]:
                raise NotAuthorizedError(
                    f"You are not allowed to access event with id {id}."
                )
            return data
    except sqlite3.OperationalError:
        raise NotFoundError(f"Unable to find event with id {id}.")
