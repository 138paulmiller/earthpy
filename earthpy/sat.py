import grabber



styles = ['bluemarble', 's2cloudless'] 

sat_image_get_url = lambda lon, lat, endlon, endlat, width, height, style  : \
	"https://tiles.maps.eox.at/wms?service=wms&request=getmap&version=1.1.1&layers={style}&bbox={lon:.8f},{lat:.8f},{endlon:.8f},{endlat:.8f}&width={width}&height={height}&srs=epsg:4326" 
 
# asnchrounously grab the tiles that intersect with the bbox. Download from server if they do not exist in cache
# Base class
class SAT(grabber.Grabber):
	def __init__(self):
		super().__init__(self, raster_formats=('png') )

		
	def prepare_retrieve(self, bbox):
		pass
		
	def retrieve_tile(self, latlon, end_latlon, res, format):
		pass    
