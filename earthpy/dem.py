'''
dem.py
    Digital Elevation Model Utilities. Used for retrieval and processing of elevation data.
'''
# cache all files that intersect with the bbox. Split the data accordingly to match the tile size requests
from os import path
import shutil

'''
If using default server:
Directory structure 
 SRTM_GL1/
    SRTM_GL1_srtm/
        North/
            North_0_29/
                N30E006.hgt
                ...
            North_30_60/
                N30E000.hgt
                ... 
        South/
            S01E006.hgt
            ...
'''
SRTM1_SERVER="https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/SRTM_GL1/"
 
CACHE_DIR = path.join(path.abspath(path.dirname(__file__)), '__demcache__')

# asnchrounously grab the tiles that intersect with the bbox. Download from server if they do not exist in cache



class DEM:
    def __init__(self, bbox, format, res, dimen, cache):
        self.bbox = bbox
        self.format = format
        self.output_res = res
        self.grid_shape = dimen, dimen 
        self.should_cache = should_cache
    
    
    def retrieve_tiles(self):
        #for each tile in grid, create a few threads and run. Calls retrieve_tile for each tile
        pass 
    
    
    def clean_cache(self):
        shutil.rmtree(CACHE_DIR)


# Base class
class DEMRunner:
    def __init__(self, bbox, format, res, dimen, cache):
        self.bbox = bbox
        self.format = format
        self.output_res = res
        self.tile = None
        self.should_cache = should_cache
    
    # --------------- interface ----------------
    
    # grab or download the tile. Load into memory, process, reformat. Then save to file
    # to be run async on run
    def retrieve_tile(self, x, y):
        pass
    

class SRTMRunner(DEMRunner):
    def __init__(self, bbox, format, res, dimen, cache):
        self.__super__(bbox, format, res, dimen, cache)

        
    def retrieve_tile(self, x, y):
        pass    
        
        
        