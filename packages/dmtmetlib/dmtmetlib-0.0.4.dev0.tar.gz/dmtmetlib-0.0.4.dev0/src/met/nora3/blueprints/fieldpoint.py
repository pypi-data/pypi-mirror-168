# 
# Generated with FieldPointBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class FieldPointBlueprint(Blueprint):
    """"""

    def __init__(self, name="FieldPoint", package_path="met/nora3", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("latitude","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("longitude","number","",optional=False,default=0.0))