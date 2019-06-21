#!/bin/sh
# Grab DEM data. Each tile is a 4096x4096 raster of signed 16bit integers. 
# Grabs a 3x5 grid from the Bounding Box (-120.0 35.0), (-119, 37) 





earthpy="D:/earthpy/earthpy/cli.py"
python3="C:/Users/pmiller/AppData/Local/Programs/Python/Python37-32/python.exe"





lon_min=-118.0
lon_max=-114.0

lat_min=34
lat_max=38

grid_x=2
grid_y=2
#
#echo "Grabbing SRTM Heightmaps"
#eval $python3 $earthpy retrieve                     \
#    --prefix "Height"                       \
#    --data srtm                             \
#    --outdir "Heightmaps"                   \
#    --format png                            \
#    --res 505 505                         \
#    --dimen $grid_x $grid_y                 \
#    --bbox $lat_min $lon_min $lat_max $lon_max
#exit
#

lon_min=-130.0
lon_max=-110.0

lat_min=20
lat_max=40

grid_x=20
grid_y=20

echo "Grabbing SRTM Heightmaps"
eval $python3 $earthpy retrieve                     \
    --prefix "Height"                       \
    --data srtm                             \
    --outdir "Heightmaps"                   \
    --format r16                            \
    --res 505 505                           \
    --dimen $grid_x $grid_y                 \
    --bbox $lat_min $lon_min $lat_max $lon_max

echo "Grabbing Sentinel Images"
eval $python3 $earthpy retrieve                     \
    --prefix "Sat"                          \
    --data sentinel                         \
    --outdir "Satellites"                   \
    --format jpg                            \
    --res 4096 4096                         \
    --dimen $grid_x $grid_y                 \
    --bbox $lat_min $lon_min $lat_max $lon_max 

echo "Done Grabbing Tiles for Lat Lon : [" $lat_min $lon_min "] [" $lat_max $lon_max "]"
