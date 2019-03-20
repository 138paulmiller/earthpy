#!/usr/bin/env python3 
import dem,sat

# TODO add process - smooth, retile

'''
Notice : exec_ arguments much match those defined iwith the cli module
'''




def exec_retrieve(dataset, format, bbox, res, dimen, cache=False):
    '''
        params
            bbox    : float tuple   ( minlat minlon maxlat maxlon )
            dataset : tuple         "dem"|"sat"
            res     : int           raster_resolution 
            dimen  : (int,int  )   dimenions of tile grid
            cache   : bool          True|False
    '''
    print (f'{bbox}, {dataset}, {format}, {res}, {dimen}, {cache}')




