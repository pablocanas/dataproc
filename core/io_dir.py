#
#
# Copyright (C) 2013 Patricio Rojo
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General 
# Public License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, 
# Boston, MA  02110-1301, USA.
#
#

from functools import wraps as _wraps
from io_file import AstroFile

class astrodir():
    """Collection of AstroFile"""
    def __init__(self, path):
        import os
        import glob
        import os.path as pth
        files=[]

        filndir = glob.glob(path)

        if len(filndir)==0:
            raise ValueError("invalid path to files")
        for f in filndir:
            if pth.isdir(f):
                for sf in os.listdir(f):
                    nf = AstroFile(f+'/'+sf)
                    if nf:
                        files.append(nf)
            else:
                nf = AstroFile(f)
                if nf:
                    files.append(nf)
        self.files = files

    def readdata(self):
        import scipy as sp
        if isinstance(self,'datacube'):
            return self.datacube
        data = []
        for f in self.files():
            data.append(f.reader())
        self.datacube = sp.array(data)
        return self.datacube

    def sort(self, *args):
        """Return sorted list of files according to specified header field, use first match. It uses in situ sorting, but returns itself"""
        if len(args)==0:
            raise ValueError("At least one valid header field must be specified to sort")
        hdrfld=False
        for a in args:
            if self.getheaderval(a):
                hdrfld=a
                break
        if not hdrfld:
            raise ValueError("A valid header field must be specified to use as a sort key. None of the currently requested were found: %s" %(', '.join(args),))
        for f in self.files:
            f.sortkey=hdrfld
        self.files.sort()
        return self

    def __iter__(self):
        return iter(self.files)

    def __repr__(self):
        return "<astrofile container: %s>" % (self.files.__repr__(),)

    def __getitem__(self, item):
        return self.files.__getitem__(item)

    def __len__(self):
        return self.files.__len__()

    def filter(self, *args, **kwargs):
        """Filter files according to those whose filter return True to the given arguments. What the filter does is type-dependent in each file. Check docstring of a single element."""
        from copy import copy
        new = copy(self)
        new.files = [f for f in self if f.filter(*args,**kwargs)]
        return new

    def basename(self, joinchr=', '):
        """Returns the basename of the files in object"""
        return joinchr.join([b.basename() for b in self])

    def getheaderval(self, *args, **kwargs):
        """Gets the header values specified in 'args' from each of the files. Returns a simple list if only one value is specified, or a list of tuples otherwise"""
        if 'mapout' in kwargs:
            mapout = kwargs['mapout']
        else:
            mapout= len(args)==1 and (lambda x:x[0]) or None
        return [f.getheaderval(*args, mapout=mapout) for f in self.files]
        


# def astrodir(path, ffilter=None):
#     """Load a directory or individual astro0qualifying files. Optionally, a FITS header filter can be applied.  Wildcards are ok """
#     import os
#     import glob
#     files=[]

#     filndir = glob.glob(path)

#     if len(filndir)==0:
#         raise ValueError("invalid path to files")
#     for f in filndir:
#         if _path.isdir(f):
#             for sf in os.listdir(f):
#                 nf = AstroFile(f+'/'+sf, ffilter=ffilter)
#                 if nf:
#                     files.append(nf)
#         else:
#             nf = AstroFile(f, ffilter=ffilter)
#             if nf:
#                 files.append(nf)

#     return files
        
