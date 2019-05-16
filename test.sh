#!/bin/sh
# Grab DEM data. Each tile is a 4096x4096 raster of signed 16bit integers. 
# Grabs a 3x5 grid from the Bounding Box (-120.0 35.0), (-119, 37) 

lat_min=-119.0
lat_max=-109.0

lon_min=34
lon_max=44

grid_x=10
grid_y=10


# Grab raw 16 bit signed integer (r16) rasters from the SRTM data set. Res is the desired resolution (3601 x 3601 is default for srtm) Unreal expects 4033 x 4033
echo "Grabbing SRTM Heightmaps"
./earthpy.sh  retrieve --cache --data srtm  --outdir "Heightmaps" --format r16 --res  3601 3601 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max

# Grab PNG rasters from the Sentinel-2 data set. Res is the desired resolution Max is (4096 x 4096)
echo "Grabbing Sentinel Images"
./earthpy.sh retrieve --cache --data sentinel --outdir "Sentinels"  --format png --res 4096 4096 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max

# Same as above, but rather than sat images, grab just vectors illustrating elevations 
#echo "Grabbing Terrain Vector"
#./earthpy.sh retrieve --data vector   --outdir "Vectors"    --format png --res 4096 4096 --dimen $grid_x $grid_y --bbox $lat_min $lon_min $lat_max $lon_max 
echo "Done Grabbing Tiles for Lat Lon : [" $lat_min $lon_min "] [" $lat_max $lon_max "]"
