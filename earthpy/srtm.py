from struct import unpack,calcsize
import os,math
import urllib.request
import numpy as np



import grabber

'''
SDSC default server directory structure 
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
# register 


srtm1_server_root='https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/SRTM_GL1/SRTM_GL1_srtm'
srtm1_source_res = 3601,3601


def submatrix(arr, row_range, col_range):
	return arr[np.ix_( row_range, col_range)]


# Grabs SRTM Data Default is GL1
class SRTM(grabber.Grabber):
	def __init__(self, server_root=srtm1_server_root, source_res=srtm1_source_res):
		super().__init__(self,  raster_formats=( 'r16' ) )
		self.server_root =server_root
		self.source_res = source_res
		self.source_chunk_size = self.source_res[0]*self.source_res[1] 
		# grid of mapped memory to downloaded raster tiles
		self.raster_map = {}
		
	# Should allow to check if file is still mapped after a max cache clean. If not, remap the file
	def prepare_retrieve(self, bbox):
		# cache all files that intersect with 
		raster_i = 0
		trunc_bbox = tuple(map(math.trunc, bbox))
		for lon in range( trunc_bbox[1], trunc_bbox[3]+1):
			self.raster_map[lon]  = {}
			for lat in range(trunc_bbox[0], trunc_bbox[2]+1 ):
				filename = self.get_srtm_file_name(lat, lon) 
				self.raster_map[lon][lat] = self.load_srtm_file(lat, lon) 


	def retrieve_tile(self, latlon, end_latlon, res, format):
		# stride over each tile that overlaps and memcpy block into row. then move to next row
		raster =  None
		lat, lon = latlon
		end_lat, end_lon = end_latlon
		range_lat, range_lon = end_lat - lat, end_lon -  lon 
		
		print('-------------TILE {lat} {lon}------------------')
		tile_x =  math.trunc(lat)
		tile_y =  math.trunc(lon)
		off_lon = (abs(lon) - math.trunc(abs(lon)))

		stride_lon = range_lon


		while stride_lon >= 0:
			beg_y =  srtm1_source_res[1] * math.floor((off_lon                  ))
			end_y =  srtm1_source_res[1]
			if stride_lon != 1:
				end_y = math.floor( end_y * (1 - stride_lon + off_lon ))
			off_lat = (abs(lat) - math.trunc(abs(lat)))

			stride_lat = range_lat

			
			while stride_lat >= 0:
				beg_x =srtm1_source_res[0] * math.floor((off_lat					 ))
				end_x =  srtm1_source_res[0]
				if stride_lat != 1:
					end_x = math.floor( end_y * (1 - stride_lat + off_lat 	 ))
				print(f'SUBMATRIX')		
				print(f' {beg_x}, {end_x}  {beg_y}, {end_y}')		
				subraster = submatrix(self.raster_map[tile_y][tile_x], range(beg_y, end_y), range(beg_x, end_x))
				for row in subraster:
					raster = row if raster is None  else  np.vstack([raster, row])
				print(raster )
				stride_lat -= 1
				tile_x+=1
				off_lat = 0
			



			stride_lon -= 1
			tile_y+=1
			off_lon = 0
		
		return raster.astype('i2').tobytes()
	
		# do something with the height
		
	# ------- helpers

	def dd_to_dms(dd):
		'''
			dms is a tuple (degree, min, sed)

		'''
		degrees = math.trunc(dd)
		minutes = math.trunc( (dd-d) * 60 )
		seconds = math.trunc(dd-d-m/60* 3600)
		return degrees, minutes, seconds 


	def load_srtm_file(self, lat, lon):
		filepath = self.get_srtm_file_name(lat, lon) 
		cachefile =  os.path.join(self.cache_dir, filepath)
		url = os.path.join(self.server_root, filepath)
		# search for filename in cache. If exists do nothing
		if not os.path.exists( cachefile ):
			print(f'Caching\n{url}\n')
			# create dirs for path
			os.makedirs(os.path.dirname(cachefile), exist_ok=True)

			urllib.request.urlretrieve(url, cachefile)
		# get a mapping to the disk. 
		# NOTICE : Readsas big endian signed integers!
		raster = np.memmap(cachefile, np.dtype('>i2'), shape =self.source_chunk_size, mode = 'r').reshape(self.source_res)

		return raster 


		
		
	def get_srtm_file_name(self, lat, lon):   
		lat = math.trunc(lat)
		lon = math.trunc(lon)
		if lon >= 0:
			dirname = 'North/'
			prefix_lon = 'N' 
			if lon > 30:
				dirname = os.path.join(dirname, 'North_30_60')
			else:
				dirname = os.path.join(dirname, 'North_0_29')

		else: # if less then zero query southern tiles. remove sign
			lon *= -1
			dirname = 'South/'
			prefix_lon = 'S'

		if lat  >= 0:
			prefix_lat = 'E' 
		else: # if less then zero query westward tiles. remove sign
			lat *= -1
			prefix_lat = 'W'
		

		filename = f'{prefix_lon}{lon:02}{prefix_lat}{lat:03}.hgt'
		filepath = os.path.join(dirname, filename) 

		return filepath
	