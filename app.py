
import os
from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Week 4 - Server Replication</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 35px 20px;
            background: linear-gradient(
                135deg,
                #fbd9e9,
                #e6d7fa,
                #d9efff
            );
            color: #222;
            font-family: "Courier New", monospace;
            line-height: 1.6;
        }

        .container {
            max-width: 850px;
            margin: auto;
        }

        h1 {
            text-align: center;
            font-size: 30px;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            margin-top: 0;
            margin-bottom: 30px;
        }

        h2 {
            font-size: 21px;
            margin-top: 0;
            margin-bottom: 15px;
        }

        .card {
            background: rgba(255, 255, 255, 0.82);
            padding: 25px;
            margin-bottom: 18px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(70, 50, 90, 0.08);
        }

        .center {
            text-align: center;
        }

        .counter {
            font-size: 56px;
            font-weight: bold;
            margin: 10px 0;
        }

        .status {
            color: #386a4a;
            font-weight: bold;
        }

        a {
            color: #67499c;
        }

        p {
            margin: 10px 0;
        }

        li {
            margin-bottom: 10px;
        }

        ul {
            padding-left: 25px;
        }

        @media (max-width: 600px) {
            body {
                padding: 20px 12px;
            }

            h1 {
                font-size: 24px;
            }

            .card {
                padding: 20px;
            }
        }
    </style>
</head>

<body>
    <div class="container">

        <h1>Week 4: Server Replication</h1>
        <p class="subtitle">
            Backups and MariaDB Replication
        </p>

        <!-- 1. VISITOR COUNTER -->

        <div class="card center">
            <h2>Visitor Counter</h2>

            {% if visits is not none %}
                <div class="counter">{{ visits }}</div>
                <p class="status">
                    Read-only replica - Server B
                </p>
            {% else %}
                <p>Unable to read the visitor counter.</p>
            {% endif %}

            <p>
                This number comes from Server B's
                local MariaDB database.
            </p>

            <p>
                Refreshing this page does not
                increase the counter.
            </p>
        </div>

        <!-- 2. LINKS -->

        <div class="card">
            <h2>Links</h2>

            <p>
                <a href="http://195.148.23.163/viikko2/">
                    Server A
                </a>
            </p>

            <p>
                <a href="http://86.50.231.16/viikko4/">
                    Server B
                </a>
            </p>

            <p>
                <a href="https://github.com/teeapiet/viikkotehtava4">
                    GitHub
                </a>
            </p>
        </div>

        <!-- 3. HOW I MADE IT -->

        <div class="card">
            <h2>How I Made It</h2>

            <p>
                <strong>Servers:</strong>
                I created Server B from a snapshot
                of Server A using CSC cPouta.
                Both servers have their own IP address.
            </p>

            <p>
                <strong>Storage:</strong>
                Both servers have a 77 GB ext4 filesystem.
                Server A uses 3.3 GB and B uses 3.4 GB.
                The website files on A are in
                /var/www/html/.
            </p>

            <p>
                <strong>Backups:</strong>
                I used Bash, rsync, SSH and cron
                to back up the website files
                from A to B every hour.
                The files are saved in
                /srv/backups/website/
                in folders with timestamps.
                This folder is not public.
            </p>

            <p>
                <strong>Users and permissions:</strong>
                I used the ubuntu user to manage
                the servers. On B, webbackup owns
                the backup folder with permissions 700.
                I used a restricted SSH key
                for transferring the backups.
            </p>

            <p>
                <strong>MariaDB:</strong>
                Server A is the primary database
                and B is the replica.
                I used a separate user called
                week4repl for replication.
                The database connection is restricted
                to the private network.
            </p>

            <p>
                <strong>Read-only:</strong>
                The Week 4 Flask application uses
                week4reader, which only has
                SELECT permission.
                It can read the counter
                but cannot change it.
            </p>

            <p>
                <strong>Why backups are needed:</strong>
                Replication also copies mistakes.
                Backups let me restore older files.
            </p>
        </div>

        <!-- 4. TESTS -->

        <div class="card">
            <h2>Tests</h2>

            <ul>
                <li>
                    <strong>Websites:</strong>
                    Both A and B pages worked.
                </li>

                <li>
                    <strong>Counter:</strong>
                    Opening A's Week 2 page increased
                    the counter. The new number
                    appeared on B.
                </li>

                <li>
                    <strong>Read-only:</strong>
                    Refreshing only B's page
                    did not increase the counter.
                </li>

                <li>
                    <strong>Replication:</strong>
                    I checked the MariaDB status.
                    Slave_IO_Running: Yes and
                    Slave_SQL_Running: Yes.
                </li>

                <li>
                    <strong>Hourly backups:</strong>
                    Three backups were successful
                    on 20.11.2026 at
                    02:00, 03:00 and 04:00 UTC.
                    I checked the log and
                    backup folders on B.
                </li>

                <li>
                    <strong>Restore:</strong>
                    I restored an index.html file
                    to a separate folder on B.
                    The SHA-256 checksums matched.
                </li>

                <li>
                    <strong>Reboot:</strong>
                    I restarted Server B and checked
                    Nginx, MariaDB, the Flask application
                    and database replication.
                    They worked after reboot.
                    I also checked that B received
                    a new hourly backup.
                </li>
            </ul>
        </div>

        <!-- 5. PROBLEM SOLVED -->

        <div class="card">
            <h2>Problem I Solved</h2>

            <p>
                My Week 2 website stopped working
                when I changed the MariaDB
                bind-address setting.
            </p>

            <p>
                I fixed it by allowing both
                local connections and connections
                through the private network.
                After that, the website worked again.
            </p>
        </div>

    </div>
</body>
</html>
"""


def get_visits():
    connection = pymysql.connect(
        host="127.0.0.1",
        user=os.environ["WEEK4_DB_USER"],
        password=os.environ["WEEK4_DB_PASSWORD"],
        database="viikko2db",
        connect_timeout=5,
        read_timeout=5,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT visits FROM visitor_counter WHERE id = 1"
            )
            row = cursor.fetchone()
            return row["visits"] if row else None
    finally:
        connection.close()


@app.route("/")
def index():
    try:
        visits = get_visits()
        return render_template_string(HTML, visits=visits)
    except Exception:
        app.logger.exception("Unable to read replica database")
        return render_template_string(HTML, visits=None), 503

