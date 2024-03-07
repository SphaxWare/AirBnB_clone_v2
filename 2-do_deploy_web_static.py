#!/usr/bin/python3
"""
Fabric script that distributes an archive
to web servers using the function do_deploy.
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.26.241.117', '107.22.144.250']


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    """
    if exists(archive_path) is False:
        return False
    arch_file = archive_path.split('/')[-1]
    arch_name = arch_file.split('.')[0]

    # First: Upload the archive to the server
    if put(archive_path, '/tmp/').failed:
        return False

    # Second: Uncompress the archive
    if run('mkdir -p /data/web_static/releases/{}'.format(arch_name)).failed:
        return False

    if run('tar -xvzf /tmp/{} -C /data/web_static/releases/{}'.
            format(arch_file, arch_name)).failed:
        return False

    # Third: Delete remote archive & recreate symbolic link
    if run('rm /tmp/{}'.format(arch_file)).failed:
        return False

    if run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(
                arch_name, arch_name)).failed:
                return False

    if run('rm -rf /data/web_static/releases/{}/web_static'.
            format(arch_name)).failed:
        return False

    if run('rm -rf /data/web_static/current').failed:
        return False

    if run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'.
            format(arch_name)).failed:
        return False

    return True
