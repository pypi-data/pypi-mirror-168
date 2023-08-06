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
# Tests for the utility functions

import os
import tempfile
import unittest

from .helpers import LOCALFS_ROOT
from .helpers import FakeContent


class UtilsTests(unittest.TestCase):

    def test__get_content_type(self):
        from ..LocalFS import _types
        from ..utils import _get_content_type

        # Valid input
        self.assertEqual(_get_content_type('.gif', _types),
                         ('image/gif', 'Image'))
        self.assertEqual(_get_content_type('.GIF', _types),
                         ('image/gif', 'Image'))

        # Invalid input or unknown type
        self.assertEqual(_get_content_type('.foo', _types), (None, None))
        self.assertEqual(_get_content_type(None, _types), (None, None))

    def test_set_content_type(self):
        from ..utils import _set_content_type

        data = b''
        ob = FakeContent()
        _set_content_type(ob, 'image/gif', data)
        self.assertEqual(ob.content_type, 'image/gif')

        # If the object already has a content_type attribute and a non-true
        # value is passed in then it will not be changed
        _set_content_type(ob, None, data)
        self.assertEqual(ob.content_type, 'image/gif')
        _set_content_type(ob, '', data)
        self.assertEqual(ob.content_type, 'image/gif')

        # (Weird) special handling for text/html
        _set_content_type(ob, 'text/html', data)
        self.assertEqual(ob.content_type, 'text/html')
        _set_content_type(ob, None, data)
        self.assertEqual(ob.content_type, 'text/plain')

        data = '<html>...'
        _set_content_type(ob, 'text/html', data)
        self.assertEqual(ob.content_type, 'text/html')
        _set_content_type(ob, None, data)
        self.assertEqual(ob.content_type, 'text/html')

        data = '<!doctype html>...'
        _set_content_type(ob, 'text/html', data)
        self.assertEqual(ob.content_type, 'text/html')
        _set_content_type(ob, None, data)
        self.assertEqual(ob.content_type, 'text/html')

    def test__list2typemap(self):
        from ..utils import _list2typemap

        t_list = ['',
                  '.dtml text/html DTMLMethod',
                  '.gif image/gif Image',
                  '.foo Foobar']
        self.assertEqual(_list2typemap(t_list),
                         {'.dtml': ('text/html', 'DTMLMethod'),
                          '.gif': ('image/gif', 'Image'),
                          '.foo': ('Foobar', '')})

        # Invalid input
        self.assertIsNone(_list2typemap(None))
        self.assertIsNone(_list2typemap(''))
        self.assertIsNone(_list2typemap([]))

    def test__typemap2list(self):
        from ..LocalFS import _types
        from ..utils import _typemap2list

        t_list = _typemap2list(_types)
        self.assertIsInstance(t_list, list)
        self.assertEqual(set(_types.keys()),
                         set([x.split()[0] for x in t_list]))

        t_map = {'.dtml': ('text/html', 'DTMLMethod'),
                 '.foo': 'Foobar'}
        self.assertEqual(_typemap2list(t_map),
                         ['.dtml text/html DTMLMethod', '.foo Foobar'])

    def test__list2iconmap(self):
        from ..utils import _list2iconmap

        i_list = ['', 'directory dir.gif', 'application binary.gif']
        self.assertEqual(_list2iconmap(i_list),
                         {'directory': 'dir.gif', 'application': 'binary.gif'})

        # Invalid input
        self.assertIsNone(_list2iconmap(None))
        self.assertIsNone(_list2iconmap(''))
        self.assertIsNone(_list2iconmap([]))
        with self.assertRaises(ValueError):
            _list2iconmap(['invalid'])

    def test__iconmap2list(self):
        from ..LocalFS import _icons
        from ..utils import _iconmap2list

        i_list = _iconmap2list(_icons)
        self.assertIsInstance(i_list, list)
        self.assertEqual(set(_icons.keys()),
                         set([x.split()[0] for x in i_list]))

    def test__set_timestamp(self):
        from ..utils import _set_timestamp

        ob = FakeContent()
        with tempfile.NamedTemporaryFile(dir=LOCALFS_ROOT) as fp:
            _set_timestamp(ob, fp.name)
        self.assertIsInstance(ob._p_serial, bytes)

    def test_valid_id(self):
        from ..utils import valid_id

        self.assertFalse(valid_id(os.curdir))
        self.assertFalse(valid_id(os.pardir))
        self.assertFalse(valid_id('_secret'))
        self.assertTrue(valid_id('foobar'))

    def test_sanity_check(self):
        from ..utils import sanity_check

        copy_source = FakeContent()
        copy_source._local_path = os.path.join(LOCALFS_ROOT, 'foo.txt')
        copy_target = FakeContent()

        copy_target.basepath = os.path.join(LOCALFS_ROOT, 'bar.txt')
        self.assertTrue(sanity_check(copy_target, copy_source))

        copy_target.basepath = os.path.join(LOCALFS_ROOT, 'foo.txt')
        self.assertFalse(sanity_check(copy_target, copy_source))
