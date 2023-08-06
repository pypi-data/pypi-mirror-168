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
# Tests for the LocalDirectory class

import os
import tempfile
import unittest

from Acquisition import aq_base
from DateTime.DateTime import DateTime
from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate
from Testing.makerequest import makerequest
from zExceptions import BadRequest

from .helpers import ADMIN_USER
from .helpers import LOCALFS_ROOT
from .helpers import FilesystemTestSupport
from .helpers import FunctionalTestCase


class LocalDirectoryAndFileTests(unittest.TestCase, FilesystemTestSupport):

    def _getTargetClass(self):
        # Using the LocalFS class, it's a subclass of LocalDirectory
        # that does not override any of its methods and is easier to initialize
        from ..LocalFS import LocalFS

        return LocalFS

    def _makeOne(self, *args):
        return self._getTargetClass()(*args)

    def _makeSimple(self):
        klass = self._getTargetClass()
        lfs = klass('localfs', 'LocalFS Title', LOCALFS_ROOT, 'user', 'pw')
        lfs.catalog = True
        return lfs

    def _makeLocalFile(self):
        lfs = self._makeSimple()
        manage_addPageTemplate(lfs, 'test.pt', b'<html>')
        lfs.manage_createDirectory('folder')
        return (lfs, lfs._getfileob('test.pt'), lfs._getfileob('folder'))

    def tearDown(self):
        self.cleanup_files()
        super(LocalDirectoryAndFileTests, self).tearDown()

    def test_instantiation(self):
        lfs = self._makeSimple()
        self.assertEqual(lfs.getId(), 'localfs')
        self.assertEqual(lfs.basepath, LOCALFS_ROOT)
        self.assertIs(aq_base(lfs.root), aq_base(lfs))
        self.assertTrue(lfs._type_map)
        self.assertTrue(lfs._icon_map)
        self.assertIsNone(lfs.file_filter)

    def test___bobo_traverse__PUT(self):
        lfs = self._makeSimple()
        req = {'REQUEST_METHOD': 'PUT'}

        returned = lfs.__bobo_traverse__(req, 'foo')
        self.assertEqual(returned.getId(), 'foo')
        self.assertEqual(returned.title, "LockNull Resource 'foo'")

    def test___getitem__invalid_input(self):
        lfs = self._makeSimple()

        with self.assertRaises(TypeError) as context:
            lfs[None]
        self.assertEqual(str(context.exception), 'index must be a string')

    def test__getpath(self):
        lfs = self._makeSimple()
        self.assertEqual(lfs._getpath('foo'),
                         os.path.join(LOCALFS_ROOT, 'foo'))

    def test__checkId(self):
        lfs = self._makeSimple()

        # No return value signals success
        self.assertIsNone(lfs._checkId('foo'))

        with self.assertRaises(BadRequest) as context:
            lfs._checkId('')
        self.assertIn('No id was specified', str(context.exception))

        with self.assertRaises(BadRequest) as context:
            lfs._checkId('foo&bar')
        self.assertIn('characters illegal in filenames',
                      str(context.exception))

        with self.assertRaises(BadRequest) as context:
            lfs._checkId('_secret')
        self.assertIn('it begins with an underscore', str(context.exception))

        with self.assertRaises(BadRequest) as context:
            lfs._checkId('.gitkeep', allow_dup=False)
        self.assertIn('it is already in use', str(context.exception))
        self.assertIsNone(lfs._checkId('.gitkeep', allow_dup=True))

    def test_PageTemplate(self):
        lfs = self._makeSimple()

        self.assertNotFileExists('test.pt')
        self.assertNotIn('test.pt', lfs.objectIds())

        manage_addPageTemplate(lfs, 'test.pt', '', b'<html>')
        self.assertFileExists('test.pt')
        self.assertIn('test.pt', lfs.objectIds())

        pt_obj = lfs['test.pt']
        self.assertEqual(pt_obj.data, b'<html>')

    def test_cut_copy_paste_rename_delete(self):
        lfs = self._makeSimple()

        lfs.manage_createDirectory('folder')
        manage_addPageTemplate(lfs, 'test.pt', '', b'<html>')
        self.assertIn('test.pt', lfs.objectIds())
        self.assertNotIn('test.pt', lfs.folder.objectIds())

        ref = lfs.manage_copyObjects('test.pt')
        lfs.folder.manage_pasteObjects(ref)
        self.assertIn('test.pt', lfs.objectIds())
        self.assertIn('test.pt', lfs.folder.objectIds())

        self.assertNotIn('renamed_test.pt', lfs.objectIds())
        lfs.manage_renameObject('test.pt', 'renamed_test.pt')
        self.assertNotIn('test.pt', lfs.objectIds())
        self.assertIn('renamed_test.pt', lfs.objectIds())

        self.assertNotIn('renamed_test.pt', lfs.folder.objectIds())
        ref = lfs.manage_cutObjects('renamed_test.pt')
        lfs.folder.manage_pasteObjects(ref)
        self.assertNotIn('renamed_test.pt', lfs.objectIds())
        self.assertIn('renamed_test.pt', lfs.folder.objectIds())

        lfs.folder.manage_delObjects('renamed_test.pt')
        self.assertNotIn('renamed_test.pt', lfs.folder.objectIds())

    def test_objectListMethods(self):
        lfs = self._makeSimple()

        # If the "catalog" variable is false these methods won't work
        lfs.catalog = False
        self.assertFalse(lfs.objectIds())
        self.assertFalse(lfs.objectIds(spec=['Local Directory']))
        self.assertFalse(lfs.objectIds(spec='Local Directory'))
        self.assertFalse(lfs.objectValues())
        self.assertFalse(lfs.objectValues(spec=['Local Directory']))
        self.assertFalse(lfs.objectValues(spec='Local Directory'))
        self.assertFalse(lfs.objectItems())
        self.assertFalse(lfs.objectItems(spec=['Local Directory']))
        self.assertFalse(lfs.objectItems(spec='Local Directory'))

        lfs.catalog = True
        self.assertEqual(lfs.objectIds(), ['.gitkeep'])
        self.assertFalse(lfs.objectIds(spec=['Local Directory']))
        self.assertFalse(lfs.objectIds(spec='Local Directory'))
        self.assertEqual(len(lfs.objectValues()), 1)
        self.assertFalse(lfs.objectValues(spec=['Local Directory']))
        self.assertFalse(lfs.objectValues(spec='Local Directory'))
        self.assertEqual(len(lfs.objectItems()), 1)
        self.assertFalse(lfs.objectItems(spec=['Local Directory']))
        self.assertFalse(lfs.objectItems(spec='Local Directory'))

        lfs.manage_createDirectory('foo')
        self.assertEqual(lfs.objectIds(), ['.gitkeep', 'foo'])
        self.assertEqual(lfs.objectIds(spec=['Local Directory']), ['foo'])
        self.assertEqual(lfs.objectIds(spec='Local Directory'), ['foo'])
        self.assertEqual(len(lfs.objectValues()), 2)
        self.assertEqual(len(lfs.objectValues(spec=['Local Directory'])), 1)
        self.assertEqual(len(lfs.objectValues(spec='Local Directory')), 1)
        self.assertEqual(len(lfs.objectItems()), 2)
        self.assertEqual(len(lfs.objectItems(spec=['Local Directory'])), 1)
        self.assertEqual(len(lfs.objectItems(spec='Local Directory')), 1)

    def test_fileMethods(self):
        lfs = self._makeSimple()

        self.assertEqual(lfs.fileIds(), ['.gitkeep'])
        self.assertEqual(len(lfs.fileValues()), 1)
        self.assertEqual(len(lfs.fileValues(propagate=False)), 1)
        self.assertEqual(len(lfs.fileItems()), 1)
        self.assertEqual(len(lfs.fileItems(propagate=False)), 1)

        self.assertFalse(lfs.fileIds(spec=['Local Directory']))
        self.assertFalse(lfs.fileValues(spec=['Local Directory']))
        self.assertFalse(lfs.fileItems(spec=['Local Directory']))

    def test_defaultDocument(self):
        lfs = self._makeSimple()
        lfs.default_document = 'index.html default.html'

        self.assertIsNone(lfs.defaultDocument())

        manage_addPageTemplate(lfs, 'default.html', b'<html>')
        doc = lfs.defaultDocument()
        self.assertEqual(doc.getId(), 'default.html')

        manage_addPageTemplate(lfs, 'index.html', b'<html>')
        doc = lfs.defaultDocument()
        self.assertEqual(doc.getId(), 'index.html')

    def test_bobobase_modification_time(self):
        lfs = self._makeSimple()
        manage_addPageTemplate(lfs, 'test.pt', '', b'<html>')

        self.assertIsInstance(lfs['test.pt'].bobobase_modification_time(),
                              DateTime)

    # LocalFile-specific tests

    def test_getObject(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertEqual(lof.meta_type, 'Local File')
        self.assertEqual(lof.getObject().meta_type, 'File')

    def test_get_size(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertTrue(lof.get_size())
        self.assertFalse(lod.get_size())

    def test_bobobase_modification_time_localfile(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertIsInstance(lof.bobobase_modification_time(), DateTime)

    def test__getURL(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertEqual(lof._getURL('Local File'), 'test.pt')
        self.assertEqual(lod._getURL('Local File'), 'folder?spec=Local%20File')
        self.assertEqual(
            lod._getURL(['Local File', 'Local Directory']),
            'folder?spec:list=Local%20File&spec:list=Local%20Directory')

    def test__getType(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertEqual(lof._getType(), 'text/html')
        self.assertEqual(lod._getType(), 'directory')

    def test__getIcon(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertEqual(lof._getIcon(), 'misc_/LocalFS/layout.gif')
        self.assertEqual(lod._getIcon(), 'misc_/LocalFS/dir.gif')

        # an unknown item
        lof.type = 'unknown'
        self.assertEqual(lof._getIcon(), 'misc_/LocalFS/generic.gif')

    def test__getDisplaySize(self):
        lfs, lof, lod = self._makeLocalFile()

        self.assertIn('bytes', lof._getDisplaySize())
        self.assertEqual(lod._getDisplaySize(), '-----')

        # large size
        lof.size = 8543
        self.assertEqual(lof._getDisplaySize(), '8.3 kB')

        lof.size = 678358764
        self.assertEqual(lof._getDisplaySize(), '646.9 MB')

        # invalid size
        lof.size = -1
        self.assertEqual(lof._getDisplaySize(), '(unknown)')


class LocalDirectoryFunctionalTests(FunctionalTestCase, FilesystemTestSupport):

    def tearDown(self):
        self.cleanup_files()
        super(LocalDirectoryFunctionalTests, self).tearDown()

    def test_manage_upload(self):
        self.login(ADMIN_USER)
        lfs = makerequest(self.folder.localfs)
        manage_addPageTemplate(lfs, 'test.pt', '', b'<html>')

        # existing file
        with tempfile.NamedTemporaryFile(dir=LOCALFS_ROOT, delete=True) as fp:
            fp.write(b'<html></html>')
            fp.seek(0)
            # existing file
            lfs.manage_upload(fp, 'test.pt')
        self.assertEqual(lfs['test.pt'].data, b'<html></html>')

        # new file
        self.assertNotIn('new_test.pt', lfs.objectIds())
        with tempfile.NamedTemporaryFile(dir=LOCALFS_ROOT, delete=True) as fp:
            fp.write(b'<html></html>')
            fp.seek(0)
            lfs.manage_upload(fp, 'new_test.pt')
        self.assertIn('new_test.pt', lfs.objectIds())
        self.assertEqual(lfs['new_test.pt'].data, b'<html></html>')

    def test_Directory(self):
        self.login(ADMIN_USER)
        lfs = makerequest(self.folder.localfs)
        req = lfs.REQUEST

        self.assertNotFolderExists('foo')
        self.assertIsNone(lfs.__bobo_traverse__(req, 'foo'))
        with self.assertRaises(AttributeError) as context:
            getattr(lfs, 'foo')
        self.assertIn('foo', str(context.exception))
        with self.assertRaises(AttributeError) as context:  # MISBEHAVIOR!
            lfs['foo']
        self.assertEqual(str(context.exception), 'foo')
        self.assertFalse(lfs.objectIds(spec=['Local Directory']))

        returned = lfs.manage_createDirectory('foo', REQUEST=req)
        self.assertIn('Directory foo has been created', returned)
        self.assertFolderExists('foo')
        self.assertIn('foo', lfs.objectIds())
        self.assertEqual(lfs.objectIds(spec=['Local Directory']), ['foo'])

        # Calling manage_createDirectory again won't do anything
        returned = lfs.manage_createDirectory('foo', REQUEST=req)
        self.assertIn('Directory foo already exists', returned)

        lfs.manage_delObjects(ids=['foo'])
        self.assertNotFolderExists('foo')
        self.assertFalse(lfs.objectIds(spec=['Local Directory']))
