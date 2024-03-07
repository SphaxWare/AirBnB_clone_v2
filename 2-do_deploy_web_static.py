#!/usr/bin/python3
"""
Fabric script that distributes an archive
to web servers using the function do_deploy.
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.26.241.117', '107.22.144.250']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations are successful, False otherwise.
    """
    if exists(archive_path) is False:
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        archive_filename = archive_path.split('/')[-1]
        release_path = '/data/web_static/releases/{}'.format(
                              archive_filename.split('.')[0])
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Move contents to the proper location
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove unnecessary directories
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Delete the current symbolic link
        current_path = '/data/web_static/current'
        run('rm -rf {}'.format(current_path))

        # Create a new symbolic link
        run('ln -s {} {}'.format(release_path, current_path))

        return True
    except Exception as e:
        print("Error:", e)
        return False
