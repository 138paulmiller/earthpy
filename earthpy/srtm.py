import grabber

from struct import unpack,calcsize
import os,math
import urllib.request
import numpy as np
import skimage



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
		super().__init__(self,  raster_formats=( 'r16','gl1') )
		self.server_root =server_root
		self.source_res = source_res
		# grid of mapped memory to downloaded raster tiles
		
	# Should allow to check if file is still mapped after a max cache clean. If not, remap the file
	def prepare_retrieve(self, bbox):
		pass # do nothing fore now. pre Loading will exceed memory mapping limits in some cases 

	def retrieve_tiles_in_bbox(self, bbox):
		# cache all files that intersect with 
		raster_i = 0
		raster_map = {}

		trunc_bbox = tuple(map(math.trunc, bbox))
		for lon in range( trunc_bbox[1], trunc_bbox[3]+1):
			raster_map[lon]  = {}
			for lat in range(trunc_bbox[0], trunc_bbox[2]+1 ):
				filename = self.get_srtm_file_name(lat, lon) 
				raster_map[lon][lat] = self.load_srtm_file(lat, lon) 
		return raster_map

	def retrieve_tile(self, latlon, end_latlon, res, format):
		# stride over each tile that overlaps and memcpy block into row. then move to next row
		# load in neighboring tiles
		lat, lon = latlon
		end_lat, end_lon = end_latlon

		raster_map =  self.retrieve_tiles_in_bbox( (lat-1, lon-1,end_lat+1, end_lon+1)) 
		raster =  None
		range_lat, range_lon = end_lat - lat, end_lon -  lon 
		
		tile_x =  math.trunc(lat)
		tile_y =  math.trunc(lon)
		off_lon = (abs(lon) - math.trunc(abs(lon)))

		stride_lon = range_lon
		

		while stride_lon > 0:
			stride_lon_frac = (abs(stride_lon) - math.trunc(abs(stride_lon)))
			
			beg_y =  math.floor( srtm1_source_res[1] * off_lon  )          
			end_y =  math.floor(beg_y + srtm1_source_res[1] * (1+stride_lon_frac )  )
  
			if tile_y < 0:
				tile_row = raster_map[ math.trunc(end_lon) ]
				range_y = range(end_y-1, beg_y-1,-1)
				
			else:
				tile_row = raster_map[tile_y]
				range_y = range(beg_y, end_y)
				
  
			off_lat = (abs(lat) - math.trunc(abs(lat)))

			stride_lat = range_lat
			while stride_lat > 0:
				stride_lat_frac = (abs(stride_lat) - math.trunc(abs(stride_lat)))
				beg_x = math.floor( srtm1_source_res[0] * off_lat)
				end_x =  math.floor(beg_x + srtm1_source_res[0] * (1+stride_lat_frac )  )
				
				if tile_x < 0:
					tile = tile_row[ math.trunc(end_lat ) ]
					range_x = range(end_x-1, beg_x-1, -1)
				else:
					tile = tile_row[tile_x]
					range_x = range(beg_x, end_x)

				subraster = submatrix(tile, range_y, range_x)
	
				raster = subraster if raster is None  else  np.vstack([raster, subraster])
				
				stride_lat -= 1
				tile_x+=1
				off_lat = 0
				
			stride_lon -= 1
			tile_y+=1
			off_lon = 0          
			
		# resize to fit resolution
		#raster = skimage.filters.gaussian(raster, sigma=2.5, mode='nearest', multichannel=True, preserve_range=True, truncate=3.0)
		raster = skimage.transform.resize(raster, res, mode='wrap', preserve_range=True,  anti_aliasing=True)        
		#scale_factor = float(res[0])/raster.shape[0], float(res[1])/raster.shape[1]
		#raster = skimage.transform.rescale(raster, scale=scale_factor, mode='wrap', preserve_range=True, multichannel=False, anti_aliasing=True)        
		return raster.astype('<i2').tobytes()
	
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
		#cachefile =  os.path.join(self.cache_dir, filepath)
		cachefile =  self.cache_dir + '/' + filepath
		
		#url = os.path.join(self.server_root, filepath)
		url = self.server_root +'/'+ filepath
		# search for filename in cache. If exists do nothing
		if not os.path.exists( cachefile ):
			print(f'Caching\n{url}\n')
			# create dirs for path
			os.makedirs(os.path.dirname(cachefile), exist_ok=True)
			try:
				urllib.request.urlretrieve(url, cachefile)
			except :
				# file does not exist. Create a file of zeroes...
				# write 16 bit zeroes as 2 bytes
				source_chunk_size_2 = self.source_res[0]*self.source_res[1] * 2 
				np.zeros(source_chunk_size_2 ).tofile(cachefile)
				
				
		source_chunk_size = self.source_res[0]*self.source_res[1] 
		raster = np.memmap(cachefile, np.dtype('>i2'), shape =source_chunk_size, mode = 'r').reshape(self.source_res)
		return raster 


		
		
	def get_srtm_file_name(self, lat, lon):   
		lat = math.trunc(lat)
		lon = math.trunc(lon)
		if lon >= 0:
			dirname = 'North/'
			prefix_lon = 'N' 
			if lon >= 30:
			   # dirname = os.path.join(dirname, 'North_30_60')
				dirname = dirname+ 'North_30_60'
			else:
				#dirname = os.path.join(dirname, 'North_0_29')
				dirname = dirname + 'North_0_29'

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
		#filepath = os.path.join(dirname, filename) 
		filepath = dirname + '/' +filename 

		return filepath
	
