#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net fabfile"""

from datetime import datetime
from fabric.api import *

from os import environ
LOCAL_DATABASE_NAME = "jmoiron"

env.hosts = ["jmoiron.net"]

@task
def fetch_db(db="jmoiron_net"):
    """Fetch db from the server."""
    # TODO: this fetches the old db, make it fetch the new one
    timestamp = datetime.now().isoformat().split("T")[0]
    path = "/tmp/%s.%s.sql" % (db, timestamp)
    cmd = "pg_dump -U jmoiron -dCE utf8 %s -f \"%s\"" % (db, path)
    run(cmd)
    run("gzip \"%s\"" % path)
    get(path + ".gz", "./")
    run("rm \"%s.gz\"" % path)
    # remove it if it already exists
    local("rm -f %s.%s.sql" % (db, timestamp))
    local("gzip -d %s.%s.sql.gz" % (db, timestamp))
    if environ["OS"] == "OSX":
        # OSX has a shitty bsd sed which works differently
        local("sed -i '' 's/^CREATE DATABASE/-- CREATE DATABASE/' %s.%s.sql" % (db, timestamp))
        local("sed -i '' 's/^ALTER DATABASE/-- ALTER DATABASE/' %s.%s.sql" % (db, timestamp))
        local(r"sed -i '' 's/^\\connect/-- \\connect/' %s.%s.sql" % (db, timestamp))
    else:
        local("sed -i 's/^CREATE DATABASE/-- CREATE DATABASE/' %s.%s.sql" % (db, timestamp))
        local("sed -i 's/^ALTER DATABASE/-- ALTER DATABASE/' %s.%s.sql" % (db, timestamp))
        local(r"sed -i 's/^\\connect/-- \\connect/' %s.%s.sql" % (db, timestamp))



