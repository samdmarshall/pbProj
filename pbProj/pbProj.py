from __future__ import absolute_import
from .pbPlist.pbPlist import PBPlist
from .PBX_Constants import *
from .PBX_Lookup import *

class PBXProj(object):
    
    def __init__(self, file_path):
        plist = PBPlist(file_path)
        
        contents = plist.root.nativeType()
        
        self.pbxObjects = set()
        self.pbxIdentifier = None
        self.pbxRootObject = None
        self.pbxObjectVersion = 0
        self.pbxArchiveVersion = 0
        if contents != None:
            # get the path that we read from
            self.pbxFilePath = plist.file_path
            
            # get the root object identifier
            self.pbxIdentifier = contents.get(kPBX_rootObject, None)
            
            # get the archive version number
            archive_version = contents.get(kPBX_archiveVersion, None)
            if archive_version:
                self.pbxArchiveVersion = int(str(archive_version))
            
            # get the object version number
            object_version = contents.get(kPBX_objectVersion, None)
            if object_version:
                self.pbxObjectVersion = int(str(object_version))
            
            # get the classes
            self.pbxClasses = contents.get(kPBX_classes, None)
            
            # get all the objects
            objects_dict = contents.get(kPBX_objects, None)
            
            for entry in objects_dict.keys():
                entry_dict = objects_dict.get(entry, None)
                if entry_dict:
                    object_item = PBX_Type_Resolver(entry, entry_dict)
                    self.pbxObjects.add(object_item)
            
            self.pbxRootObject = self.objectForIdentifier(self.pbxIdentifier) 
            self.pbxRootObject.resolveGraph(self)
            
    def __repr__(self):
        if self.isValid():
            return '<%s : %s : %s>' % (type(self), self.pbxFilePath, self.pbxIdentifier)
        else:
            return '<%s : INVALID OBJECT>' % (type(self))
    
    def __attrs(self):
        return (self.pbxIdentifier, self.pbxFilePath)

    def __eq__(self, other):
        return isinstance(other, PBXProj) and self.pbxIdentifier == other.pbxIdentifier and self.pbxFilePath == other.pbxFilePath

    def __hash__(self):
        return hash(self.__attrs())
    
    def isValid(self):
        return self.pbxIdentifier != None
        
    def objectForIdentifier(self, identifier):
        """
        Returns the parsed object from the project file for matching identifier, if no matching object is found it will return None.
        """
        result = None
        if self.isValid():
            filter_results = filter(lambda obj: obj.identifier == identifier, self.pbxObjects)
            if len(filter_results) > 0:
                result = filter_results[0]
        return result
    
    def targets(self):
        """
        This method will return a list of build targets that are associated with this xcodeproj.
        """
        targets = list()
        if self.isValid():
            targets.extend(self.rootObject.targets)
        return targets