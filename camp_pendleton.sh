#!/bin/sh
# Grab DEM data. Each tile is a 4096x4096 raster of signed 16bit integers. 
# Grabs a 3x5 grid from the Bounding Box (-120.0 35.0), (-119, 37) 

lat_min=43  
lat_max=45 

lon_min=-119.0
lon_max=-117.0

# Resolution of grid (will create3x3 grid of 9 rasters)
grid_x=2
grid_y=2

root_dir='/media/paul/Seagate Backup Plus Drive'

echo "Grabbing SRTM Heightmaps"
./earth.py retrieve                     \
    --prefix "Height"                       \
    --data srtm                             \
    --outdir "$root_dir/CampPendleton/Heightmaps"         \
    --format r16                            \
    --res 2017 2017                         \
    --dimen $grid_x $grid_y                 \
    --bbox $lat_min $lon_min $lat_max $lon_max\
    --cache

echo "Grabbing Sentinel Images"
./earth.py  retrieve                     \
    --prefix "Sat"                          \
    --data sentinel                         \
    --outdir "$root_dir/CampPendleton/Satellites"         \
    --format jpg                            \
    --res 4096 4096                         \
    --dimen $grid_x $grid_y                 \
    --bbox $lat_min $lon_min $lat_max $lon_max \
    --cache
echo "Done Grabbing Tiles for Lat Lon : [" $lat_min $lon_min "] [" $lat_max $lon_max "]"
