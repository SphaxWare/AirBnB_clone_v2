#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if successful, None otherwise.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Get the current date and time
        now = datetime.utcnow()

        # Format the date and time to match the desired archive name
        date_string = now.strftime("%Y%m%d%H%M%S")

        # Define the archive path
        archive_path = "versions/web_static_{}.tgz".format(date_string)

        # Create the .tgz archive using tar
        local("tar -cvzf {} web_static".format(archive_path))

        # Check if the archive was created successfully
        if os.path.exists(archive_path):
            return archive_path
        else:
            return None
    except Exception as e:
        print("Error: {}".format(str(e)))
        return None
