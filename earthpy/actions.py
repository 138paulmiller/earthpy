import grabber
# TODO add process - smooth, retile

'''
Notice : exec_* arguments much match those defined with the cli module
'''

# Register data set grabbers
grabber.add('sentinel', 'sat.SentinelSAT')
grabber.add('vector', 'sat.VectorSAT')
grabber.add('srtm', 'srtm.SRTM')

#


def exec_retrieve(dataset, outdir, bbox, format, res, dimen, cache):
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
		grabber.get(dataset).retrieve_tiles(outdir, bbox, format, res, dimen, cache)
	except Exception as e :
		print(str(e))



def exec_clean():
	for value in grabber.all():
		value().clean_cache()
