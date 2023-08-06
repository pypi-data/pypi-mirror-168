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
# Tests for the StreamingFile class

import tempfile
import unittest

from .helpers import LOCALFS_ROOT


class StreamingFileTests(unittest.TestCase):

    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(dir=LOCALFS_ROOT,
                                                    delete=True)
        self.tempfile.write(b'.'*40000)

    def tearDown(self):
        self.tempfile.close()

    def _getTargetClass(self):
        from ..StreamingFile import StreamingFile

        return StreamingFile

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeSimple(self, data=b'data'):
        return self._makeOne('fileid', '', data)

    def test_read(self):
        from ..StreamingFile import BUFFER_SIZE
        from ..StreamingFile import Sdata

        ob = self._makeSimple()

        # small file
        data = b'data'
        ob = self._makeSimple(data=data)
        self.assertEqual(ob.getId(), 'fileid')
        self.assertEqual(ob.data, data)
        self.assertEqual(ob._read_data(file=data), (b'data', 4))

        # Large data
        data = b'.' * BUFFER_SIZE
        ob = self._makeSimple(data=data)
        self.assertEqual(bytes(ob.data), data)
        stream_data, size = ob._read_data(ob.data)
        self.assertIsInstance(stream_data, Sdata)
        self.assertEqual(size, BUFFER_SIZE)
        self.assertEqual(bytes(stream_data), data)

        # Read a single byte
        self.assertEqual(stream_data[BUFFER_SIZE-1], b'.')

        # Try to read beyond chunk size
        self.assertEqual(stream_data[BUFFER_SIZE+1], b'')
