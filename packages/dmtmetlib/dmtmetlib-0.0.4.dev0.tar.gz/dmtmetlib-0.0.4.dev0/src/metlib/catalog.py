
import json
import math
import os
import shutil
from pathlib import Path
from typing import Dict, Sequence
from urllib.request import urlopen
from xml.dom.minidom import Document, Element, parse

from numpy import ndarray
from netCDF4 import Dataset
import numpy as np
import requests
from tqdm.auto import tqdm
from .scatter import Scatter
from .jsonencoder import JsonCustomEncoder

class Progress():
    
    def __init__(self) -> None:
        self.worked = 0.0
        self.total = 0.0
    
    def increment_total(self, incr):
        self.total=self.total+incr

    def increment_worked(self, incr):
        self.worked=self.worked + incr
        
    def progress(self) -> float:
        if self.total == 0:
            return 0.0
        return self.worked / self.total
    
    def done(self):
        self.worked = 1.0
        self.total = 1.0
        
class RejectingDict(dict):
    def __setitem__(self, k, v):
        if k in self.keys():
            raise ValueError("Key is already present")
        else:
            return super(RejectingDict, self).__setitem__(k, v)


class Catalog:

    def __init__(self, bin_size, progress=Progress()) -> None:
        self.bin_size=bin_size
        self.progress = progress

    def __read_catalog(self,path:Path, base: str, id:str,level,stop_level) -> Dict:
        """Reads the catalog.xml recursively down to a certain level"""
        if level == stop_level:
            return

        var_url = urlopen(base+id+'/catalog.xml')
        xmldoc: Document = parse(var_url)
        catalog: Element = xmldoc.getElementsByTagName('catalog')[0]
        dataset: Element = catalog.getElementsByTagName('dataset')[0]
        name = dataset.getAttribute("name")
        cat_dict = {
            "name":name
        }

        folder = path / name
        folder.mkdir(exist_ok=True)

        cat_file: Path = folder / 'catalog.xml'

        with open(cat_file, 'w') as file:
            xmldoc.writexml(file)

        catalogRefs: Sequence[Element] = dataset.getElementsByTagName('catalogRef')
        datasets: Sequence[Element] = dataset.getElementsByTagName('dataset')
        offset = "\t" * level
        print(offset+"Dataset: "+name+":")
        print(offset+str(folder.absolute()))
        print(offset+str(len(datasets)) + ' datasets')

        cat_sets = {}
        cat_dict["datasets"]=cat_sets
        for ref in datasets:
            name: str=ref.getAttribute('name')
            path: str=ref.getAttribute('urlPath')
            url = 'https://thredds.met.no/thredds/fileServer/'+path
            set_dict =   {
                "name":name,
                "path":path,
                "url":url
            }
            cat_sets[name]=set_dict

            dates=ref.getElementsByTagName('date')
            if len(dates) == 1:
                # <date type="modified">2019-06-27T11:41:51Z</date>
                date:Element = dates[0]
                if date.getAttribute("type") == "modified":
                    value: Element = date.firstChild
                    sdate  = value.nodeValue
                    set_dict["modified"] = sdate

        cat_cats = {}
        cat_dict["catalogs"]=cat_cats
        for ref in catalogRefs:
            title: str=ref.getAttribute('xlink:title')
            if title.isdigit():
                refid = ref.getAttribute('ID')
                cat_ref = self.__read_catalog(folder,base,refid,level+1,stop_level)
                if cat_ref:
                    cat_cats[cat_ref["name"]]=cat_ref
        
        return cat_dict

    def __convert_size(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def __download(self,url: str, dfile: Path):
        # make an HTTP request within a context manager
        with requests.get(url, stream=True, allow_redirects=True) as r:
            # check header to get content length, in bytes
            total_length = int(r.headers.get("Content-Length"))
            print('Downloading ' + url + ', ' + self.__convert_size(total_length))
            
            # implement progress bar via tqdm
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
            
                # save the output to a file
                with open(dfile, 'wb')as output:
                    shutil.copyfileobj(raw, output)

    def __store_dataset_locally(self,dataset: Dict, dfile: Path):
        name = dataset["name"]
        with open(dfile.parent / (name + ".json"), "w") as fp:
            json.dump(dataset, fp, indent=4, cls=JsonCustomEncoder)

    def __download_catalog(self,path:Path, catalog: Dict, update_progress: bool):
        name = catalog["name"]
        folder = path / name
        print('Checking ' + str(folder))
        folder.mkdir(exist_ok=True)

        datasets= catalog.get("datasets",{})

        for name, dataset in datasets.items():
            dfile: Path = folder / name
            if self.__should_download(dataset,folder):
                if update_progress:
                    self.progress.increment_total(1.0)
                else:
                    url = dataset["url"]
                    self.__download(url,dfile)
                    self.progress.increment_worked(1.0)
            if dfile.exists() and not update_progress:
                self.__read_dataset(dfile, dataset)
                self.__store_dataset_locally(dataset,dfile)
                # We will delete after relevant data is found
                os.remove(dfile)
        
        catalogs = catalog.get("catalogs",{})
        for name,cat in catalogs.items():
            self.__download_catalog(folder,cat,update_progress)

    def __should_download(self,dataset:Dict, folder: Path):
        name = dataset["name"]
        if "raw" in name:
            return False

        if "_wave" in name or "_wind" in name:
            ncfile = folder / name
            jsonfile = folder / (name +".json")
            if ncfile.exists() and not jsonfile.exists():
                return False
            if jsonfile.exists():
                with open(jsonfile, 'r') as file:
                    observation = json.load(file)
                    # Check to see if the timestamp matches
                    if dataset["modified"] == observation["modified"]:
                        return False
                    else:
                        return True


            return True
        return False

    def __read_dataset(self,path, metadata):
        rootgrp = Dataset(path, "r")
        global_attributes = {}
        metadata["global_attributes"] = global_attributes
        for name in rootgrp.ncattrs():
            value = getattr(rootgrp, name)
            if isinstance(value, str):
                global_attributes[name] = value
            else:
                if isinstance(value, list):
                    global_attributes[name] = value
                elif value.ndim > 0:
                    global_attributes[name] = list(value[:])
                else:
                    global_attributes[name] = value.item()
        variables = {}
        metadata["variables"] = variables
        hs = None
        for name, var in rootgrp.variables.items():
            variable = (
                RejectingDict()
            )  # Make sure we do not overwrite any already existing keys
            variables[name] = variable
            self.__handle_variable(variable, var)
            for key, value in var.__dict__.items():
                if isinstance(value, str):
                    variable[key] = value
                else:
                    if value.ndim > 0:
                        variable[key] = list(value[:])
                    else:
                        variable[key] = value.item()

        hm0 = rootgrp.variables.get("Hm0")
        if hm0:
            tps = rootgrp.variables.get("tp")
            mdir = rootgrp.variables.get("mdir")
            wave_scatter = Scatter()
            
            hs_values = self.__get_values({},hm0)
            tp_values = self.__get_values({},tps)
            dirs: ndarray = self.__get_values({},mdir)
            for (hs,tp, dir) in zip(hs_values,tp_values,dirs):
                if not math.isnan(hs):
                    wave_scatter.add(hs,tp,waveDir=dir)
            
            metadata["scatter"] = {
                "bin_size": wave_scatter.bin_size,
                "wave": wave_scatter.bins,
            }
            
            
        rootgrp.close()

    def __get_values(self,variable, var)->ndarray:
        meta = var.__dict__
        missing_value=meta.get("_FillValue",meta.get("missing_value"))
        values: ndarray = var[:]
        if missing_value:
            if np.ma.is_masked(values):
                variable["has_missing_values"] = True
        return values

    def __handle_variable(self,variable, var):
        values: ndarray = self.__get_values(variable,var)
        size = values.size
        variable["size"] = size
        min = values.min().item()
        if not math.isnan(min):
            variable["min"] = min
            if size==1:
                variable["mean"] = min
                variable["max"] = min
                variable["std"] = 0.0
            else:
                variable["mean"] = values.mean().item()
                variable["max"] = values.max().item()
                variable["std"] = values.std().item()
        else:
            variable["has_missing_values"] = True

    def __read_catalogs(self,path:Path) -> Sequence[Dict]:
        catalogs = []
        base = 'https://thredds.met.no/thredds/catalog/'
        for id,level in [['obs/buoy-svv-e39',3]]:
            cat_dict = self.__read_catalog(path,base,id,0,level)
            catalogs.append(cat_dict)
        return catalogs

    def __download_catalogs(self,path:Path, update_progress):
        for catalog in self.__read_catalogs(path):
            folder = path / catalog["name"]
            with open(folder / 'catalog.json', 'w') as file:
                json.dump(catalog,file)
            self.__download_catalog(path,catalog,update_progress)

    def download_catalogs(self,path:Path):
        self.__download_catalogs(path,True)
        self.__download_catalogs(path,False)
        self.progress.done()

