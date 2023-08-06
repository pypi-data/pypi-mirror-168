# 
# Generated with JobRunnerBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class JobRunnerBlueprint(Blueprint):
    """"""

    def __init__(self, name="JobRunner", package_path="met/jobs", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("lat","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("lon","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("fromDate","string","",optional=False,default=""))
        self.attributes.append(Attribute("toDate","string","",default=""))
        self.attributes.append(BlueprintAttribute("result","met/jobs/JobResult","",True))