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
"""Local File System product"""
__version__ = '1.12'
__doc__ = """Local File System product"""

import glob
import marshal  # sbk
import os
import stat

import six
from six.moves.urllib.parse import quote

import AccessControl
import Acquisition
import App
import OFS
import Persistence
from AccessControl.SecurityManagement import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.Common import absattr
from App.FactoryDispatcher import ProductDispatcher
from App.special_dtml import HTMLFile
from DateTime import DateTime
from OFS.CopySupport import CopyError
from OFS.CopySupport import _cb_decode
from OFS.CopySupport import _cb_encode
from OFS.role import RoleManager
from webdav.NullResource import LockNullResource
from zExceptions import BadRequest
from zExceptions import Forbidden
from zExceptions import NotFound
from zExceptions import Unauthorized

from .exceptions import DeleteError
from .exceptions import RenameError
from .exceptions import UploadError
from .utils import HAVE_FTP
from .utils import _create_ob
from .utils import _get_content_type
from .utils import _iconmap2list
from .utils import _iswin32
from .utils import _list2iconmap
from .utils import _list2typemap
from .utils import _marker
from .utils import _save_ob
from .utils import _set_content_type
from .utils import _set_timestamp
from .utils import _test_read
from .utils import _typemap2list
from .utils import _unknown
from .utils import bad_id
from .utils import sanity_check
from .utils import unc_expr
from .utils import valid_id


if (_iswin32):
    try:
        import win32wnet
    except ImportError:
        pass


############################################################################
# The process of determining the content-type involves the following steps.
# This same process is used in LocalDirectory._getOb and LocalFile._getType.
#
# 1. Call _get_content_type which tries to look up the content-type
#    in the type map.
# 2. If that fails then create a file object with the first _test_read
#    bytes of data and see what content-type Zope determines.
#    If we can't read the file then assign 'application/octet-stream'.
# 3. If we found a content-type then assign it to the object in
#    _set_content_type. This overrides the type assigned by Zope.
# 4. Try to see if Zope has assigned 'text/html' to a file that it
#    shouldn't have and change the type back to 'text/plain'. This
#    also happens in _set_content_type.
############################################################################


_types = {
    '.py': ('text/x-python', 'PythonScript'),
    '.html': ('text/html', 'DTMLDocument'),
    '.htm': ('text/html', 'DTMLDocument'),
    '.dtml': ('text/html', 'DTMLMethod'),
    '.gif': ('image/gif', 'Image'),
    '.jpg': ('image/jpeg', 'Image'),
    '.jpeg': ('image/jpeg', 'Image'),
    '.png': ('image/png', 'Image'),
    '.pt': ('text/html', 'PageTemplate'),  # ***SmileyChris
    '.zpt': ('text/html', 'PageTemplate'),  # ***SmileyChris
    '.ra': ('audio/vnd.rn-realaudio', ''),
    '.rv': ('video/vnd.rn-realvideo', ''),
    '.rm': ('application/vnd.rn-realmedia', ''),
    '.rp': ('image/vnd.rn-realpix', ''),
    '.rt': ('text/vnd.rn-realtext', ''),
    '.smi': ('application/smil', ''),
    '.swf': ('application/x-shockwave-flash', ''),
    '.stx': (
        'text/html',
        'Products.StructuredDocument.StructuredDocument.StructuredDocument'),
    '.xml': ('text/xml', 'LocalFS.Factory.XMLDocumentFactory'),
}

_icons = {
    'directory': 'dir.gif',
    'application': 'binary.gif',
    'application/mac-binhex40': 'compressed.gif',
    'application/octet-stream': 'binary.gif',
    'application/pdf': 'layout.gif',
    'application/postscript': 'ps.gif',
    'application/smil': 'layout.gif',
    'application/vnd.rn-realmedia': 'movie.gif',
    'application/x-dvi': 'dvi.gif',
    'application/x-gtar': 'tar.gif',
    'application/x-gzip': 'compressed.gif',
    'application/x-shockwave-flash': 'image2.gif',
    'application/x-tar': 'tar.gif',
    'application/x-tex': 'tex.gif',
    'application/zip': 'compressed.gif',
    'audio': 'sound1.gif',
    'audio/mpeg': 'sound1.gif',
    'audio/vnd.rn-realaudio': 'sound1.gif',
    'audio/x-wav': 'sound1.gif',
    'image': 'image2.gif',
    'image/gif': 'image2.gif',
    'image/jpeg': 'image2.gif',
    'image/png': 'image2.gif',
    'image/vnd.rn-realpix': 'image2.gif',
    'text': 'text.gif',
    'text/html': 'layout.gif',
    'text/plain': 'text.gif',
    'text/x-python': 'p.gif',
    'video': 'movie.gif',
    'video/mpeg': 'movie.gif',
    'video/quicktime': 'movie.gif',
    'video/vnd.rn-realvideo': 'movie.gif',
}
_icon_base = 'misc_/LocalFS/'
for k, v in _icons.items():
    _icons[k] = _icon_base + v


class LocalDirectory(OFS.CopySupport.CopyContainer, App.Management.Navigation,
                     OFS.SimpleItem.Item, Acquisition.Implicit):

    """Object representing a directory in the local file system."""

    meta_type = 'Local Directory'
    zmi_icon = 'far fa-folder text-danger'

    # Set to True and the ZMI becomes too sluggish
    isPrincipiaFolderish = 0
    manage_addProduct = ProductDispatcher()

    manage_main = HTMLFile('dtml/main', globals())
    manage_uploadForm = HTMLFile('dtml/methodUpload', globals())

    manage_options = (
        {'label': 'Contents', 'action': 'manage_main'},
        {'label': 'Upload', 'action': 'manage_uploadForm'},
        {'label': 'View', 'action': ''},
        )

    icon = 'misc_/OFSP/Folder_icon.gif'

    security = AccessControl.ClassSecurityInfo()  # sbk

    security.declareProtected('FTP access', 'manage_FTPstat',  # NOQA
                              'manage_FTPget', 'manage_FTPlist')

    def __init__(self, id, basepath, root, catalog, _type_map,
                 _icon_map, file_filter=None):
        """LocalDirectory __init__"""
        self.id = id
        self.basepath = self._local_path = basepath
        self.root = root
        self.catalog = catalog
        self._type_map = _type_map
        self._icon_map = _icon_map
        self.file_filter = file_filter

    def __bobo_traverse__(self, REQUEST, name):
        """ bobo_traverse """
        method = REQUEST.get('REQUEST_METHOD', 'GET').upper()
        try:
            # FTP - PUT
            if method not in ('GET', 'POST', 'HEAD'):
                return LockNullResource(name).__of__(self)
        except Exception:
            pass
        try:
            return self._safe_getOb(name)
        except Exception:
            pass
        try:
            return getattr(self, name)
        except AttributeError:
            pass

    def __getitem__(self, i):
        if isinstance(i, (str, bytes)):
            return self._safe_getOb(i)
        else:
            raise TypeError('index must be a string')

    def __getattr__(self, attr):
        try:
            return self._safe_getOb(attr)
        except NotFound:
            raise AttributeError(attr)

    def _getpath(self, id):
        return os.path.join(self.basepath, id)

    def _getfileob(self, id, spec=None):
        if spec is None:
            spec = self.file_filter
        path = self._getpath(id)
        return LocalFile(self, id, path, spec)

    def _ids(self, spec=None):
        if spec is None:
            spec = self.file_filter
        try:
            ids = os.listdir(self.basepath)
        except PermissionError:
            raise Forbidden('Sorry, you do not have permission to read '
                            'the requested directory.')

        if (spec is not None):
            try:
                if isinstance(spec, str):
                    spec = spec.split(' ')
                curdir = os.getcwd()
                os.chdir(self.basepath)
                candidates = []
                for id in ids:
                    if os.path.isdir(id) and '*/' in spec or '*\\' in spec:
                        candidates.append(id)
                for patt in spec:
                    names = glob.glob(patt)
                    for id in names:
                        if id[-1] == os.sep:
                            id = id[:-1]
                        if (id not in candidates):
                            candidates.append(id)
                ids = candidates
            finally:
                os.chdir(curdir)
        ids = sorted(filter(valid_id, ids))
        return ids

    def _safe_getOb(self, name, default=_marker):
        return self._getOb(name, default)

    def _getOb(self, id, default=_marker):
        if (id in (os.curdir, os.pardir)):
            raise ValueError(id)
        ob = None
        path = self._getpath(id)
        if (os.path.isdir(path)):
            ob = LocalDirectory(id, path, self.root or self, self.catalog,
                                self._type_map, self._icon_map)
        elif (os.path.isfile(path)):
            try:
                with open(path, 'rb') as f:
                    ob = _create_ob(id, f, path, self._type_map)
            except PermissionError:
                raise Forbidden('Sorry, you do not have permission to read '
                                'the requested resource "%s".' % id)

        if (ob is None):
            if default is _marker:
                raise AttributeError(id)
            return default
        _set_timestamp(ob, path)
        ob._p_jar = self._p_jar
        return ob.__of__(self)

    def _setObject(self, id, object, roles=None, user=None):
        if getattr(object, '__locknull_resource__', 0):
            self._checkId(id, 1)
            return id
        else:
            self._checkId(id)
        self._safe_setOb(id, object)
        return id

    def _delObject(self, id, dp=1):
        self._delOb(id)

    def _checkId(self, id, allow_dup=0):
        # If allow_dup is false, an error will be raised if an object
        # with the given id already exists. If allow_dup is true,
        # only check that the id string contains no illegal chars.
        if not id:
            raise BadRequest('No id was specified')
        if bad_id(id):
            raise BadRequest(
                'The id %s contains characters illegal in filenames.' % id)
        if id[0] == '_':
            raise BadRequest(
                'The id %s  is invalid - it begins with an underscore.' % id)
        if not allow_dup:
            path = self._getpath(id)
            if os.path.exists(path):
                raise BadRequest(
                    'The id %s is invalid - it is already in use.' % id)

    def _safe_setOb(self, id, ob):
        try:
            self._setOb(id, ob)
        except PermissionError:
            raise Forbidden('Sorry, you do not have permission to write '
                            'to this directory.')

    def _setOb(self, id, ob):
        if not hasattr(ob, 'meta_type'):
            raise BadRequest('Unknown object type.')
        path = self._getpath(id)
        try:
            _save_ob(ob, path)
        except TypeError:
            raise BadRequest(
                'Cannot add objects of type "%s" to local directories.'
                % ob.meta_type)

    def _delOb(self, id):
        path = self._getpath(id)
        try:
            if os.path.isdir(path):
                t = 'directory'
                os.rmdir(path)
            else:
                t = 'file'
                os.unlink(path)
        except PermissionError:
            raise Forbidden('Sorry, you do not have permission to delete '
                            'the requested %s ("%s").' % (t, id))
        except OSError:
            if t == 'directory' and os.listdir(path):
                raise DeleteError('The directory "%s" is not empty.' % id)
            raise

    def _copyOb(self, id, ob):
        self._setObject(id, ob)

    def _moveOb(self, id, ob):
        src = ob._local_path
        dest = self._getpath(id)
        try:
            os.rename(src, dest)
        except PermissionError:
            raise Forbidden('Sorry, you do not have permission to write '
                            'to this directory.')

    def _verifyObjectPaste(self, ob, REQUEST):
        pass

    def _write_file(self, file, path):
        try:
            if isinstance(file, bytes):
                outfile = open(path, 'wb')
                outfile.write(file)
                outfile.close()
            else:
                blocksize = 8*1024
                outfile = open(path, 'wb')
                data = file.read(blocksize)
                while data:
                    outfile.write(data)
                    data = file.read(blocksize)
                outfile.close()
        except PermissionError:
            raise Forbidden('Sorry, you do not have permission to write '
                            'to this directory.')

    def manage_createDirectory(self, path, action='manage_workspace',
                               REQUEST=None):
        """Create a new directory relative to this directory."""
        parts = [p for p in os.path.split(path) if p not in ('.', '..')]
        path = os.path.join(*parts)
        fullpath = os.path.join(self.basepath, path)
        if os.path.exists(fullpath):
            if REQUEST is not None:
                REQUEST.set('manage_tabs_message',
                            'Directory %s already exists.' % path)
                return self.manage_uploadForm(self, REQUEST)

        else:
            try:
                os.makedirs(fullpath)
            except PermissionError:
                msg = 'You do not have permission to write to this directory.'
                if REQUEST is not None:
                    REQUEST.set('manage_tabs_message', msg)
                    return self.manage_uploadForm(self, REQUEST)
                else:
                    raise Forbidden(msg)

            if REQUEST is not None:
                msg = 'Directory %s has been created.' % path
                REQUEST.set('manage_tabs_message', msg)
                return self.manage_main(self, REQUEST, update_menu=1)

    def index_html(self, REQUEST, RESPONSE):
        """ Show the default page if it exists, otherwise acquire """
        default_document = self.defaultDocument()
        if default_document is None:
            return aq_parent(aq_inner(self)).index_html(REQUEST, RESPONSE)
        return default_document(REQUEST, RESPONSE)

    def manage_upload(self, file, id='', action='manage_workspace',
                      REQUEST=None):
        """Upload a file to the local file system. The 'file' parameter
        is a FileUpload instance representing the uploaded file."""
        if hasattr(file, 'filename'):
            filename = file.filename
        else:
            filename = file.name
        if not id:
            # Try to determine the filename without any path.
            # First check for a UNIX full path. There will be no UNIX path
            # separators in a Windows path.
            if '/' in filename:
                id = filename[filename.rfind('/')+1:]
            # Next check for Window separators. If there are no UNIX path
            # separators then it's probably a Windows path and not a random
            # relative UNIX path which happens to have backslashes in it.
            # Lets hope this never happens, anyway. ;)
            elif '\\' in filename:
                id = filename[filename.rfind('\\')+1:]
            # Not sure if we'll ever get a Mac path, but here goes...
            elif ':' in filename:
                id = filename[filename.rfind(':')+1:]
            # Else we have a filename with no path components so let's use
            # that for the id.
            else:
                id = filename

        try:
            self._checkId(id, 1)
        except BadRequest as exc:
            if REQUEST is not None:
                REQUEST.set('manage_tabs_message', str(exc))
                return self.manage_uploadForm(self, REQUEST)
            else:
                raise UploadError(str(exc))

        path = self._getpath(id)
        if os.path.exists(path):
            self.manage_overwrite(file, path, REQUEST)
        else:
            self._write_file(file, path)

        if REQUEST:
            REQUEST.set('manage_tabs_message',
                        'File %s has been uploaded.' % id)
            return self.manage_main(self, REQUEST, update_menu=1)

    def manage_overwrite(self, file, path, REQUEST=None):
        """Overwrite a local file."""
        user = getSecurityManager().getUser()

        if user is None or \
           not user.has_permission('Overwrite local files', self):
            raise Unauthorized(
                    'Sorry, you are not authorized to overwrite files.')
        self._write_file(file, path)

    def manage_renameObject(self, id, new_id, REQUEST=None):
        """Rename a file or subdirectory."""
        error_msg = ''
        try:
            self._checkId(new_id)
            f = self._getpath(id)
            t = self._getpath(new_id)
            os.rename(f, t)
        except BadRequest as exc:
            error_msg = str(exc)
        except PermissionError:
            error_msg = 'You do not have permission to rename %s' % id

        if error_msg and REQUEST is None:
            raise RenameError(error_msg)

        if REQUEST is not None:
            REQUEST.set('manage_tabs_message', error_msg)
            return self.manage_main(self, REQUEST, update_menu=1)

    def manage_cutObjects(self, ids, REQUEST=None):
        """Put a reference to the objects named in ids in the clipboard,
        marked for a cut operation."""
        if isinstance(ids, str):
            ids = [ids]
        oblist = []
        for id in ids:
            ob = self._safe_getOb(id)
            m = FileMoniker(ob)
            oblist.append(m.ids)
        cp = (1, oblist)
        cp = _cb_encode(cp)
        if REQUEST is not None:
            resp = REQUEST['RESPONSE']
            resp.setCookie('__lcp', cp, path='%s' % REQUEST['SCRIPT_NAME'])
            return self.manage_main(self, REQUEST, cb_dataValid=1)
        return cp

    def manage_copyObjects(self, ids, REQUEST=None, RESPONSE=None):
        """Put a reference to the objects named in ids in the clipboard,
        marked for a copy operation."""
        if isinstance(ids, str):
            ids = [ids]
        oblist = []
        for id in ids:
            ob = self._safe_getOb(id)
            m = FileMoniker(ob)
            oblist.append(m.ids)
        cp = (0, oblist)
        cp = _cb_encode(cp)
        if REQUEST is not None:
            resp = REQUEST['RESPONSE']
            resp.setCookie('__lcp', cp, path='%s' % REQUEST['SCRIPT_NAME'])
            return self.manage_main(self, REQUEST, cb_dataValid=1)
        return cp

    def manage_pasteObjects(self, cb_copy_data=None, REQUEST=None):
        """Paste objects from the clipboard into the current directory.
        The cb_copy_data parameter, if specified, should be the result
        of a previous call to manage_cutObjects or manage_copyObjects."""
        cp = None
        if cb_copy_data is not None:
            cp = cb_copy_data
        else:
            if REQUEST and '__lcp' in REQUEST:
                cp = REQUEST['__lcp']
        if cp is None:
            raise CopyError('No clipboard data found.')

        try:
            cp = _cb_decode(cp)
        except Exception as e:
            six.raise_from(CopyError('Clipboard Error'), e)

        oblist = []
        m = FileMoniker()
        op = cp[0]
        for ids in cp[1]:
            m.ids = ids
            try:
                ob = m.bind(self.root or self)
            except Exception:
                raise CopyError('Item Not Found')
            self._verifyObjectPaste(ob, REQUEST)
            oblist.append(ob)

        if op == 0:
            # Copy operation
            for ob in oblist:
                id = self._get_id(absattr(ob.id))
                self._copyOb(id, ob)

            if REQUEST is not None:
                return self.manage_main(self, REQUEST, update_menu=1,
                                        cb_dataValid=1)

        if op == 1:
            # Move operation
            for ob in oblist:
                id = absattr(ob.id)
                if not sanity_check(self, ob):
                    raise CopyError('This object cannot be pasted into itself')
                id = self._get_id(id)
                self._moveOb(id, ob)

            if REQUEST is not None:
                resp = REQUEST['RESPONSE']
                resp.setCookie('cp_', 'deleted',
                               path='%s' % REQUEST['SCRIPT_NAME'],
                               expires='Wed, 31-Dec-97 23:59:59 GMT')
                return self.manage_main(self, REQUEST, update_menu=1,
                                        cb_dataValid=0)
        return ''

    def cb_dataValid(self):
        """Return true if clipboard data seems valid."""
        try:
            _cb_decode(self.REQUEST['__lcp'])
            return 1
        except Exception:
            return 0

    def manage_delObjects(self, ids=[], REQUEST=None):
        """Delete files or subdirectories."""
        notfound = []
        if isinstance(ids, str):
            ids = [ids]
        if not ids:
            if REQUEST is not None:
                REQUEST.set('manage_tabs_message', 'No items specified')
                return self.manage_main(self, REQUEST)

        for id in ids:
            path = self._getpath(id)
            if not os.path.exists(path):
                notfound.append(id)
            else:
                self._delObject(id)

        if REQUEST is not None:
            if notfound:
                msg = 'Some items were not found: %s' % ', '.join(notfound)
            else:
                msg = 'Items deleted.'
            REQUEST.set('manage_tabs_message', msg)
            return self.manage_main(self, REQUEST, update_menu=1)

    def fileIds(self, spec=None):
        """Return a list of subobject ids.
        If 'spec' is specified, return only objects whose filename
        matches 'spec'."""
        if spec is None:
            spec = self.file_filter
        return self._ids(spec)

    def fileValues(self, spec=None, propagate=1):
        """Return a list of Local File objects.
        If 'spec' is specified, return only objects whose filename
        matches 'spec'."""
        if spec is None:
            spec = self.file_filter
        r = []
        a = r.append
        g = self._getfileob
        if propagate:
            for id in self._ids(spec):
                a(g(id, spec))
        else:
            for id in self._ids(spec):
                a(g(id))
        # sort that directories come first
        res = []
        for v in r:
            s = '%s%s' % ((v.type != 'directory'), v.id)
            res.append((s, v))

        return [x[1] for x in sorted(res)]

    def fileItems(self, spec=None, propagate=1):
        """Return a list of (id, fileobject) tuples.
        If 'spec' is specified, return only objects whose filename
        matches 'spec'
        """
        if spec is None:
            spec = self.file_filter
        r = []
        a = r.append
        g = self._getfileob
        if propagate:
            for id in self._ids(spec):
                a((id, g(id, spec)))
        else:
            for id in self._ids(spec):
                a((id, g(id)))
        return r

    def objectIds(self, spec=None):
        """Return a list of subobject ids.

        Returns a list of subobject ids of the current object.  If 'spec' is
        specified, returns objects whose meta_type matches 'spec'.
        """
        if self.catalog:
            return self._objectIds(spec)
        return ()

    def objectValues(self, spec=None):
        """Return a list of the actual subobjects.

        Returns a list of actual subobjects of the current object.  If
        'spec' is specified, returns only objects whose meta_type match 'spec'
        """
        if self.catalog:
            return self._objectValues(spec)
        return ()

    def objectItems(self, spec=None):
        """Return a list of (id, subobject) tuples.

        Returns a list of (id, subobject) tuples of the current object.
        If 'spec' is specified, returns only objects whose meta_type match
        'spec'
        """
        if self.catalog:
            return self._objectItems(spec)
        return ()

    def _objectIds(self, spec=None):
        g = self._safe_getOb
        ids = self._ids()
        if spec is not None:
            if isinstance(spec, str):
                spec = [spec]
            r = []
            a = r.append
            for id in ids:
                ob = g(id)
                if ob.meta_type in spec:
                    a(id)
            return r
        return ids

    def _objectValues(self, spec=None):
        r = []
        a = r.append
        g = self._safe_getOb
        if spec is not None:
            if isinstance(spec, str):
                spec = [spec]
            for id in self._ids():
                ob = g(id)
                if ob.meta_type in spec:
                    a(g(id))
        else:
            for id in self._ids():
                a(g(id))
        return r

    def _objectItems(self, spec=None):
        r = []
        a = r.append
        g = self._safe_getOb
        if spec is not None:
            if isinstance(spec, str):
                spec = [spec]
            for id in self._ids():
                ob = g(id)
                if ob.meta_type in spec:
                    a((id, g(id)))
        else:
            for id in self._ids():
                a((id, g(id)))
        return r

    def serverPath(self):
        """Return the full path of the directory object relative to the
        root of the server."""
        ids = []
        ob = self
        while 1:
            if not hasattr(ob, 'id'):
                break
            ids.append(absattr(ob.id))
            if not hasattr(ob, 'aq_parent'):
                break
            ob = ob.aq_parent
        ids.reverse()
        path_str = '/'.join(ids)
        return path_str.encode('UTF-8')

    def parentURL(self):
        """Return the URL of the parent directory."""
        url = self.REQUEST['URL2']
        spec = self.REQUEST.get('spec', None)
        if (spec is not None):
            if isinstance(spec, str):
                url = '%s?spec=%s' % (url, quote(spec))
            else:
                query = []
                for patt in spec:
                    query.append('spec:list=%s' % quote(patt))
                url = url + '?' + '&'.join(query)
        return url

    def defaultDocument(self):
        """Return the first default document found in this folder
        as a Zope object or None."""
        # Don't know why but self.default_document is sometimes empty
        try:
            files = self.default_document.split()
            for file in files:
                path = self._getpath(file)
                if (os.path.isfile(path)):
                    try:
                        return self._safe_getOb(file)
                    except Forbidden:
                        pass
        except Exception:
            pass
        return None

    def bobobase_modification_time(self):
        t = os.stat(self._local_path)[stat.ST_MTIME]
        return DateTime(t)

    #
    #  FTP and WebDAV Support - sbk
    #

    @security.private
    def PUT_factory(self, name, typ, body):
        """
        Dispatcher for PUT requests to non-existent IDs.
        """
        if name and (name.endswith('.pt') or name.endswith('.zpt')):
            from Products.PageTemplates.ZopePageTemplate import \
                ZopePageTemplate
            ob = ZopePageTemplate(name, body, content_type=typ)
        elif typ in ('text/html', 'text/xml', 'text/plain'):
            from OFS.DTMLDocument import DTMLDocument
            if not isinstance(body, (str, bytes)):
                body = body.read()
            ob = DTMLDocument(body, __name__=name)
        elif typ[:6] == 'image/':
            from OFS.Image import Image
            ob = Image(name, '', body, content_type=typ)
        else:
            from OFS.Image import File
            ob = File(name, '', body, content_type=typ)
        return ob

    if HAVE_FTP:

        def manage_FTPlist(self, REQUEST):
            """Directory listing for FTP"""
            out = ()
            files = list(self.fileItems())
            is_root = getattr(self,
                              'isTopLevelPrincipiaApplicationObject',
                              None)
            try:
                if not is_root and self.isTopLevelPrincipiaApplicationObject:
                    files.insert(0, ('..', self.aq_parent))
            except Exception:
                pass

            for k, v in files:
                try:
                    stat = marshal.loads(v.manage_FTPstat(REQUEST))
                except Exception:
                    stat = None
                if stat is not None:
                    out = out + ((k, stat),)
            return marshal.dumps(out)

        def manage_FTPstat(self, REQUEST):
            """Psuedo stat used for FTP listings"""
            # mode = 0040000 | 0770
            mode = 33272 | 0o0770
            mtime = self.bobobase_modification_time().timeTime()
            owner = group = 'Zope'
            return marshal.dumps((mode, 0, 0, 1, owner, group, 0, mtime, mtime,
                                  mtime))


class LocalFile(OFS.SimpleItem.Item, Acquisition.Implicit):

    """Object representing a file in the local file system."""

    meta_type = 'Local File'

    security = AccessControl.ClassSecurityInfo()

    security.declareProtected('FTP access', 'manage_FTPstat',  # NOQA
                              'manage_FTPget', 'manage_FTPlist', 'PUT',
                              'manage_FTPput')

    def __init__(self, parent, id, path, spec):
        """LocalFile __init__"""
        self.parent = parent
        self.id = id
        self.path = path
        self.type = self._getType()
        self.url = self._getURL(spec)
        self.plain_url = self._getPlainURL()
        self.icon = self._getIcon()
        self.size = self._getSize()
        self.mtime = self._getTime()
        self.display_size = self._getDisplaySize()
        self.display_mtime = self._getDisplayTime()

    def getObject(self):
        """Return a Zope object representing this local file."""
        return self.parent._safe_getOb(self.id)

    def get_size(self):
        """Return the size of the file."""
        return self.size

    def bobobase_modification_time(self):
        """bobobase_modification_time"""
        return self.mtime

    def _getURL(self, spec):
        """_getURL"""
        url = quote(self.id)
        if (self.type == 'directory') and (spec is not None):
            if isinstance(spec, str):
                return url + '?spec=' + quote(spec)
            else:
                query = []
                for patt in spec:
                    query.append('spec:list=%s' % quote(patt))
                return url + '?' + '&'.join(query)
        return url

    def _getPlainURL(self):
        """_getPlainURL"""
        return quote(self.id)

    def _getType(self):
        """Return the content type of a file."""
        name = self.id
        path = self.path
        if (os.path.isdir(path)):
            return 'directory'
        ext = os.path.splitext(name)[-1]
        t, c = _get_content_type(ext, self.parent._type_map)
        if t:
            return t
        try:
            f = open(path, 'rb')
            data = f.read(_test_read)
            f.close()
            ob = OFS.Image.File(name, name, data)
            _set_content_type(ob, t, data)
            return ob.content_type
        except EnvironmentError:
            return 'application/octet-stream'

    def _getIcon(self):
        """Return the path of the icon associated with this file type."""
        content_type = self.type.lower()
        _icon_map = self.parent._icon_map
        try:
            return _icon_map[content_type]
        except KeyError:
            pass
        content_type = content_type[:content_type.find('/')]
        try:
            return _icon_map[content_type]
        except KeyError:
            pass
        return _icon_base + 'generic.gif'

    def _getSize(self):
        """Return the size of the specified file or -1 if an error occurs.
        Return None if the path refers to a directory."""
        path = self.path
        if (os.path.isdir(path)):
            return 0
        try:
            return os.stat(path)[stat.ST_SIZE]
        except Exception:
            return -1

    def _getDisplaySize(self):
        """Return the size of a file or directory formatted for display."""
        size = self.size
        if size in (0, None):
            return '-' * 5
        if size == -1:
            return _unknown
        k = 1024.0
        if (size > k):
            size = size / k
            if (size > k):
                size = size / k
                return '%.1f MB' % size
            else:
                return '%.1f kB' % size
        else:
            return '%d bytes' % size

    def _getTime(self):
        """Return the last modified time of a file or directory
        or None if an error occurs."""
        try:
            return DateTime(os.stat(self.path)[stat.ST_MTIME])
        except Exception:
            pass

    def _getDisplayTime(self):
        """Return the last modified time of a file or directory formatted
        for display."""
        t = self.mtime
        if t is None:
            return _unknown
        return '%s %s' % (t.Time(), t.Date())

    #
    # FTP and WebDAV Support - sbk
    #

    def PUT(self, REQUEST, RESPONSE):
        """ Handle HTTP PUT requests """
        self.dav__init(REQUEST, RESPONSE)
        self.dav__simpleifhandler(REQUEST, RESPONSE, refresh=1)
        self.write(REQUEST.get('BODY', ''))
        self.ZCacheable_invalidate()
        RESPONSE.setStatus(204)
        return RESPONSE

    manage_FTPput = PUT

    def manage_FTPget(self):
        """Get source for FTP download"""
        self.REQUEST.RESPONSE.setHeader('Content-Type', self.content_type)
        return self.read()

    getSize = get_size

    if HAVE_FTP:

        def manage_FTPstat(self, REQUEST):
            """Psuedo stat used for FTP listings"""
            size = self._getSize()
            # mode = 0100000 | 0660
            mode = 33152 | 0o0660
            if self.type == 'directory':
                size = 0
                # mode = 0040000 | 0770
                mode = 33272 | 0o0770
            mtime = self.bobobase_modification_time().timeTime()
            owner = group = 'Zope'
            return marshal.dumps((mode, 0, 0, 1, owner, group, size, mtime,
                                  mtime, mtime))


class FileMoniker:

    """A file moniker is a reference to an object in the file system."""

    def __init__(self, ob=None):
        """FileMoniker __init__"""
        if ob is None:
            return
        self.ids = []
        while 1:
            if not hasattr(ob, 'id'):
                break
            if ob.meta_type == 'Local File System':
                break
            self.ids.append(absattr(ob.id))
            ob = ob.aq_parent
        self.ids.reverse()

    def bind(self, root):
        """Return the file object named by this moniker"""
        ob = root
        for id in self.ids:
            ob = ob._safe_getOb(id)
        return ob


class LocalFS(LocalDirectory, OFS.PropertyManager.PropertyManager,
              Persistence.Persistent, RoleManager):

    """Object that creates Zope objects from files in the local file system."""

    meta_type = 'Local File System'
    zmi_icon = 'far fa-hdd text-danger'

    manage_options = (
        ({'label': 'Contents', 'action': 'manage_main'},
         {'label': 'View', 'action': ''},
         {'label': 'Properties', 'action': 'manage_propertiesForm'},
         {'label': 'Security', 'action': 'manage_access'},
         {'label': 'Upload', 'action': 'manage_uploadForm'})
    )

    __ac_permissions__ = (
        ('View', ('',)),
        ('View management screens',
            ('manage', 'manage_main')),
        ('Change Local File System properties',
            ('manage_propertiesForm', 'manage_changeProperties')),
        ('Access contents information',
            ('fileIds', 'fileValues', 'fileItems')),
        ('Upload local files',
            ('manage_uploadForm', 'manage_upload')),
        ('Overwrite local files', ('manage_overwrite',)),
        ('Manage local files',
            ('manage_cutObjects', 'manage_copyObjects', 'manage_pasteObjects',
             'manage_renameForm', 'manage_renameObject',
             'manage_createDirectory')),
        ('Delete local files', ('manage_delObjects',)),
        )

    _properties = (
        {'id': 'title', 'type': 'string', 'mode': 'w'},
        {'id': 'basepath', 'type': 'string', 'mode': 'w'},
    )
    if (_iswin32):
        _properties = _properties + (
            {'id': 'username', 'type': 'string', 'mode': 'w'},
            {'id': 'password', 'type': 'string', 'mode': 'w'},
            )
    _properties = _properties + (
        {'id': 'default_document', 'type': 'string', 'mode': 'w'},
        {'id': 'type_map', 'type': 'lines', 'mode': 'w'},
        {'id': 'icon_map', 'type': 'lines', 'mode': 'w'},
        {'id': 'catalog', 'type': 'boolean', 'mode': 'w'},
        {'id': 'file_filter', 'type': 'string', 'mode': 'w'},
    )

    default_document = 'index.html default.html'
    username = _share = ''
    _connected = 0
    isPrincipiaFolderish = 1  # leaving this at one though
    catalog = 0
    root = None
    password = _password = ''

    _type_map = _types
    _icon_map = _icons
    type_map = _typemap2list(_types)
    icon_map = _iconmap2list(_icons)
    file_filter = None

    def __init__(self, id, title, basepath, username, password):
        """LocalFS __init__"""
        LocalDirectory.__init__(self, id, basepath, self, self.catalog,
                                self._type_map, self._icon_map,
                                self.file_filter)
        self.title = title

        self.basepath = self._local_path = basepath
        if (_iswin32):
            self.username = username
            self._password = password or ''
            m = unc_expr.match(self.basepath)
            if (m is not None) and (self.username):
                self._share = m.group(1)
                self._connect()
            else:
                self._share = ''

    def manage_editProperties(self, REQUEST):
        """Edit object properties via the web.
        The purpose of this method is to change all property values,
        even those not listed in REQUEST; otherwise checkboxes that
        get turned off will be ignored.  Use manage_changeProperties()
        instead for most situations.
        """
        type_map = self.type_map
        icon_map = self.icon_map
        username = self.username
        password = self.password

        super(LocalFS, self).manage_editProperties(REQUEST)

        if not self.file_filter.strip():
            self.file_filter = None
        if self.file_filter == 'None':
            self.file_filter = None
        if self.type_map != type_map:
            self._type_map = _list2typemap(self.type_map)
        if self.icon_map != icon_map:
            self._icon_map = _list2iconmap(self.icon_map)
        if (_iswin32):
            if self.username != username or self.password != password:
                self._password = self.password
                if (self._connected):
                    self._disconnect()
                m = unc_expr.match(self.basepath)
                if (m is not None) and (self.username):
                    self._share = m.group(1)
                    self._connect()
                else:
                    self._share = ''
            self.password = ''
        message = 'Saved changes.'
        return self.manage_propertiesForm(self, REQUEST,
                                          manage_tabs_message=message,
                                          update_menu=1)

    def manage_changeProperties(self, REQUEST=None, **kw):
        """Change existing object properties.

        Change object properties by passing either a mapping object
        of name:value pairs {'foo':6} or passing name = value parameters
        """
        type_map = self.type_map
        icon_map = self.icon_map
        username = self.username
        password = self._password

        super(LocalFS, self).manage_changeProperties(REQUEST=REQUEST, **kw)

        if self.type_map != type_map:
            self._type_map = _list2typemap(self.type_map)
        if self.icon_map != icon_map:
            self._icon_map = _list2iconmap(self.icon_map)
        if (_iswin32):
            if self.username != username or self.password != password:
                self._password = self.password
                if (self._connected):
                    self._disconnect()
                m = unc_expr.match(self.basepath)
                if (m is not None) and (self.username):
                    self._share = m.group(1)
                    self._connect()
                else:
                    self._share = ''
            self.password = ''

    def _connect(self):
        """_connect"""
        win32wnet.WNetAddConnection2(1, None, self._share, None,
                                     self.username or None,
                                     self._password or None)
        self._connected = 1

    def _disconnect(self):
        """_disconnect"""
        win32wnet.WNetCancelConnection2(self._share, 0, 0)
        self._connected = 0

    def _check_connected(self):
        """_check_connected"""
        if (self._share and not self._connected):
            self._connect()

    def _ids(self, spec=None):
        """_ids"""
        self._check_connected()
        return LocalDirectory._ids(self, spec)

    def _getfileob(self, id, spec=None):
        """_getfileob"""
        self._check_connected()
        return LocalDirectory._getfileob(self, id, spec)

    def _getOb(self, id, default=_marker):
        """_getOb"""
        self._check_connected()
        return LocalDirectory._getOb(self, id, default)

    def bobobase_modification_time(self):
        """bobobase_modification_time"""
        return Persistence.Persistent.bobobase_modification_time(self)

    def hasDefaultDocument(self):
        """Return true if is Directory and has default doc"""
        # Don't know why but self.default_document is sometimes empty
        try:
            files = self.default_document.split()
            for file in files:
                path = self._getpath(file)
                if (os.path.isfile(path)):
                    try:
                        return self._safe_getOb(file)
                    except Forbidden:
                        pass
        except Exception:
            pass
        return None


def manage_addLocalFS(self, id, title, basepath, username=None,
                      password=None, REQUEST=None):
    """Add a local file system object to a folder

    In addition to the standard Zope object-creation arguments,
    'id' and 'title', the following arguments are defined:

        basepath -- The base path of the local files.
        username -- Username for a network share (win32 only).
        password -- Password for a network share (win32 only).
    """

    ob = LocalFS(id, title, basepath, username, password)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)


manage_addLocalFSForm = HTMLFile('dtml/methodAdd', globals())
