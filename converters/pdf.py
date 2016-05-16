"""
 Deal with thumbnail extraction operations on PDF using the Open OFfice family of software.


(c) Peter Sefton 2016

This file is part of Netta.

    Netta is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.



"""
from PyPDF2 import PdfFileReader
import subprocess



class Pdf(FileType):
    name = "PDF"
    exts = [".pdf"]
    viewable = True
    
    
    def __init__(self, file):
        self.setup(file)
        

    def make_thumbnail(self):
        """
        Make a thumbnail of this PDF via soffice (Libre office or another Open Office Variant
        Needs soffice to be on your $PATH
        """
        if self.fresh_thumbnail_needed():
            command = "soffice --headless --convert-to png --outdir '{html_dir}' '{filename}'".format(filename=self.original_path, html_dir=self.thumb_dir)
            res = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)
            self.make_image_thumbnail(self.renditons_store.thumb_path)

# This is called from the __init__ method of converters.Converters
self.register(Pdf)
