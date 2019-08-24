#! /usr/bin/env python3
"""Synchronize configuration from Mozilla git repository"""
from hashlib import sha256
from os import listdir, makedirs, remove, walk
from os.path import dirname, join, relpath
from shutil import copyfile
from subprocess import run


def update():
    """
    Update configuration.

    Returns:
        dict: Changed files, status.
    """
    root = dirname(__file__)
    src_dir = join(root, 'ssl-config-generator/src')
    dst_dir = join(root, 'ssl_config', '_data')
    files = dict()
    changed = dict()

    # Ensure "mozilla/ssl-config-generator" Git repository is up to date
    run(['git', 'pull'], check=True, capture_output=True, cwd=src_dir)

    # Get latest guidelines
    guidelines = join(src_dir, 'static/guidelines')
    files['guidelines.json'] = join(guidelines, sorted(
        name for name in listdir(guidelines) if name != 'latest.json')[-1])

    # Get configs
    files['configs.js'] = join(src_dir, 'js/configs.js')

    # Get DHE files
    for size in (2048, 4096):
        name = 'ffdhe%d.txt' % size
        files[name] = join(src_dir, 'static', name)

    # Get templates
    templates = join(src_dir, 'templates/partials')
    for name in listdir(templates):
        if name not in ('header.hbs', 'nosupport.hbs'):
            files[join('templates', name)] = join(templates, name)

    # Ensure destination exists
    makedirs(join(dst_dir, 'templates'), exist_ok=True)

    # Load manifest file
    manifest = dict()
    for walk_root, _, walk_files in walk(dst_dir):
        for walk_file in walk_files:
            path = join(walk_root, walk_file)
            with open(path, 'rb') as file:
                manifest[relpath(path, dst_dir)] = sha256(
                    file.read()).hexdigest()

    # Copy new and changed files
    for dst, src in files.items():
        with open(src, 'rb') as src_file:
            src_digest = sha256(src_file.read()).hexdigest()
        dst_digest = manifest.get(dst)

        if dst_digest != src_digest:
            copyfile(src, join(dst_dir, dst))
            changed[dst] = 'created' if not dst_digest else 'updated'

    # Remove absent files
    for dst in set(manifest.keys()) - set(files.keys()):
        remove(join(dst_dir, dst))
        changed[dst] = 'removed'

    return changed


if __name__ == '__main__':
    print('\n'.join(' : '. join((dst, stat)) for dst, stat in update().items()))
