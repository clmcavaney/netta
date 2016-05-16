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
