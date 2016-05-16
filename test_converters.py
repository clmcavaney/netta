"""
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


import unittest
import converters
import shutil
import os


class TestLoading(unittest.TestCase):
  def cleanup(self):
      renditions = os.path.join('test', '_renditions_')
      if os.path.exists(renditions):
          shutil.rmtree(renditions)

  def test_paths(self):
      path = "/some/root/path/file_name.docx"
      rs = converters.RenditionsStore(path, "/opt/", test_mode=True)
      self.assertEqual(rs.renditions_dir, "/opt/_renditions_/some/root/path")
      self.assertEqual(rs.pdf_dir, "/opt/_renditions_/some/root/path/pdf")
      self.assertEqual(rs.thumb_dir, "/opt/_renditions_/some/root/path/thumbs")
      self.assertEqual(rs.thumb_path, "/opt/_renditions_/some/root/path/thumbs/file_name.docx.png")
      self.assertEqual(rs.pdf_path, "/opt/_renditions_/some/root/path/pdf/file_name.pdf") #TODO - make this .docx.pdf

      home = os.path.expanduser("~")
      rs = converters.RenditionsStore(path, test_mode=True)
      self.assertEqual(rs.renditions_dir, os.path.join(home, "_renditions_/some/root/path"))

          
  def test_pdf(self):
      self.cleanup()
      converter_stash = converters.Converters('converters', home = 'test')
      self.assertEqual(converter_stash.get_by_ext('.pdf').name, 'PDF')
      pdf_converter = converter_stash.get_by_ext('.pdf')("tests/uni-verse.cho.txt_key_C.pdf")
      self.assertEqual(pdf_converter.get_metadata()['dc:title'],'Universe')
      self.assertEqual(pdf_converter.get_metadata_item('dc:title'),'Universe')
      self.assertEqual(pdf_converter.get_mime(),"application/pdf")
      self.assertEqual(pdf_converter.renditions_store.thumb_path, "test/_renditions_/tests/thumbs/uni-verse.cho.txt_key_C.pdf.png")
      
  def test_jpg(self):
      self.cleanup()
      converter_stash = converters.Converters('converters', home = 'test')
      self.assertEqual(converter_stash.get_by_ext('.jpg').name, 'Image')
      img_converter = converter_stash.get_by_ext('.jpg')("tests/landscape.jpg")
      img_converter.get_metadata()
      self.assertEqual(img_converter.get_metadata_item('dc:title'),None)
      self.assertEqual(img_converter.get_mime(),"image/jpeg")
      self.assertEqual(img_converter.renditions_store.thumb_filename, "landscape.jpg.png")
      self.assertEqual(img_converter.renditions_store.thumb_path, "test/_renditions_/tests/thumbs/landscape.jpg.png")
      self.assertEqual(img_converter.get_viewable(), ("tests/landscape.jpg", "image/jpeg"))

      
  def test_office(self):
      self.cleanup()
      converter_stash = converters.Converters('converters', home = 'test')
      self.assertEqual(converter_stash.get_by_ext('.docx').name, 'Office')
      self.assertEqual(converter_stash.get_by_ext('.doc').name, 'Office')
      
    
if __name__ == '__main__':
    unittest.main()
