# Description for stochastic process at a sector.
# Generated with WindCurrentBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class WindCurrentBlueprint(Blueprint):
    """Description for stochastic process at a sector."""

    def __init__(self, name="WindCurrent", package_path="met/scatter", description="Description for stochastic process at a sector."):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("level","number","measured level.",default=0.0))
        self.attributes.append(Attribute("speed","number","the scatter data for speed.",Dimension("*"),Dimension("*"),default=0.0))
        self.attributes.append(Attribute("direction","number","the scatter data for direction.",Dimension("*"),Dimension("*"),default=0.0))