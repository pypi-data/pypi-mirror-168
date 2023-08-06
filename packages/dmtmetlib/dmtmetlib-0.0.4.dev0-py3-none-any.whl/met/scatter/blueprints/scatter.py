# Description for scatter data based on Hs-Tp.
# Generated with ScatterBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class ScatterBlueprint(Blueprint):
    """Description for scatter data based on Hs-Tp."""

    def __init__(self, name="Scatter", package_path="met/scatter", description="Description for scatter data based on Hs-Tp."):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","name for the scatter data as appear in SIMA.",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("hsUpperLimits","number","upper limits of the boundaries for each row in the scatter data.",Dimension("*"),default=0.0))
        self.attributes.append(Attribute("tpUpperLimits","number","upper limits of the boundaries for each column in the scatter data.",Dimension("*"),default=0.0))
        self.attributes.append(Attribute("seaStateDuration","number","duration of sea state.",default=0.0))
        self.attributes.append(Attribute("countingPeriod","number","the duration which is used to count the occurrence of events.",default=0.0))
        self.attributes.append(BlueprintAttribute("sectors","met/scatter/Sector","sector scatter data.",True,Dimension("*")))
        self.attributes.append(BlueprintAttribute("omni","met/scatter/Sector","omni scatter data.",True))