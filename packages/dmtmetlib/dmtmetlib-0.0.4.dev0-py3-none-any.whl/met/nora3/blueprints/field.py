# 
# Generated with FieldBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class FieldBlueprint(Blueprint):
    """"""

    def __init__(self, name="Field", package_path="met/nora3", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("label","string","",optional=False,default=""))
        self.attributes.append(Attribute("latitude","number","",Dimension("*"),default=0.0))
        self.attributes.append(Attribute("longitude","number","",Dimension("*"),default=0.0))
        self.attributes.append(BlueprintAttribute("points","met/nora3/FieldPoint","",True,Dimension("*")))