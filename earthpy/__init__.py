from . import grabber
from . import sat, srtm
# TODO add process - smooth, retile

'''
Notice : exec_* arguments much match those defined with the cli module
'''

# Register data set grabbers
grabber.add('sentinel', sat.SentinelSAT)
#TODO
#grabber.add('vector', 'sat.Vector')
grabber.add('srtm', srtm.SRTM)

#



def retrieve(dataset, outdir, bbox, format, res, dimen, prefix, cache, use_xy_format):
	'''
	params
	    bbox    : float tuple   ( minlat minlon maxlat maxlon )
	    dataset : tuple         "dem"|"sat"
	    res     : int           raster_resolution 
	    dimen  : (int,int  )   dimensions of tile grid
	    cache   : bool          True|False - save cached data after?
	'''
	#map dataset to class and call
	try:
		grabber.get(dataset).retrieve_tiles(outdir, bbox, format, res, dimen, prefix, cache, use_xy_format)
	except Exception as e :
		print(str(e))



def clean():
	for value in grabber.all():
		value().clean_cache()
