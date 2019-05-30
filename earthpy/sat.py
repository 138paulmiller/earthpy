import grabber


import urllib
import numpy as np
import os

# styles from https://maps.eox.at/


 
   
class SAT(grabber.Grabber):
	def __init__(self,subclass = None):
		self.subclass = subclass
		super().__init__(self, raster_formats=('png', 'jpg', 'jpeg'))

 	
	def prepare_retrieve(self, bbox):
		pass
		
	def retrieve_tile(self, latlon, end_latlon, res, format):
		print('super')
		return None
		

	def sat_image_get_url (self,  latlon, end_latlon, width, height, style):
		
		server_wms = 'https://tiles.maps.eox.at/wms?service=wms&request=getmap&version=1.1.1'
		url = f'{server_wms}&layers={style}&bbox={latlon[0]:.8f},{latlon[1]:.8f},{end_latlon[0]:.8f},{end_latlon[1]:.8f}&width={width}&height={height}&srs=epsg:4326' 
		return url
		
	def check_url(self, url):
		try:
			u = urllib.urlopen(url)
			u.close()
			return True
		except:
			return False
		
	def load_sat_file(self, latlon, end_latlon, res, style, format):
		width,height = res

		filepath = self.sat_image_get_filepath(latlon, end_latlon, width, height, style, format) 

		cachefile =	 os.path.join(self.cache_dir, filepath)
		url = self.sat_image_get_url(latlon, end_latlon, width, height, style) 
		# search for filename in cache. If exists do nothing
		if not os.path.exists( cachefile ):
			print(f'Caching{cachefile}')
			# create dirs for path
			os.makedirs(os.path.dirname(cachefile), exist_ok=True)
			#if self.check_url(url):
			urllib.request.urlretrieve(url, cachefile)
			#else:
			#	print(f'Failed to get {url}')
		#raster = np.memmap(cachefile, shape =res, mode = 'r').reshape(self.source_res)

		return cachefile 
		
	def	sat_image_get_filepath(self, latlon, end_latlon, width, height, style, format):
		# mkdir for style			
		
		lat,lon = latlon
		filename = f'{lat}_{lon}_{width}x{height}.{format}'
		filepath =os.path.join(style, filename)
		return filepath

		
class VectorSAT(SAT):
	def __init__(self):
		super().__init__(self)
		
		
	def retrieve_tile(self, latlon, end_latlon, res, format):
		return self.load_sat_file(latlon, end_latlon, res, 'terrain-light', format)


		
class SentinelSAT(SAT):
	def __init__(self):
		super().__init__(self)
		
		
	def retrieve_tile(self, latlon, end_latlon, res, format):
		return self.load_sat_file(latlon, end_latlon, res, 's2cloudless', format)
		
		