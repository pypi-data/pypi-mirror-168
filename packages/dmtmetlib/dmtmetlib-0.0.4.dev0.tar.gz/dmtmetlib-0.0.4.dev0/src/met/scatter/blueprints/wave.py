# Description for stochastic process at a sector.
# Generated with WaveBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class WaveBlueprint(Blueprint):
    """Description for stochastic process at a sector."""

    def __init__(self, name="Wave", package_path="met/scatter", description="Description for stochastic process at a sector."):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("occurence","number","the scatter data for occurrence of Hs-Tp.",Dimension("*"),Dimension("*"),default=0.0))