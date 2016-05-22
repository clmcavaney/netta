"""
 Basic functions for file conversion and metadata extraction

RenditionsStore: deals with setting up paths etc for caching file renditions, metadata and thumbnails
Converters: Class for keeping track of converter plugins for various file tpyes
FileType: Type-specific conversion and metadata extraction code


(c) Peter Sefton 2016

This file is part of Netta.

    Netta is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Netta is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Netta.  If not, see <http://www.gnu.org/licenses/>.



"""

import os
import imp
from PIL import Image
import json
from tika import parser
import subprocess
import tempfile

from shutil import copyfile

class RenditionsStore:
    """
    Deal with creating paths for where thumbnails, metadata and converted docs get stored
    file: The file for which to calculate paths, can be absolute or relative
    home: Where to keep renditions, if None, will default to ~/_renditions_ 
    test_mode: If true will not try to make pre-make directories otherwise it will

    """
    def __init__(self, file, home = None, test_mode = False):   
        self.original_path = file
        self.path, self.filename = os.path.split(file)
        self.stem, self.ext = os.path.splitext(self.filename)
        if home == None:
            home = os.path.expanduser("~")
           
        self.original_dir,self.filename = os.path.split(self.original_path)
        
        rel_path = os.path.relpath(self.path, "/") if os.path.isabs(self.path) else self.path
            
        self.renditions_dir = os.path.join(home,"_renditions_", rel_path)
        if not test_mode and not os.path.exists(self.renditions_dir):
            os.makedirs(self.renditions_dir)
            
        self.thumb_dir = os.path.join(self.renditions_dir,"thumbs")
        if not test_mode and not os.path.exists(self.thumb_dir):
            os.makedirs(self.thumb_dir)
            
        # Special place for PDF - TODO: have a similar thing for HTML too
        self.pdf_dir = os.path.join(self.renditions_dir,"pdf")
        if not test_mode and not os.path.exists(self.pdf_dir):
            os.makedirs(self.pdf_dir)

        self.pdf_filename = self.filename + ".pdf" #TODO: this should be filename + '.pdf'
        self.pdf_path = os.path.join(self.pdf_dir, self.pdf_filename)
        self.thumb_filename =  self.filename + ".png"
        self.thumb_path = os.path.join(self.thumb_dir, self.thumb_filename)
        self.meta_path = os.path.join(self.renditions_dir,  self.filename + ".metadata.json")
    

class Converters:
    """ Container for conversion objects that know how to get metadata, make thumbnails etc for various filetypes"""
    def __init__(self, dir, home=None):
        self._converters_by_ext = {}
        self._converters_by_mime = {}
        self._converters_by_pronom = {}
        self.converters = []
        if not home:
            home = os.path.expanduser("~")
        self._home = home

        for converter in [x for x in os.listdir(dir) if x.endswith(".py") and not x.startswith(".")]:
            with open(os.path.join(dir, converter)) as f:
                code = compile(f.read(), converter, 'exec')
                exec(code)
                

    def register(self, some_class):
        """Build look up tables so we can find this converter using a mime, extension or pronom description, pass in a FileType instance"""
        some_class.home = self._home
        self.converters.append(some_class)
        for ext in some_class.exts:
            self._converters_by_ext[ext.lower()] = some_class
        for mime in some_class.mimes:
            self._converters_by_mimes[mime] = some_class
        for pronom in some_class.pronoms:
            self._converters_by_pronom[pronom] = some_class
            
    def get_by_ext(self, ext):
        """ Return a converter class based on extension lookup """
        ext = ext.lower()
        if ext in self._converters_by_ext:
            return self._converters_by_ext[ext]
        else:
            return self._converters_by_ext['*']
        
 
class FileType:
    """ Super-class, converter for a particular type of file. The file-type specific stuff is handled by plugins"""
    
    pronoms = []
    exts = []
    mimes = []
    def __init__(self):
        pass
    
    def setup(self, file):
        self.renditions_store  = RenditionsStore(file, self.home)
        

    #Methods to help cache thumbnails and metada
    def fresh_thumbnail_needed(self):
        return not os.path.exists(self.renditions_store.thumb_path) or os.path.getmtime(self.renditions_store.thumb_path) < os.path.getmtime(self.renditions_store.original_path)

    def fresh_metadata_needed(self):
        return not os.path.exists(self.renditions_store.meta_path) or os.path.getmtime(self.renditions_store.meta_path) < os.path.getmtime(self.renditions_store.original_path)

    def fresh_pdf_needed(self):
        return not os.path.exists(self.renditions_store.pdf_path) or os.path.getmtime(self.renditions_store.pdf_path) < os.path.getmtime(self.renditions_store.original_path)
    # TODO Garbage collection
    
    def has_thumbnail_method(self):
        """Default is to not make thumbnails"""
        return 'make_thumbnail' in dir(self)

    def has_pdf_method(self):
        """Default is to not make thumbnails"""
        return 'make_pdf' in dir(self)

 
    def make_image_thumbnail(self, path=None):
        if not path:
            path = self.renditions_store.original_path
        size = 128,128
        im = Image.open(path)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(self.renditions_store.thumb_path, "PNG")

    def get_metadata(self):
        """Returns metadata from any file via Apache Tika - overwrite this method if you know better"""
        if self.fresh_metadata_needed():
            try:
                parsed = parser.from_file(self.renditions_store.original_path)
            except:
                parsed = {}
            if "metadata" not in parsed:
                parsed["metadata"] = {}
            self.parsed = parsed
            with open(self.renditions_store.meta_path, "w") as f:
                f.write(json.dumps(parsed))
                return(parsed['metadata'])
            
        else:
            with open(self.renditions_store.meta_path) as meta:
                self.parsed = json.load(meta)
                return self.parsed['metadata']
            
    def get_metadata_item(self, field):
        """Looks up metadata using field returns none if not found"""
        if field in self.parsed['metadata']:
            return self.parsed['metadata'][field]
        else:
            return None
        
    def get_mime(self):
        """Returns the mime type of the file"""
        if "Content-Type" in self.parsed['metadata']:
            return self.parsed['metadata']["Content-Type"]
        else:
            return None
    
    def get_viewable(self):
        """
        Returns a mime type if this file is viewable, deals with things
        like office docs that can have PDF previews
        Returns None if this is not known to be viewable

        TODO: Make this return a tuple of viewable path and mime-string
        """
        mime = self.get_mime()
        # We don't want a list of mimes - jsut one
        if mime and isinstance(mime, list):
            mime = mime[0]
            
        if mime and mime.startswith("text/"):
            return (self.renditions_store.original_path, mime)
        if mime in ["image/jpeg","application/pdf","image/png"]:
            return (self.renditions_store.original_path, mime)

        if self.has_pdf_method():
            return (self.renditions_store.pdf_path, "application/pdf")

        return None
