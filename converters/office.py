"""
 Deal with thumbnail extraction operations on Office documents using the Open OFfice family of software.


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


import subprocess
import tempfile 
from shutil import copyfile



class Office(FileType):
    name = "Office"

    
    exts = [".doc",".docx",".xls",".xlsx"]

    
    def __init__(self, file):
        self.setup(file)
        

    def make_thumbnail(self):
        """
        Make thumbnails using soffice. TODO: fix paths, this won't handle two docs with same filestem eg doc.doc and doc.docx, 
        need to use a temp dir then move the resulting file
        """
        if self.fresh_thumbnail_needed():
            self.make_pdf()
            with tempfile.TemporaryDirectory() as tmp:
                # Gnerate a PNG from the front page
                command = "soffice --headless --convert-to png --outdir '{html_dir}' '{filename}'".format(filename=self.renditions_store.pdf_path, html_dir=tmp)
                res = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)
                copyfile(os.path.join(tmp, self.renditions_store.stem + ".png"), self.renditions_store.thumb_path)
                self.make_image_thumbnail(self.renditions_store.thumb_path)

    def make_pdf(self):
        if self.fresh_pdf_needed():
            with tempfile.TemporaryDirectory() as tmp:
                # save as PDF then copy to the right place
                command = "soffice --headless --convert-to pdf --outdir '{html_dir}' '{filename}'".format(filename=self.renditions_store.original_path, html_dir=tmp)
                res = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)
                copyfile(os.path.join(tmp, self.renditions_store.stem + ".pdf"), self.renditions_store.pdf_path)

# This is called from the __init__ method of converters.Converters
self.register(Office)
