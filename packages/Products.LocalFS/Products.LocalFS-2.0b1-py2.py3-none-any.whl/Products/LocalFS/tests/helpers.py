##############################################################################
#
# Copyright (c) 1999 Jonothan Farr and contributors
# All rights reserved. Written by Jonothan Farr <jfarr@speakeasy.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission
#
# Disclaimer
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# In accordance with the license provided for by the software upon
# which some of the source code has been derived or used, the following
# acknowledgement is hereby provided:
#
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
#
##############################################################################
# Helper functions and definitions for LocalFS tests

import os
import shutil

from Testing.ZopeTestCase import ZopeTestCase

from ..LocalFS import manage_addLocalFS


TESTS_PATH = os.path.dirname(os.path.abspath(__file__))
LOCALFS_ROOT = os.path.join(TESTS_PATH, 'files')
ADMIN_USER = 'admin'


class FunctionalTestCase(ZopeTestCase):

    _setup_fixture = True

    def _setup(self):
        super(FunctionalTestCase, self)._setup()

        # Add an admin user
        uf = self.folder.acl_users
        uf.userFolderAddUser(ADMIN_USER, 'foobar', ['Manager'], [])

        # Add a LocalFS instance
        manage_addLocalFS(self.folder,
                          'localfs',
                          'LocalFS Title',
                          LOCALFS_ROOT)

        # Make sure the objectXXX methods work
        self.folder.localfs.tree_view = True
        self.folder.localfs.catalog = True


class FilesystemTestSupport:
    """ Mix-in with utility methods for manipulating filesystem files """

    def cleanup_files(self):
        filenames = self.list_folder()
        filenames.remove('.gitkeep')

        for filename in filenames:
            path = os.path.join(LOCALFS_ROOT, filename)
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    def list_folder(self, subpath=None):
        if subpath:
            path = os.path.join(LOCALFS_ROOT, subpath)
        else:
            path = LOCALFS_ROOT
        return os.listdir(path)

    def assertFolderExists(self, subpath):
        path = os.path.join(LOCALFS_ROOT, subpath)
        if not os.path.isdir(path):
            raise AssertionError('Folder does not exist: %s' % path)

    def assertNotFolderExists(self, subpath):
        path = os.path.join(LOCALFS_ROOT, subpath)
        if os.path.isdir(path):
            raise AssertionError('Folder exists: %s' % path)

    def assertFileExists(self, subpath):
        path = os.path.join(LOCALFS_ROOT, subpath)
        if not os.path.isfile(path):
            raise AssertionError('File does not exist: %s' % path)

    def assertNotFileExists(self, subpath):
        path = os.path.join(LOCALFS_ROOT, subpath)
        if os.path.isfile(path):
            raise AssertionError('File exists: %s' % path)

    def read_file(self, subpath):
        with open(os.path.join(LOCALFS_ROOT, subpath), 'rb') as fp:
            return fp.read()


class FakeContent:

    basepath = ''
    _local_path = ''
