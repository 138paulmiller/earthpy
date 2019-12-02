from . import  grabber

from struct import unpack,calcsize
import os,math
import urllib.request
import numpy as np
import skimage
import imageio


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
		super().__init__(self,  raster_formats=( 'r16','png') )
		self.server_root =server_root
		self.source_res = source_res
		# grid of mapped memory to downloaded raster tiles
		
	# Should allow to check if file is still mapped after a max cache clean. If not, remap the file
	def prepare_retrieve(self, bbox):
		pass # do nothing fore now. pre Loading will exceed memory mapping limits in some cases 

	def retrieve_tiles_in_bbox(self, bbox, cache_dir):
		# cache all files that intersect with 
		raster_i = 0
		raster_map = {}

		trunc_bbox = tuple(map(math.trunc, bbox))
		for lat in range( trunc_bbox[0], trunc_bbox[2]):
			raster_map[lat]  = {}
			for lon in range(trunc_bbox[1], trunc_bbox[3]):
				filename = self.get_srtm_file_name(lat, lon) 
				raster_map[lat][lon] = self.load_srtm_file(lat, lon, cache_dir) 
		return raster_map


	def save_raster(self, raster, filename ):
		pixels = np.array(65536*(raster-32768)/(32767 + 32768 )  )
		#skimage.io.imsave(filename,  pixels.astype(np.uint16))
		imageio.imsave(filename,  pixels)
	
	def retrieve_tile(self, latlon, end_latlon, res, format, cache_dirself.subclass_name):
		# stride over each tile that overlaps and memcpy block into row. then move to next row
		# load in neighboring tiles
		raster = self.load_srtm_file(latlon[0],latlon[1], cache_dir)
		#raster = skimage.transform.resize(raster, res, mode='wrap', preserve_range=True,  anti_aliasing=True)        
		

		# return raster.astype('<i2').tobytes()
		raster = np.zeros(res)
		
		lat,lon = latlon
		end_lat,end_lon = end_latlon
		stride_lat,stride_lon = (end_lat - lat)/ (res[0]), (end_lon - lon)/ (res[1]) 
		
		raster_map =  self.retrieve_tiles_in_bbox( (lat-1, lon-1,end_lat+1,end_lon+1), cache_dir) 
		for raster_u in range(0, res[0]):
			lat = latlon[0]
			for raster_v in range(0, res[1]):
				tile_u = lon - math.trunc(lon)
				tile_v = lat - math.trunc(lat)				
				sample_u, sample_v = math.trunc(srtm1_source_res[0]*tile_u), srtm1_source_res[1] - 1 - math.trunc(srtm1_source_res[1]*tile_v	)		
				sample_lat, sample_lon = math.trunc(lat) , math.trunc(lon)
				raster_sample = raster_map[sample_lat][sample_lon]
				sample = raster_sample[ sample_v][sample_u] 
				if sample <= -32767:
					sample  = 1/8.0 * \
						  raster_sample[ sample_v+1][sample_u-1] + raster_sample[sample_v+1][sample_u] +  raster_sample[sample_v+1][sample_u+1] \
						+ raster_sample[ sample_v  ][sample_u-1] +                                        raster_sample[sample_v ][sample_u+1] \
						+ raster_sample[ sample_v-1][sample_u-1] + raster_sample[sample_v-1][sample_u] +  raster_sample[sample_v-1][sample_u+1] \
						
				raster[ raster_v][ raster_u    ]  = sample
				lat += stride_lat
			lon += stride_lon

		lat,lon = latlon
		# resize to fit resolution
		# raster = skimage.transform.resize(raster, res, mode='wrap', preserve_range=True,  anti_aliasing=True)        
		
		return raster
	
		# do something with the height
		
	def export_tile(self, tile, filename, format):
		if format == 'png':
			self.save_raster(tile, filename)
		elif format == 'r16':
			raw_data = tile.astype('<i2').tobytes()	
			with open(filename, "wb") as f:
				f.write(raw_data)


	# ------- helpers

	def dd_to_dms(dd):
		'''
			dms is a tuple (degree, min, sed)

		'''
		degrees = math.trunc(dd)
		minutes = math.trunc( (dd-d) * 60 )
		seconds = math.trunc(dd-d-m/60* 3600)
		return degrees, minutes, seconds 


	def load_srtm_file(self, lat, lon, cache_dir):
		filepath = self.get_srtm_file_name(lat, lon) 
		#cachefile =  os.path.join(self.cache_dir, filepath)
		cachefile =  cache_dir + '/' + filepath
		
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
		if lat >= 0:
			dirname = 'North/'
			prefix_lat = 'N' 
			if lat >= 30:
			   # dirname = os.path.join(dirname, 'North_30_60')
				dirname = dirname+ 'North_30_60'
			else:
				#dirname = os.path.join(dirname, 'North_0_29')
				dirname = dirname + 'North_0_29'

		else: # if less then zero query southern tiles. remove sign
			lat *= -1
			dirname = 'South/'
			prefix_lat = 'S'

		if lon  >= 0:
			prefix_lon = 'E' 
		else: # if less then zero query westward tiles. remove sign
			lon *= -1
			prefix_lon = 'W'
		

		filename = f'{prefix_lat}{lat:02}{prefix_lon}{lon:03}.hgt'
		#filepath = os.path.join(dirname, filename) 
		filepath = dirname + '/' +filename 

		return filepath
	
