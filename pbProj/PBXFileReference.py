from .PBXItem import *

class PBXFileReference(PBX_Base_Reference):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)