""" Generic converter which just inherits the metadata """



class GenericConverter(FileType):
    name = "Generic"
    exts = ["*"]
    viewable = True
    
    
    def __init__(self, file):
        self.setup(file)
        


# This is called from the __init__ method of converters.Converters
self.register(GenericConverter)
