# 
# Generated with JobResultBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class JobResultBlueprint(Blueprint):
    """"""

    def __init__(self, name="JobResult", package_path="met/jobs", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("progress","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("result","string","",optional=False,default=""))
        self.attributes.append(Attribute("wind_speed","number","",Dimension("*"),default=0.0))
        self.attributes.append(Attribute("wind_direction","number","",Dimension("*"),default=0.0))