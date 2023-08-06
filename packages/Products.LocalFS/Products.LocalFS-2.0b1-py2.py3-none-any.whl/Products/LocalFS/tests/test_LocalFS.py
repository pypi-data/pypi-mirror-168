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
# Tests for the LocalFS class

import unittest

from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate
from Testing.makerequest import makerequest

from ..LocalFS import _iswin32
from .helpers import ADMIN_USER
from .helpers import LOCALFS_ROOT
from .helpers import FilesystemTestSupport
from .helpers import FunctionalTestCase


class LocalFSTests(unittest.TestCase, FilesystemTestSupport):

    def _getTargetClass(self):
        from ..LocalFS import LocalFS

        return LocalFS

    def _makeOne(self, *args):
        return self._getTargetClass()(*args)

    def _makeSimple(self):
        klass = self._getTargetClass()
        return klass('localfs', 'LocalFS Title', LOCALFS_ROOT, 'user', 'pw')

    def tearDown(self):
        self.cleanup_files()
        super(LocalFSTests, self).tearDown()

    def test_instantiation(self):
        lfs = self._makeSimple()
        self.assertEqual(lfs.getId(), 'localfs')
        self.assertEqual(lfs.title, 'LocalFS Title')
        self.assertEqual(lfs.basepath, LOCALFS_ROOT)

        # Only on Windows
        if _iswin32:
            self.assertEqual(lfs.username, 'user')
            self.assertEqual(lfs._password, 'pw')

    def test_factory(self):
        from OFS.Folder import Folder

        from ..LocalFS import manage_addLocalFS

        folder = Folder('test')

        manage_addLocalFS(folder, 'lfs', 'Local FS', LOCALFS_ROOT)

        self.assertEqual(folder.lfs.getId(), 'lfs')
        self.assertEqual(folder.lfs.title, 'Local FS')
        self.assertEqual(folder.lfs.basepath, LOCALFS_ROOT)

        # Only on Windows
        if _iswin32:
            self.assertEqual(folder.lfs.username, None)
            self.assertEqual(folder.lfs._password, '')

    def test_hasDefaultDocument(self):
        lfs = self._makeSimple()
        lfs.default_document = 'index.html default.html'

        self.assertFalse(lfs.hasDefaultDocument())

        manage_addPageTemplate(lfs, 'index.html', b'<html>')
        self.assertTrue(lfs.hasDefaultDocument())


class LocalFSFunctionalTests(FunctionalTestCase):

    def test_manage_editProperties(self):
        self.login(ADMIN_USER)
        lfs = makerequest(self.folder.localfs)
        req = lfs.REQUEST

        req.form['title'] = 'New Title'
        req.form['basepath'] = '/tmp'
        req.form['username'] = 'user1'
        req.form['password'] = 'pass1'
        req.form['default_document'] = 'my.html index.jsp'
        req.form['catalog'] = 1
        req.form['type_map'] = ['',
                                '.dtml text/html DTMLMethod',
                                '.gif image/gif Image',
                                '.foo Foobar']
        req.form['icon_map'] = ['', 'directory dir.gif', 'foobar foo.gif']
        req.form['file_filter'] = 'None'

        lfs.manage_editProperties(req)
        self.assertEqual(lfs.title, 'New Title')
        self.assertEqual(lfs.basepath, '/tmp')
        self.assertEqual(lfs.default_document, 'my.html index.jsp')
        self.assertEqual(lfs.catalog, 1)
        self.assertEqual(lfs._type_map,
                         {'.dtml': ('text/html', 'DTMLMethod'),
                          '.gif': ('image/gif', 'Image'),
                          '.foo': ('Foobar', '')})
        self.assertEqual(lfs._icon_map,
                         {'directory': 'dir.gif', 'foobar': 'foo.gif'})
        self.assertIsNone(lfs.file_filter)
        self.assertTrue(lfs.isPrincipiaFolderish)
        self.assertTrue(lfs.catalog)

        if _iswin32:  # Only on Windows
            self.assertEqual(lfs.username, 'user1')
            self.assertEqual(lfs._password, 'pass1')
            self.assertEqual(lfs.password, '')  # Gets reset automatically

        # Some special cases
        req.form['file_filter'] = 'myfilter'
        lfs.manage_editProperties(req)
        self.assertEqual(lfs.file_filter, 'myfilter')
        req.form['file_filter'] = ' '
        lfs.manage_editProperties(req)
        self.assertIsNone(lfs.file_filter)

    def test_manage_changeProperties(self):
        self.login(ADMIN_USER)
        lfs = makerequest(self.folder.localfs)

        new_type_map = ['',
                        '.dtml text/html DTMLMethod',
                        '.gif image/gif Image',
                        '.foo Foobar']
        new_icon_map = ['', 'directory dir.gif', 'foobar foo.gif']

        lfs.manage_changeProperties(REQUEST=None,
                                    title='New Title',
                                    basepath='/tmp',
                                    username='user1',
                                    password='pass1',
                                    default_document='my.html index.jsp',
                                    catalog=1,
                                    type_map=new_type_map,
                                    icon_map=new_icon_map,
                                    file_filter='')

        self.assertEqual(lfs.title, 'New Title')
        self.assertEqual(lfs.basepath, '/tmp')
        self.assertEqual(lfs.default_document, 'my.html index.jsp')
        self.assertEqual(lfs.catalog, 1)
        self.assertEqual(lfs._type_map,
                         {'.dtml': ('text/html', 'DTMLMethod'),
                          '.gif': ('image/gif', 'Image'),
                          '.foo': ('Foobar', '')})
        self.assertEqual(lfs._icon_map,
                         {'directory': 'dir.gif', 'foobar': 'foo.gif'})
        self.assertFalse(lfs.file_filter)
        self.assertTrue(lfs.isPrincipiaFolderish)
        self.assertTrue(lfs.catalog)

        if _iswin32:  # Only on Windows
            self.assertEqual(lfs.username, 'user1')
            self.assertEqual(lfs._password, 'pass1')
            self.assertEqual(lfs.password, '')  # Gets reset automatically
