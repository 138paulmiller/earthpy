#!/usr/bin/env python3
import os, sys
import argparse
import inspect

import actions

'''
sat :
	EOX::Maps's Sentinel-2 Cloudless dataset for satellite imagery. 

dem :
	NASA's SRTM1 dataset for digital elevation 
	
'''

	

ACTION_TABLE = {
	# action : callback, args used
	'retrieve' :  actions.exec_retrieve,    # retrieve tiles
	'clean' :  actions.exec_clean,          # clean all cache the datasets
}
AVAILABLE_ACTIONS = [ key for key in ACTION_TABLE.keys()]

SUPPORTED_DATASETS = ('sat', 'srtm') 
SUPPORTED_OUTPUT_FORMATS =  ('png', 'r16') 
DEFAULT_RESOLUTION = {
	# srtm gl1 data is 3601x3601 big endian sint16 raster
	'dem' :  3061,
	
	# EOX::Maps max resolution is 4096x4096 raster
	'sat' :  4096,
	
}


def cli():
	'''Helpers'''
	maybe_datum = lambda arg : arg[0] if arg else arg   
	
	try_lower = lambda s : s.lower() if isinstance(s, str) else s


	def error(msg):
		print(msg)
		print('\nSee earthpy -h for help\n')
		sys.exit(1)
	
	def get_required_func_args(func):
		params = inspect.signature(func).parameters
		return [arg for arg in params if params[arg].default is params[arg].empty ]
	
	def get_optional_func_args(func):
		params = inspect.signature(func).parameters
		return [arg for arg in params if params[arg].default is not params[arg].empty ]

		
	
	'''Command Line Interface'''
	parser = argparse.ArgumentParser(description='Retrieve and process Earth rasters')
	
	parser.add_argument('action' , help=f'Available actions: ' + ' '.join(AVAILABLE_ACTIONS),
								   metavar='Action', nargs=1)
						 
	
	parser.add_argument('--bbox' ,  help='Area of interest. WGS84 geodetic coordinates',
									metavar=('Lat', 'Lon', 'Lat', 'Lon'), nargs=4 , type=float)
	
	parser.add_argument('--dimen'  , help='Width and Height of resulting tile grid',
								   metavar='Width Height', nargs=2, type=int)
	
	parser.add_argument('--res'  , help='Resolution of output raster tiles',
								   metavar='Width Height', nargs=2, type=int)

	parser.add_argument('--dataset'  , help=f'Query raster tiles. Supported Datasets: ' + ' '.join(SUPPORTED_DATASETS),
								   metavar=('dataset_id') , nargs=1  )

	parser.add_argument('--format'  , help=f'Raster tile format. Supported Output Formats: ' + ' '.join(SUPPORTED_OUTPUT_FORMATS),
								   metavar=('Format') , nargs=1 )

	parser.add_argument('--outdir' , help=f'Raster tile output directory',
								   metavar=('path') , nargs=1, default='out' )

	
	# flag ewxample
	parser.add_argument('--cache', help='Caches raw datafiles locally. Faster re-retrieval',
	                              action='store_true')
									   
	

	# parse arguments
	cli_args  = parser.parse_args()

	# lowercase any string cli arguments with parameters
	cli_args.action     = try_lower(maybe_datum(cli_args.action  ))
	cli_args.dataset    = try_lower(maybe_datum(cli_args.dataset ))
	cli_args.format     = try_lower(maybe_datum(cli_args.format  ))

	# strip lists to datum
	cli_args.outdir     = 			maybe_datum(cli_args.outdir  )
	
	
	if cli_args.res is None:
	   cli_args.res = DEFAULT_RESOLUTION[cli_args.res]
	
	# check args    
	if not cli_args.action in AVAILABLE_ACTIONS:
		error(f'Unsupported action {cli_args.action}')
	if cli_args.bbox:
		if cli_args.bbox[0] >= cli_args.bbox[2] or cli_args.bbox[1] >= cli_args.bbox[3]: 
			error(f'Invalid bounding box {cli_args.bbox}')

	if cli_args.format :
		if not cli_args.format  in SUPPORTED_OUTPUT_FORMATS:
			error(f'Unsupported format {cli_args.format}')

	if cli_args.dataset :
		if not cli_args.dataset  in SUPPORTED_DATASETS:
			error(f'Unsupported dataset {cli_args.dataset}')

	# get action info
	action = ACTION_TABLE[ cli_args.action ]
	required_args = get_required_func_args(ACTION_TABLE[ cli_args.action ])
	optional_args = get_optional_func_args(ACTION_TABLE[ cli_args.action ])
	all_args = required_args + optional_args

	args_dict = vars(cli_args)
	# remove action. Leave only arguments
	del  args_dict['action']
	
	print(args_dict)

	# get all required and optional args from  the cli args
	action_args =  { key:args_dict[key] for key in all_args if key in args_dict.keys() and args_dict[key] != None}  
	ignored_args = [ key for key in args_dict.keys() if args_dict[key] != None and key not in all_args ]
	
	if len(ignored_args) > 0:
		print(f'Unncessary arguments. Ignoring : ' + ' '.join(ignored_args))
	
	
	if len(action_args.keys()) < len(required_args):
		error(f'Action requires the following missing arguments: '+ ' '.join(required_args - action_args.keys() ))
		
	# initiate action with args!
	action(**action_args)
	
 
if __name__ == '__main__':
	cli()
