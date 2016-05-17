""" 

Deal with Image thumbnails - not much needed here as it's built in.



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



class Img(FileType):
    name = "Image"
    exts = [".jpg",".jpeg",".tiff",".gif"]
    viewable = True
    
    
    def __init__(self, file):
        self.setup(file)
        

    def make_thumbnail(self):
        """
        Use standard method
        """
        if self.fresh_thumbnail_needed():
            self.make_image_thumbnail()

# This is called from the __init__ method of converters.Converters
self.register(Img)
