#!/bin/sh
# Grab DEM data. Each tile is a 4096x4096 raster of signed 16bit integers. 
# Grabs a 3x5 grid from the Bounding Box (-120.0 35.0), (-119, 37) 
echo "Grabbing DEM heightmaps"
python3 cli.py retrieve --data srtm --format r16 --res 4033 4033 --dimen 2 4 --bbox -120.0 35.0 -119.0 37.0
#echo "Grabbing Satellite images" 
#python3 cli.py retrieve --data sat --format png --res 4096 4096 --dimen 4 8 --bbox -120.0 35.0 -119.0 37.0 