import json
import os
import shutil
import random
import bagit
import tempfile
import re

class BagIsFile(Exception):
    pass

class BagDirExists(Exception):
    pass

class Package:
    """ 
    Class for dealing with abstract heirarchical file packages 
    built around the JSTree JSON format for convenience but with an interface that is useful for 
    building packages of files such as bagit, or EPUB.
    """
    def slugify(value):
    
        """
        Create a file-system safe version of a string 
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens. From:
        http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python

        """
        import unicodedata
        value = str(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'))
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        value = re.sub('[-\s]+', '-', value)
        return(value)
        
 
    def __init__(self, path = None):
        """Initialise with a place to store, normally needs to be populated with a json string created at the client side using JStree"""
        if path:
            self.package_export_dir = os.path.join(os.path.expanduser("~"), "netta_packages") # For saved zips etc

            if not os.path.exists(self.package_export_dir):
                os.makedirs(self.package_export_dir)
            self.path = os.path.join(self.package_export_dir, path)

    @classmethod
    def __from_dir(self, dir):
        """Treat a JSTree directory node as a kind of package"""
        p = Package()
        p.content = [dir]
        return p
        
    def save(self, content):
        """ Save data from jstree without validation """
        
        with open(self.path, "w") as package:
            package.write(json.dumps(content))
            self.content = content
        return ("yep")

    def read(self):
        if not os.path.exists(self.path):
            self.save( [{"a_attr": {"id": "1_anchor", "href": "#"}, "id": "1", "icon": "/static/themes/default/tree_icon.png", "children": [], "type": "root", "data": {}, "state": {"selected": False, "disabled": False, "opened": True, "loaded": True}, "li_attr": {"id": "1"}, "text": "Package"}])
        
        with open(self.path, "r") as package:
            content = package.read()
            self.content = json.loads(content)
        return(content)
    @property
    def id(self):
        return self.content[0]["id"]
    
    @property
    def name(self):
        return self.content[0]["text"] 
    
    @property
    def dirs(self):
         return([Package.__from_dir(dir) for dir in self.content[0]["children"] if dir["type"] == "dir"])
     
    @property
    def files(self):
        """Return all the files under this node"""
        return([File(f) for f in self.content[0]["children"] if f["type"] == "file"])
    
    @property
    def all_files(self):
        """Return all files in tree recursive"""
        files = self.files
        for dir in self.dirs:
            files += dir.all_files
        return files

    def bag_me(self, path, overwrite = False, testmode= False):
        """ 
        Creates a new bag for the package - will over-write if overwrite is True
        in testmode will create files in the target dir whether or not they exist
        """
        # Housekeeping first, deal with existing dir etc
        path = os.path.abspath(path)
        if os.path.exists(path):
            if os.path.isdir:
                if overwrite:
                    shutil.rmtree(path)
                else:
                    raise BagDirExists("Bag dir {path} already exists".format(path=path))
                #remove
            else:
                raise BagIsFile("{path} is a file!")
        #Make a place for the bag
        os.makedirs(path)
        #copy all the files into the bag
        for f in self.all_files:
            c = os.path.commonpath([os.path.abspath(path), f.path])
            new_path = os.path.join(path, f.path.replace(c,"."))
            new_dir,_ = os.path.split(new_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            if testmode:
                contents = random.random()
                with open(new_path, "w") as new_file:
                    new_file.write(str(random.random()))
            else:
                #TODO - Deal with Directories as well!
                shutil.copyfile(f.path, new_path)
                
        bag = bagit.make_bag(path)
        self.bag = bag
        return bag
                
    def zipped_bag(self, path):
        """Create a zipped bag, via a temp directory"""
        bag_path = os.path.join(path,".bag") # TODO tempfile.mkdtemp() didn't work
        self.bag_me(bag_path, overwrite=True)
        outpath = os.path.join(self.package_export_dir, self.name)
        shutil.make_archive(outpath, 'zip', bag_path)
        shutil.rmtree(bag_path)
        
        
                
            

class File:
    """Helper data structure for file-nodes in JSTrees"""
    def __init__(self, data):
        """Initialised with JSTree node"""
        self.__id = data["id"]
        self.__name = data["text"]
        self.__path = data['data']['href']
        self.__data = data['data']

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path
    
    @property
    def data(self):
        return self.__data
