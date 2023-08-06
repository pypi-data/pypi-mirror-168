# 
# Generated with MetVariableBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class MetVariableBlueprint(Blueprint):
    """"""

    def __init__(self, name="MetVariable", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("max","number","",default=0.0))
        self.attributes.append(Attribute("mean","number","",default=0.0))
        self.attributes.append(Attribute("min","number","",default=0.0))
        self.attributes.append(Attribute("size","integer","",optional=False,default=0))
        self.attributes.append(Attribute("standard_name","string","",default=""))
        self.attributes.append(Attribute("std","number","",default=0.0))
        self.attributes.append(Attribute("units","string","",optional=False,default=""))