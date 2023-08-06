# 
# Generated with LocationBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class LocationBlueprint(Blueprint):
    """"""

    def __init__(self, name="Location", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("geospatial_lat_min","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_lat_max","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_lon_min","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_lon_max","number","",optional=False,default=0.0))
        self.attributes.append(BlueprintAttribute("waves","met/Wave","",True,Dimension("*")))
        self.attributes.append(BlueprintAttribute("winds","met/Wind","",True,Dimension("*")))
        self.attributes.append(BlueprintAttribute("waveScatter","met/scatter/Scatter","",True))
        self.attributes.append(BlueprintAttribute("waveDirScatter","met/scatter/Wave","",True))
        self.attributes.append(Attribute("meanWaveDirection","number","",default=0.0))
        self.attributes.append(Attribute("meanHs","number","",default=0.0))
        self.attributes.append(Attribute("meanTp","number","",default=0.0))