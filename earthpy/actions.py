#!/usr/bin/env python3 
import srtm,sat

# TODO add process - smooth, retile

'''
Notice : exec_* arguments much match those defined with the cli module
'''

DATASET_TO_GRABBER = {
	'srtm' : srtm.SRTMGrabber,
	'sat' : sat.SATGrabber,
}

def exec_retrieve(dataset, outdir, bbox, format, res, dimen, cache=False):
	'''
	params
	    bbox    : float tuple   ( minlat minlon maxlat maxlon )
	    dataset : tuple         "dem"|"sat"
	    res     : int           raster_resolution 
	    dimen  : (int,int  )   dimenions of tile grid
	    cache   : bool          True|False - save cached data after
	'''
	#map dataset to class and call
	DATASET_TO_GRABBER[dataset]().retrieve_tiles(outdir, bbox, format, res, dimen, cache)

def exec_clean():
	for key,value in DATASET_TO_GRABBER.items():
		value().clean_cache()
