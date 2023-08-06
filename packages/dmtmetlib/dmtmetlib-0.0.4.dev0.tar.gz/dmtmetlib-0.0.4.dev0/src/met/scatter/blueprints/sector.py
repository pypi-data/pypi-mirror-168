# Description for stochastic process at a sector.
# Generated with SectorBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class SectorBlueprint(Blueprint):
    """Description for stochastic process at a sector."""

    def __init__(self, name="Sector", package_path="met/scatter", description="Description for stochastic process at a sector."):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("direction","number","sector direction.",default=0.0))
        self.attributes.append(Attribute("sectorSize","number","sector size.",default=0.0))
        self.attributes.append(BlueprintAttribute("wave","met/scatter/Wave","the scatter data for wave.",True))
        self.attributes.append(BlueprintAttribute("wind","met/scatter/WindCurrent","the scatter data for wind at different levels.",True,Dimension("*")))
        self.attributes.append(BlueprintAttribute("current","met/scatter/WindCurrent","the scatter data for current at different levels.",True,Dimension("*")))