#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to make the extension.
"""

import os
import re
import logging
import argparse
import psutil
import tempfile
from shutil import copytree, ignore_patterns, make_archive
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE, run

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Extension factory')

VERSION = "0.0.1"

EXTENSION_NAME= "footswitch_monitor"
FILENAME = f'{EXTENSION_NAME}.oxt'
EXTENSION_DIRECTORY = f'extension/{VERSION}'
USER_DIRECTORY = os.path.expanduser('~')
MACROS_DIRECTORY = 'macros'


class Extension:
    def __init__(self):
        self.filename = FILENAME
        self.version = VERSION
        self.install_path = self._get_install_path()

    def make(self):
        self.update_description_version()
        self.zip_files()

    def update_description_version(self):
        """XML description file is updated with the
        correct version number."""
        description_file = 'src/description.xml'
        tree = ET.parse(description_file)
        root = tree.getroot()
        # we suppose position of version node won't change
        root[1].attrib['value'] = self.version
        ET.register_namespace("", "http://openoffice.org/extensions/description/2006")
        tree.write(description_file)

    def zip_files(self):
        extension_path = os.path.join(EXTENSION_DIRECTORY, self.filename)
        with tempfile.TemporaryDirectory() as tmpdirname:
            src = os.path.join(tmpdirname, 'src')
            self.create_tmp_src(src)
            make_archive(extension_path, 'zip', src)
            os.rename(extension_path + '.zip', extension_path)

    def create_tmp_src(self, temp_dir):
        copytree('src/', temp_dir, ignore=ignore_patterns(
            '*.pyc', '*.py~', '__pycache__', '.idea', ))

    def _get_install_path(self):
        sp = Popen(['unopkg', 'list'], stdout=PIPE)
        output, error = sp.communicate()
        search = re.compile('uno\_packages\/(.*)\.tmp\_\/footswitch')
        res = search.search(output.decode('utf-8'))
        if res:
            cache_dir = res.group(1) + ".tmp_"
            return os.path.join(
                USER_DIRECTORY,
                '.config/libreoffice/4/user/uno_packages/cache/uno_packages',
                cache_dir,
                self.filename
            )

    @property
    def is_installed(self):
        return bool(self.install_path)

    def install(self):
        if self.is_installed:
            logger.debug(" Extension was previously installed.")
            self.restore_python_dir()
            self.uninstall()
        self._install()
        self.install_path = self._get_install_path()

    def _install(self):
        extension_path = f'./{EXTENSION_DIRECTORY}/{FILENAME}'
        logger.debug(f' Extension path: {extension_path}')
        run(['unopkg', 'add', '-f', extension_path])

    def uninstall(self):
        run(['unopkg', 'remove', FILENAME])

    def set_development_env(self):
        if self.is_installed:
            self.symlink_python_dir()
        else:
            logger.debug(f"Extension is not installed. Can't perform dev env.")

    def open_install_path(self):
        if self.install_path:
            Popen(['nautilus', self.install_path])
        else:
            logger.debug(" Install path can't be None")

    def symlink_python_dir(self):
        if not os.path.exists(self.python_path + '_'):
            self.rename_python_dir()
            python_dev = os.path.join(os.getcwd(), 'src', MACROS_DIRECTORY)
            os.symlink(python_dev, self.python_path )

    def rename_python_dir(self):
        os.rename(self.python_path, self.python_path + '_')

    def restore_python_dir(self):
        if os.path.exists(self.python_path + '_'):
            os.remove(self.python_path)
            os.rename(self.python_path + '_', self.python_path)

    @property
    def python_path(self):
        return os.path.join(self.install_path, MACROS_DIRECTORY)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open', help="Open installation directory",
                        action='store_true')
    parser.add_argument('-m', '--make', help="Make extension",
                        action='store_true')
    parser.add_argument('-i', '--install', help="Install extension",
                        action='store_true')
    parser.add_argument('-u', '--uninstall', help="Uninstall extension",
                        action='store_true')
    parser.add_argument('-d', '--dev', help="Set dev shortcuts",
                        action='store_true')
    parser.add_argument('-id', '--install-dev',
                        help="Install and set dev shortcuts",
                        action='store_true')
    args = parser.parse_args()

    # if 'soffice.bin' not in (i.name() for i in psutil.process_iter()):
    #     logger.error(' LibreOffice is not started. Operation aborted.')
    #     exit()
    restart_needed = False

    ext = Extension()
    if args.open:
        ext.open_install_path()
    if args.make:
        ext.make()
    if args.install:
        logger.debug('Install initiated.')
        ext.make()
        ext.install()
        restart_needed = True
    if args.uninstall:
        ext.uninstall()
        restart_needed = True
    if args.dev:
        ext.set_development_env()
    if args.install_dev:
        ext.make()
        ext.install()
        ext.set_development_env()

    if restart_needed:
        logger.info('Libreoffice should be restarted now.')

if __name__ == '__main__':
    main()
