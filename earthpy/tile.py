'''
dem.py
	Digital Elevation Model Utilities. Used for retrieval and processing of elevation data.
'''
# cache all files that intersect with the bbox. Split the data accordingly to match the tile size requests
import os
import shutil


# Tile grabber interface
class Grabber:
	def __init__(self, subclass, cache_dir_id):
		'''
			subclass - reference to inheriting class
			bbox - latlon bound to query
			raster_format - str representing the output format of raster
			raster_res - resolution of raster
			dimen - dimension of tiles grid to create from bbox. dimen is the  width and height of grid  
		'''
		self.subclass = subclass if subclass else self
		self.root_dir = os.path.abspath(os.path.dirname(__file__))
		self.cache_dir = os.path.join(self.root_dir, f'__{cache_dir_id}cache__') if cache_dir_id else None



	#---------- interface ----------------
	# Should return (raw data, filename ) as tuple
	def prepare_retrieve(self, latlon, end_latlon, res, format):
		pass


	# Should return raw data 
	def retrieve_tile(self, latlon, end_latlon, res, format):
		pass


	# ----------- actions ---------------------
	
	## TODO Create a cache max that calls clean after
	def retrieve_tiles(self, outdir, bbox, raster_format, raster_res, dimen, cache=False):
		
		self.subclass.prepare_retrieve(bbox)
		
		bbox_size = bbox[2]  - bbox[0], bbox[3]  - bbox[1]
		stride = bbox_size[0]/dimen[0] , bbox_size[1]/dimen[1] 
		#for each tile in grid, create a few threads and run. Calls retrieve_tile for each tile
		
		lon = bbox[1]
		for j in range(0, dimen[1] ):
			lat =bbox[0]
			for i in range(0, dimen[0] ):
				# TODO - thread this.
				raw_data = self.subclass.retrieve_tile( (lat, lon), (lat+stride[0], lon+stride[1]), raster_res, raster_format)
				
				filename = f'Tile_x{i}_y{j}.{raster_format}'
				filename = os.path.join(outdir, filename)
				self.save_tile(raw_data, filename)

				lat += stride[0]
			lon += stride[1]
		if cache:
			self.clean_cache()


	def clean_cache(self):
		if not self.cache_dir is None:
			shutil.rmtree(self.cache_dir)


	# ----------- helpers  ---------------------

	# called adfter tile is retrieved!
	def save_tile(self,raw_data, filename):
		if raw_data:
			os.makedirs(os.path.dirname(filename), exist_ok=True)
			with open(filename, "wb") as f:
				f.write(raw_data)



