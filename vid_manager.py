import google
import mariadb
import datetime
import os
import random
import mariadb
import db

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import db


def get_rand_vids(num: int = 10):
    db.db_connect()
    try:
        statement = "SELECT t1.video_id FROM videos AS t1 JOIN (SELECT video_id FROM videos ORDER BY RAND() LIMIT %s) " \
                    "as t2 ON t1.video_id=t2.video_id"
        db.cur.execute(statement, (num,))
        data = [i[0] for i in db.cur.fetchall()]
        db.db_close()
        return data
    except mariadb.Error as e:
        db.db_close()
        return f"Error adding entry to database {e}"


def download_vids(request):
    db.db_connect()

    returnString = ""

    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=request.args.get("key"))
    except google.auth.exceptions.DefaultCredentialsError as e:
        return f"Error getting credentials"

    def pad_num(num: int, length: int = 3):
        return str(num).zfill(length)

    def rand_num():
        return pad_num(random.randint(1, 999))

    tags = [
        "DSC",
        "IMG",
    ]

    def rand_tag():
        return random.choice(tags)

    for i in range(0, 10):
        search = rand_tag() + " " + rand_num()
        now = datetime.datetime.now(datetime.timezone.utc)
        one_week_ago = now - datetime.timedelta(days=7)
        returnString += "Searching for: " + search + ", published after: " + one_week_ago.isoformat()
        try:
            request = youtube.search().list(
                part="snippet",
                publishedAfter=one_week_ago.isoformat(),
                q=search,
                type="video",
                safeSearch="none",
                maxResults=50,
            )
            response = request.execute()
        except googleapiclient.errors.HttpError as e:
            returnString += f"Error retruning search results"
            break

        if len(response["items"]) <= 0:
            returnString += "No videos found"
            continue

        video_ids = [i["id"]["videoId"] for i in response["items"]]
        # Insert new videos
        for video_id in video_ids:
            try:
                statement = "INSERT INTO videos (video_id, added) VALUES (%s, %s)"
                data = (video_id, now)
                db.cur.execute(statement, data)
                db.conn.commit()
            except mariadb.IntegrityError as e:
                returnString += f"Video already added to database/Other Integrity Error"
            except mariadb.Error as e:
                returnString += f"Error adding entry to database"
                break

    # Remove old entries
    try:
        statement = "DELETE FROM videos WHERE added < NOW() - INTERVAL 30 DAY"
        db.cur.execute(statement)
        db.conn.commit()
    except mariadb.Error as e:
        returnString += f"Error removing entry from database"

    db.db_close()

    return returnString
