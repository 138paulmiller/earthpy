
STYLES = ['bluemarble', 's2cloudless'] 

SAT_IMAGE_GET = lambda lon, lat, endlon, endlat, width, height, style  : \
    "https://tiles.maps.eox.at/wms?service=wms&request=getmap&version=1.1.1&layers={style}&bbox={lon:.8f},{lat:.8f},{endlon:.8f},{endlat:.8f}&width={width}&height={height}&srs=epsg:4326" 
 
CACHE_DIR = path.join(path.abspath(path.dirname(__file__)), '__demcache__')

# asnchrounously grab the tiles that intersect with the bbox. Download from server if they do not exist in cache
