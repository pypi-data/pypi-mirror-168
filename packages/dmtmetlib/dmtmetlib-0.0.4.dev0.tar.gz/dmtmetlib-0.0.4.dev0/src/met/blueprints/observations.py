# 
# Generated with ObservationsBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute

class ObservationsBlueprint(Blueprint):
    """"""

    def __init__(self, name="Observations", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.attributes.append(Attribute("name","string","",default=""))
        self.attributes.append(Attribute("description","string","",default=""))
        self.attributes.append(Attribute("Conventions","string","",optional=False,default=""))
        self.attributes.append(Attribute("NCO","string","",default=""))
        self.attributes.append(Attribute("buoy_manufacturer","string","",optional=False,default=""))
        self.attributes.append(Attribute("buoy_serialno","string","",optional=False,default=""))
        self.attributes.append(Attribute("buoy_type","string","",optional=False,default=""))
        self.attributes.append(Attribute("data_collecting_contractor","string","",optional=False,default=""))
        self.attributes.append(Attribute("data_owner","string","",optional=False,default=""))
        self.attributes.append(Attribute("date_created","string","",optional=False,default=""))
        self.attributes.append(Attribute("featureType","string","",default=""))
        self.attributes.append(Attribute("geospatial_lat_max","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_lat_min","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_lon_max","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_lon_min","number","",optional=False,default=0.0))
        self.attributes.append(Attribute("geospatial_vertical_positive","string","",optional=False,default=""))
        self.attributes.append(Attribute("history","string","",optional=False,default=""))
        self.attributes.append(Attribute("keywords","string","",optional=False,default=""))
        self.attributes.append(Attribute("keywords_vocabulary","string","",optional=False,default=""))
        self.attributes.append(BlueprintAttribute("latitude","met/MetVariable","",True))
        self.attributes.append(Attribute("licence","string","",optional=False,default=""))
        self.attributes.append(BlueprintAttribute("longitude","met/MetVariable","",True))
        self.attributes.append(Attribute("measurement_update_period","string","",optional=False,default=""))
        self.attributes.append(Attribute("modified","string","",optional=False,default=""))
        self.attributes.append(Attribute("netcdf_version","string","",optional=False,default=""))
        self.attributes.append(Attribute("position_ref","string","",optional=False,default=""))
        self.attributes.append(Attribute("processing_level","string","",optional=False,default=""))
        self.attributes.append(Attribute("publisher_email","string","",optional=False,default=""))
        self.attributes.append(Attribute("publisher_name","string","",optional=False,default=""))
        self.attributes.append(Attribute("publisher_url","string","",optional=False,default=""))
        self.attributes.append(Attribute("sensor_level","string","",optional=False,default=""))
        self.attributes.append(Attribute("sensor_manufacturer","string","",optional=False,default=""))
        self.attributes.append(Attribute("sensor_serialno","string","",optional=False,default=""))
        self.attributes.append(Attribute("sensor_type","string","",optional=False,default=""))
        self.attributes.append(Attribute("station_name","string","",optional=False,default=""))
        self.attributes.append(Attribute("status","string","",default=""))
        self.attributes.append(Attribute("summary","string","",optional=False,default=""))
        self.attributes.append(BlueprintAttribute("time","met/MetVariable","",True))
        self.attributes.append(Attribute("time_coverage_end","string","",optional=False,default=""))
        self.attributes.append(Attribute("time_coverage_start","string","",optional=False,default=""))
        self.attributes.append(Attribute("title","string","",optional=False,default=""))
        self.attributes.append(Attribute("url","string","",optional=False,default=""))
        self.attributes.append(Attribute("water_depth","string","",optional=False,default=""))