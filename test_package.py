"""
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

import unittest
import package
import shutil
import os
import glob

class TestLoading(unittest.TestCase):
  def startup(self):
      self.test_packages = os.path.join('tests', 'test_packages', "*.json")
      self.temp_packages = os.path.join('tests', 'temp_packages')
      for file in glob.glob(self.test_packages):                                                                                                                                        
          shutil.copy(file, self.temp_packages)
          
  def test_simple_stufff(self):
      self.startup()
      path = os.path.join(self.temp_packages, "package1.json")
      p = package.Package(path)
      p.read()
      self.assertEqual(p.id, "1")
      self.assertEqual(p.name, "Package")
      dirs = p.dirs
      self.assertEqual(dirs[0].name, 'FOLDER 1')
      files = p.files
      self.assertEqual(len(files),0)
      files = dirs[0].files
      self.assertEqual(len(files),2)
      files = p.all_files
      self.assertEqual(len(files),5)
      print(files[0].path)


      bag = p.bag_me("test/bag1", overwrite=True, testmode=True)
      #Test validity

      p.zipped_bag("test/package1")

      
    
if __name__ == '__main__':
    unittest.main()
