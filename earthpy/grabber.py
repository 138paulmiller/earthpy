# cache all files that intersect with the bbox. Split the data accordingly to match the tile size requests
import os
import shutil

dataset_to_grabber_map = {}
# call to register support for new dataset
# dataset - string representaion of dataset
# grabber - class that inherits Grabber formatted as "module.classname" where module is module.py
def add(dataset, grabber ):
	global dataset_to_grabber_map
	module_name, class_name = grabber.split('.')
	print(dataset_to_grabber_map)
	dataset_to_grabber_map[dataset] = getattr(__import__(module_name), class_name) 

def get(dataset):
	global dataset_to_grabber_map
	if not dataset in dataset_to_grabber_map.keys():
		raise Exception('Unsupported Dataset')

	return dataset_to_grabber_map[dataset]()

def all():
	global dataset_to_grabber_map
	return dataset_to_grabber_map.values()


# Tile grabber interface
class Grabber:
	def __init__(self, subclass, raster_formats=( '' ) ):
		'''
			subclass - reference to inheriting class
			bbox - latlon bound to query
			raster_format - str representing the output format of raster
			raster_res - resolution of raster
			dimen - dimension of tiles grid to create from bbox. dimen is the  width and height of grid  
		'''
		self.raster_formats = raster_formats
		self.subclass = subclass if subclass else self
		self.subclass_name = self.subclass.__class__.__name__.lower() 
		self.root_dir = os.path.abspath(os.path.dirname(__file__))
		self.cache_dir = os.path.join(self.root_dir, f'__{self.subclass_name }cache__') if self.subclass_name  else None


	#---------- interface ----------------
	# Should return (raw data, filename ) as tuple
	def prepare_retrieve(self, latlon, end_latlon, res, format):
		pass


	# Should return raw data 
	def retrieve_tile(self, latlon, end_latlon, res, format):
		raise Exception('Retrieve functionality is not implemented ')

	# ----------- actions ---------------------
	

	## TODO Create a cache max that calls clean after
	def retrieve_tiles(self, outdir, bbox, raster_format, raster_res, dimen, cache=False, prefix='Tile'):
		if not raster_format in self.raster_formats:
			raise Exception('Unsupported Format')

		self.subclass.prepare_retrieve(bbox)
		
		bbox_end = bbox[2:]
		bbox_size = bbox[2]  - bbox[0], bbox[3]  - bbox[1]
		stride = bbox_size[0]/dimen[0] , bbox_size[1]/dimen[1] 

		#for each tile in grid, create a few threads and run. Calls retrieve_tile for each tile
		j =0 
		lon = bbox[1]
		while lon < bbox_end[1]:
			i=0
			lat =bbox[0]
			while lat < bbox_end[0]:
				# TODO - thread this.
				data = self.subclass.retrieve_tile( (lat, lon), (lat+stride[0], lon+stride[1]), raster_res, raster_format)
				if not data is None:
					filename = f'{prefix}_x{i}_y{j}.{raster_format}'
					filename = os.path.join(outdir, filename)
					self.save_tile(data, filename)
				i+=1
				lat += stride[0]
			j+=1
			lon += stride[1]
		if cache:
			self.clean_cache()
		print('Done')

	def clean_cache(self):
		if not self.cache_dir is None:
			shutil.rmtree(self.cache_dir)


	# ----------- helpers  ---------------------

	# called after tile is retrieved!
	def save_tile(self,raw_data, filename):
		if raw_data:
			os.makedirs(os.path.dirname(filename), exist_ok=True)
			with open(filename, "wb") as f:
				f.write(raw_data)



