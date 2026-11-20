
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
            padding: 40px 20px;
            background: linear-gradient(
                135deg,
                #fbd9e9,
                #e6d7fa,
                #d9efff
            );
            color: #222;
            font-family: "Courier New", monospace;
        }

        .container {
            max-width: 850px;
            margin: auto;
        }

        h1, h2 {
            text-align: center;
        }

        h1 {
            font-size: 32px;
        }

        .subtitle {
            text-align: center;
            margin-bottom: 30px;
        }

        .card {
            background: rgba(255, 255, 255, 0.8);
            padding: 25px;
            margin: 20px 0;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(70, 50, 90, 0.08);
        }

        .counter {
            font-size: 56px;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
        }

        .center {
            text-align: center;
        }

        .label {
            font-weight: bold;
        }

        a {
            color: #67499c;
        }

        .status {
            font-weight: bold;
            color: #386a4a;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Week 4: Server Replication</h1>
        <p class="subtitle">
            Backups & Database Replication
        </p>

        <div class="card center">
            <h2>Replicated Visitor Counter</h2>

            {% if visits is not none %}
                <div class="counter">{{ visits }}</div>
                <p class="status">Read-only replica</p>
            {% else %}
                <p>Unable to read the visitor counter.</p>
            {% endif %}

            <p>
                This value comes from Server B's
                local MariaDB database.
            </p>
            <p>
                Reloading this page does not
                increase the counter.
            </p>
        </div>

        <div class="card">
            <h2>Server Information</h2>
            <p><span class="label">Server A:</span>
                Primary database
            </p>
            <p><span class="label">Server B:</span>
                Read-only replica
            </p>
            <p><span class="label">Database:</span>
                MariaDB
            </p>
            <p><span class="label">Backups:</span>
                Hourly using rsync and cron
            </p>
        </div>

        <div class="card">
            <h2>Links</h2>
            <p>
                <a href="http://195.148.23.163/viikko2/">
                    Server A - Visitor Counter
                </a>
            </p>
            <p>
                Server B - This read-only page
            </p>
        </div>

        <div class="card">
            <h2>Documentation</h2>
            <p>
                Server B was created from a snapshot
                of Server A using CSC cPouta.
            </p>
            <p>
                Website files are backed up from
                Server A to Server B every hour.
            </p>
            <p>
                MariaDB replication continuously
                copies database changes from
                Server A to Server B.
            </p>
            <p>
                The application uses a database
                account with SELECT-only access.
            </p>
            <p>
                Detailed tests and GitHub source
                code will be added here.
            </p>
        </div>
    </div>

<div class="container">

    <div class="card">
        <h2>Technical Implementation</h2>
        <p><strong>Server A:</strong> Primary Ubuntu server,
           running the original visitor counter.</p>
        <p><strong>Server B:</strong> Ubuntu server cloned
           from a CSC cPouta snapshot.</p>
        <p><strong>Backups:</strong> Website files are copied
           hourly from A to B using Bash, rsync, SSH and cron.</p>
        <p><strong>Backup location:</strong>
           /srv/backups/website/ on Server B.</p>
        <p><strong>Database:</strong> MariaDB primary-replica
           replication using binary logs.</p>
        <p><strong>Read-only access:</strong>
           The Week 4 Flask application uses a database
           account with SELECT-only permission.</p>
    </div>

    <div class="card">
        <h2>Commands Used</h2>
        <p><strong>crontab -l</strong> displays the
           hourly backup schedule.</p>
        <p><strong>rsync -a</strong> copies website files
           over an encrypted SSH connection.</p>
        <p><strong>SHOW REPLICA STATUS</strong> checks
           the MariaDB replication status.</p>
        <p><strong>sha256sum</strong> verifies that a
           restored file matches its backup.</p>
        <p><strong>systemctl is-active</strong> checks
           whether services are running.</p>
    </div>

    <div class="card">
        <h2>Testing</h2>
        <p>The following tests were performed:</p>
        <ul>
            <li>Hourly backup scheduling and backup log checks</li>
            <li>Restoring a website file from a backup</li>
            <li>Comparing SHA-256 checksums</li>
            <li>Testing database replication from A to B</li>
            <li>Verifying that B does not increment the counter</li>
            <li>Checking services and replication after reboot</li>
        </ul>
<h3>Hourly Backup Test</h3>
<p>I checked the backup log on Server A.</p>
<p>Three automatic backups were successful:</p>
<ul>
    <li>20.11.2026 at 02:00 UTC</li>
    <li>20.11.2026 at 03:00 UTC</li>
    <li>20.11.2026 at 04:00 UTC</li>
</ul>
<p>
    All three showed SUCCESS in the log.
    I also checked that the backup folders
    were saved on Server B.
</p>
    </div>

    <div class="card">
        <h2>Problem Solved</h2>
        <p>
            During database replication setup, the Week 2
            application temporarily lost its database
            connection. MariaDB was configured to listen
            on the private network address, but the local
            application also needed access through
            127.0.0.1.
        </p>
        <p>
            I solved this by updating the bind-address
            configuration to support both local and
            private-network connections.
        </p>
    </div>

    <div class="card">
        <h2>GitHub Repository</h2>
        <p>
            <a href="https://github.com/teeapiet/viikkotehtava4">
                Week 4 - Source Code and Documentation
            </a>
        </p>
    </div>
<div class="card">
    <h2>Storage Layout</h2>

    <p>
        Both servers have a 77 GB root
        filesystem using ext4.
    </p>

    <p>
        Server A: 3.3 GB used (5%).
    </p>

    <p>
        Server B: 3.4 GB used (5%).
    </p>

    <p>
        Server A stores the website files
        in /var/www/html/.
    </p>

    <p>
        Server B stores the backups in
        /srv/backups/website/.
    </p>

    <p>
        Backups are stored outside the public
        website directory.
    </p>
</div>
<div class="card">
    <h2>Users and Permissions</h2>

    <p>
        I used the ubuntu user to manage
        both servers.
    </p>

    <p>
        I created a Linux user called webbackup
        on Server B for the website backups.
    </p>

    <p>
        The backup folder belongs to webbackup
        and has permissions 700.
    </p>

    <p>
        I used SSH keys to transfer files
        safely between the servers.
    </p>

    <p>
        I created a MariaDB replication user
        called week4repl.
    </p>

    <p>
        The replication connection is allowed
        only from Server B's private IP address.
    </p>

    <p>
        The Week 4 application uses the
        week4reader database user.
        It only has SELECT permission.
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

