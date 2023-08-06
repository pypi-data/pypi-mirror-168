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
# Utility functions and definitions

import os
import re
import stat
import sys

import OFS
from App.Extensions import getObject
from DateTime import DateTime
from OFS.Image import Pdata
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Products.PythonScripts.PythonScript import PythonScript
from ZODB.utils import p64


try:
    import ZServer  # NOQA: F401 unused import
    HAVE_FTP = True
except ImportError:
    HAVE_FTP = False


_iswin32 = (sys.platform == 'win32' or
            'test' in os.environ.get('_', '') or
            os.environ.get('TOX_ENV_DIR', ''))
_test_read = 1024 * 8
_unknown = '(unknown)'
_marker = []
unc_expr = re.compile(r'(\\\\[^\\]+\\[^\\]+)(.*)')


def _get_content_type(ext, _type_map):
    """_get_content_type"""
    try:
        return _type_map[ext.lower()]
    except (KeyError, AttributeError):
        return (None, None)


def _set_content_type(ob, content_type, data):
    """_set_content_type"""
    if content_type:
        ob.content_type = content_type

    if hasattr(ob, 'content_type') and ob.content_type == 'text/html':
        if content_type == 'text/html':
            return
        data = data.strip().lower()
        if data[:6] != '<html>' and data[:14] != '<!doctype html':
            ob.content_type = 'text/plain'


def _list2typemap(types_list):
    """_list2typemap"""
    if not types_list:
        return
    types_mapping = {}
    for i in types_list:
        if i:
            try:
                e, t = i.split()
                c = ''
            except ValueError:
                try:
                    e, t, c = re.split('[ \t]+', i, 2)
                except ValueError:
                    raise ValueError('Error parsing type map: "%s"' % i)
            types_mapping[e] = (t, c)
    return types_mapping


def _typemap2list(types_mapping):
    """_typemap2list"""
    res = []
    keys = sorted(types_mapping.keys())
    for k in keys:
        v = types_mapping[k]
        if isinstance(v, tuple):
            res.append(' '.join((k, v[0], v[1])))
        else:
            res.append(' '.join((k, v)))
    return res


def _list2iconmap(icons_list):
    """_list2iconmap"""
    if not icons_list:
        return
    icons_mapping = {}
    for i in icons_list:
        if i:
            try:
                k, v = i.split()
            except ValueError:
                raise ValueError("Error parsing icon map: '%s'" % i)
            icons_mapping[k] = v
    return icons_mapping


def _iconmap2list(icons_mapping):
    """_iconmap2list"""
    res = []
    for key in sorted(icons_mapping.keys()):
        res.append(' '.join((key, icons_mapping[key])))
    return res


def _create_ob(id, file, path, _type_map):
    """_create_ob"""
    ob = None
    ext = os.path.splitext(path)[-1]
    t, c = _get_content_type(ext, _type_map)
    if c is not None:
        ob = _create_builtin_ob(c, id, file, path)
        if ob is None:
            ob = _create_ob_from_function(c, id, file, path)
        if ob is None:
            ob = _create_ob_from_factory(c, id, file, path)
    if ob is None:
        ob = _wrap_ob(_create_File(id, file), path)
    file.seek(0)
    ob.__doc__ = 'LocalFile'
    _set_content_type(ob, t, file.read(_test_read))
    return ob


def _create_DTMLMethod(id, file):
    """_create_DTMLMethod"""
    return OFS.DTMLMethod.DTMLMethod(file.read().decode(), __name__=id)


def _create_DTMLDocument(id, file):
    """_create_DTMLDocument"""
    return OFS.DTMLDocument.DTMLDocument(file.read().decode(), __name__=id)


def _create_Image(id, file):
    """_create_Image"""
    # return StreamingImage(id, '', file)
    return OFS.Image.Image(id, '', file)


def _create_File(id, file):
    """_create_File"""
    # return StreamingFile(id, '', file)
    return OFS.Image.File(id, '', file)


def _create_ZPT(id, file):
    """_create_ZPT"""
    return ZopePageTemplate(id, file, content_type='text/html')


def _create_PythonScript(id, file):
    """_create_PythonScript"""
    ob = PythonScript(id)
    ob.write(file.read())
    return ob


_builtin_create = {
    'PythonScript': _create_PythonScript,
    'DTMLMethod': _create_DTMLMethod,
    'DTMLDocument': _create_DTMLDocument,
    'Image': _create_Image,
    'File': _create_File,
    'PageTemplate': _create_ZPT,  # ***SmileyChris
}


def _create_builtin_ob(c, id, file, path):
    try:
        f = _builtin_create[c]
        return _wrap_ob(f(id, file), path)
    except Exception:
        pass


def _create_ob_from_function(c, id, file, path):
    try:
        i = c.rindex('.')
        m, c = c[:i], c[i+1:]
        m = __import__(m, globals(), locals(), (c,))
        c = getattr(m, c)
        f = getattr(c, 'createSelf').__func__
        if f.__code__.co_varnames == ('id', 'file'):
            return _wrap_ob(f(id, file), path)
    except Exception:
        pass


def _create_ob_from_factory(c, id, file, path):
    try:
        i = c.rindex('.')
        m, c = c[:i], c[i+1:]
        c = getObject(m, c)
        f = c()
        ob = _wrap_ob(f(id, file), path)
        ob.__factory = f
        return ob
    except Exception:
        pass


class Wrapper:
    """Mix-in class used to save object changes."""
    _local_path = None
    # Create a global and persistent lock table
    _dav_writelocks = {}
    # The object itself is not persistent and cannot be stored
    _p_changed = 0

    def bobobase_modification_time(self):
        """ bobobase_modification_time """
        t = os.stat(self._local_path)[stat.ST_MTIME]
        return DateTime(t)

    def __repr__(self):
        """ __repr__ """
        c = self.__class__.__bases__[-1].__name__
        return '<%s ObjectWrapper instance at %8X>' % (c, id(self))

    def wl_lockmapping(self, killinvalids=0, create=0):
        """ Overwrite the default method of LockableItem """
        locks = self._dav_writelocks.get(self._local_path)
        if locks is None:
            locks = {}
            if create:
                # Store it in persistent lock table
                self._dav_writelocks[self._local_path] = locks
        elif killinvalids:
            # Delete invalid locks
            for token, lock in locks.items():
                if not lock.isValid():
                    del locks[token]
            if not locks and not create:
                # Remove empty lock table
                del self._dav_writelocks[self._local_path]
        return locks


_wrapper_method = '''def %(name)s %(arglist)s:
    """Wrapper for the %(name)s method."""
    # r = apply(self.__class__.__bases__[-1].%(name)s, %(baseargs)s)
    r = self.__class__.__bases__[-1].%(name)s(*%(baseargs)s)
    try: _save_ob(self, self._local_path)
    except ValueError: pass
    return r
'''

_wrappers = {}


def _get_wrapper(c):
    try:
        return _wrappers[c]
    except KeyError:
        class ObjectWrapper(Wrapper, c):
            pass

        _wrap_method(ObjectWrapper, 'manage_edit')
        _wrap_method(ObjectWrapper, 'manage_upload')
        _wrap_method(ObjectWrapper, 'pt_edit')  # PT ZMI editing
        _wrap_method(ObjectWrapper, 'write')  # PythonScript
        _wrap_method(ObjectWrapper, 'ZBindingsHTML_editAction')  # PythonScript
        _wrap_method(ObjectWrapper, 'PUT')
        # Remove management options that cannot be used
        manage_options = []
        for opt in ObjectWrapper.manage_options:
            if opt['label'] not in ('Properties', 'Security', 'Undo',
                                    'Ownership', 'Interfaces', 'Proxy',
                                    'History'):
                manage_options.append(opt)
        ObjectWrapper.manage_options = tuple(manage_options)
        _wrappers[c] = ObjectWrapper
        return ObjectWrapper


def _wrap_method(c, name):
    try:
        m = getattr(c.__bases__[-1], name)
    except AttributeError:
        return
    try:
        f = m.__func__
    except AttributeError:
        f = m
    a = list(f.__code__.co_varnames)[:f.__code__.co_argcount]
    d = f.__defaults__ or ()
    arglist = []
    baseargs = []
    while (len(a) > len(d)):
        arglist.append(a[0])
        baseargs.append(a[0])
        del a[0]
    for i in range(len(a)):
        arglist.append('%s=%s' % (a[i], repr(d[i])))
        baseargs.append(a[i])
    arglist = '(' + ','.join(arglist) + ')'
    baseargs = '(' + ','.join(baseargs) + ')'
    d = {}
    # exec _wrapper_method % vars() in globals(), d
    exec(_wrapper_method % vars(), globals(), d)
    setattr(c, name, d[name])


def _wrap_ob(ob, path):
    c = ob.__class__
    n = ob.__name__
    if hasattr(c, '__basicnew__'):
        c = _get_wrapper(c)
        d = ob.__dict__
        ob = c.__basicnew__()
        ob.__dict__.update(d)
    else:
        c = _get_wrapper(c)
        ob.__class__ = c
    ob._local_path = path
    ob.__name__ = n
    ob._p_oid = path
    return ob


def _save_DTML(ob, path):
    f = open(path, 'w')
    try:
        f.write(ob.read())
    finally:
        f.close()


def _save_File(ob, path):
    with open(path, 'wb') as fp:
        if isinstance(ob.data, Pdata):
            fp.write(bytes(ob.data))
        else:
            fp.write(ob.data)


def _save_Folder(ob, path):
    os.mkdir(path)


_builtin_save = {
    'Script (Python)': _save_DTML,
    'DTML Method': _save_DTML,
    'DTML Document': _save_DTML,
    'Image': _save_File,
    'File': _save_File,
    'Folder': _save_Folder,
    'Page Template': _save_DTML,  # ***SmileyChris
}


def _save_builtin_ob(ob, path):
    try:
        f = _builtin_save[ob.meta_type]
        f(ob, path)
        return 1
    except KeyError:
        pass


def _save_ob_with_function(ob, path):
    try:
        ob.saveSelf(path)
        return 1
    except Exception:
        pass


def _save_ob_with_factory(ob, path):
    try:
        ob.__factory.save(ob, path)
        return 1
    except Exception:
        pass


def _save_ob(ob, path):
    s = _save_builtin_ob(ob, path)
    if not s:
        s = _save_ob_with_function(ob, path)
    if not s:
        s = _save_ob_with_factory(ob, path)
    if not s:
        raise TypeError("Cannot save files of type '%s'." % ob.meta_type)


def _set_timestamp(ob, path):
    t = os.stat(path)[stat.ST_MTIME]
    ob._p_serial = p64(t)


_marker = []


def valid_id(id):
    if id == os.curdir or id == os.pardir or id[0] == '_':
        return 0
    return 1


bad_id = re.compile('[^a-zA-Z0-9-_~,. ]').search


def sanity_check(c, ob):
    # This is called on cut/paste operations to make sure that
    # an object is not cut and pasted into itself or one of its
    # subobjects, which is an undefined situation.
    dest = c.basepath
    src = ob._local_path
    if dest[:len(src)] != src:
        return 1
