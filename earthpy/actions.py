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

def exec_retrieve(dataset, outdir, bbox, format, res, dimen):
	'''
	params
	    bbox    : float tuple   ( minlat minlon maxlat maxlon )
	    dataset : tuple         "dem"|"sat"
	    res     : int           raster_resolution 
	    dimen  : (int,int  )   dimenions of tile grid
	    cache   : bool          True|False
	'''
	#map dataset to class and call
	print(f'{bbox}\n{dimen}\n')
	DATASET_TO_GRABBER[dataset]().retrieve_tiles(outdir, bbox, format, res, dimen)

def exec_clean(dataset):
	DATASET_TO_GRABBER[dataset]().clean_cache()
