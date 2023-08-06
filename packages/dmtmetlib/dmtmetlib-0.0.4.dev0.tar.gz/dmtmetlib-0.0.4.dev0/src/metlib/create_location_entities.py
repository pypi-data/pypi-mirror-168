import json
import os
from pathlib import Path
from typing import Dict, List

from dmt.dmt_writer import DMTWriter

from met.scatter.sector import Sector
from met.scatter.wave import Wave
import met.scatter as met_scatter

from .scatter import Scatter


def __create_entities(path,bp_path):
    entities = {}
    for prefix in ["wave","wind"]:
        bp_name = __find_bp_name(prefix)
        bp_type = bp_path+bp_name
        __create_entites_of_type(entities,path,prefix,bp_type,bp_path)
        
    return entities

def __find_bp_name(prefix):
    name = prefix.capitalize()
    if name == "10min":
        return "SampledObservations"
    return name

def __create_entites_of_type(entities, path, prefix,bp_type, bp_path):
    for root, _, files in os.walk(path):
        for filename in files:
            ending = "_" + prefix+".nc.json"
            if filename.endswith(ending):
                file = Path(os.path.join(root, filename))
                idx = len(filename)-len(".nc.json")
                name = filename[0:idx]
                with open(file, 'r') as fp:
                    res=json.load(fp)
                    entity = __create_entity(res, bp_type,bp_path)
                    if name in entities:
                        raise ValueError("Duplicate entry " + name)
                    entity["name"] = name
                    entities[name]=entity

def __create_entity(obj,type, bp_path):
    entity= {
        "type":type,
        "description": ""
    }
    for pname,prop in obj.items():
        if pname == "global_attributes":
            __populate_entity(entity,prop)
        elif pname == "variables":
            for name,variable in prop.items():
                var_entity = {
                "type":bp_path + "MetVariable",
                "description": ""
                }
                __populate_entity(var_entity,variable)
                entity[name]=var_entity
        elif pname not in ["name","path"]:
            entity[pname]=prop
    
    __populate_entity(entity, obj["global_attributes"])
    
    for name,variable in obj["variables"].items():
        var_entity = {
            "type":bp_path + "MetVariable",
            "description": ""
        }
        __populate_entity(var_entity,variable)
        entity[name]=var_entity
    return entity

def __populate_entity(entity:Dict, vars:Dict):
    for name,variable in vars.items():
        if name == "keywords":
            #FIXME We should handle this in the first stage
            if isinstance(variable, List):
                variable = ", ".join(variable)
        entity[name]=variable

def __create_location_entity(name,bp_path):
    return {
        "type" :  bp_path + "Location",
        "name": name,
        "waves": [],
        "winds": []
    }

def __create_and_sort_entities(path,locations: Dict,bp_path):
    entities = __create_entities(path,bp_path)
    for observation in entities.values():
        stype=observation["type"][len(bp_path):].lower()
        sname = observation.get("station_name")
        name = sname.replace(" ","_")
        location=locations.get(name)
        if not location:
            location = __create_location_entity(name,bp_path)
            locations[name] = location
        relation = stype + "s"
        observations:list = location[relation]
        observations.append(observation)

        for prop in ["geospatial_lat_min","geospatial_lon_min"]:
            vmin = observation[prop]
            location[prop] = min(location.get(prop,vmin),vmin)

        for prop in ["geospatial_lat_max","geospatial_lon_max"]:
            vmax = observation[prop]
            location[prop] = max(location.get(prop,vmax),vmax)

def __create_wave_scatter(scatter: Scatter):
    hs_upper = scatter.upper_rows()
    tp_upper = scatter.upper_columns()
    occurences=scatter.occurences()
    m_scatter = met_scatter.Scatter(name="omni")

    m_scatter.hsUpperLimits = list(hs_upper)
    m_scatter.tpUpperLimits = list(tp_upper)
    wave = Wave()
    wave.occurence = occurences.tolist()
    omni = Sector(name="omni",wave=wave)
    m_scatter.omni = omni

    return DMTWriter().to_dict(m_scatter)

def __add_datasource(entity: Dict,data_source:str):
    entity["type"] = data_source + entity["type"]
    for value in entity.values():
        if isinstance(value,dict):
            __add_datasource(value,data_source)
    

def __compute_location_scatter(location: Dict,data_source:str):
    waves = location.get("waves",[])
    location_wave_scatter = None
    for wave in waves:
        # Remove the scatter from the individual observation
        # And combine it in the location scatter
        scatter_dict = wave.pop("scatter",None)
        if scatter_dict:
            bin_size = scatter_dict["bin_size"]
            bins = scatter_dict["wave"]
            wave_scatter = Scatter(bin_size,bins)
            if location_wave_scatter is None:
                location_wave_scatter = wave_scatter
            else:
                location_wave_scatter.combine(wave_scatter)
    
    if location_wave_scatter:
        scatter = __create_wave_scatter(location_wave_scatter)
        __add_datasource(scatter,data_source)

        waveDirs=location_wave_scatter.get("waveDir")
        wave = Wave()
        wave.occurence = waveDirs.tolist()
        meanWaveDir = location_wave_scatter.mean_of("waveDir")
        waveDirScatter = DMTWriter().to_dict(wave)
        __add_datasource(waveDirScatter,data_source)

        location["waveScatter"]= scatter
        location["waveDirScatter"]= waveDirScatter
        location["meanWaveDirection"]= meanWaveDir

        (hs,tp) = location_wave_scatter.mean_xy()
        location["meanHs"]= hs
        location["meanTp"]= tp

def create_location_entities(input_path: Path, data_source="") -> Dict:
    """
    Read the files in the given folder and convert to location entities
    """
    met_bp_path ="met/"
    locations = {}
    __create_and_sort_entities(input_path,locations,data_source+met_bp_path)    
    
    for location in locations.values():
        __compute_location_scatter(location,data_source)
    
    return locations
