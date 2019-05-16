#!/bin/sh
# Grab DEM data. Each tile is a 4096x4096 raster of signed 16bit integers. 
# Grabs a 3x5 grid from the Bounding Box (-120.0 35.0), (-119, 37) 

lat_min=-121.0
lat_max=-111.0

lon_min=33
lon_max=43

grid_x=10
grid_y=10


echo "Grabbing SRTM Heightmaps"
#python3 cli.py retrieve --cache  --data srtm  --outdir "Heightmaps" --format r16 --res 4033 4033 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max
#converts big endian to native endinaness
python3 cli.py retrieve --cache --data srtm  --outdir "Heightmaps" --format r16 --res  3601 3601 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max


# twice as many sat images. 4 per tile
grid_x=10
grid_y=10


echo "Grabbing Sentinel Images"
python3 cli.py retrieve --cache --data sentinel --outdir "Sentinels"  --format png --res 4096 4096 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max 

echo "Done Grabbing Tiles for Lat Lon : [" $lat_min $lon_min "] [" $lat_max $lon_max "]"

#echo "Grabbing Terrain Vector"
#python3 cli.py retrieve --data vector   --outdir "Vectors"    --format png --res 4096 4096 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max 
#