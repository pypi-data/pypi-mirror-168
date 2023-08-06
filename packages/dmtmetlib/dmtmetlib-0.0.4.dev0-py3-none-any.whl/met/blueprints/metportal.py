# Application entry
# Generated with MetPortalBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class MetPortalBlueprint(Blueprint):
    """Application entry"""

    def __init__(self, name="MetPortal", package_path="met", description="Application entry"):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(BlueprintAttribute("jobs","met/jobs/Job","",True,Dimension("*")))