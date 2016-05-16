""" Deal with operations on PDF """



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
