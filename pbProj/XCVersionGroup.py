from .PBXItem import *

class XCVersionGroup(PBX_Base_Reference):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodesForArray(kPBX_REFERENCE_children, project)
        self.resolveGraphNodeForKey(kPBX_XCVERSIONGROUP_currentVersion, project)