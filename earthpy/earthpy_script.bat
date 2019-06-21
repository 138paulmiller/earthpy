REM Grab DEM data. Each tile is a 4096x4096 raster of signed 16bit integers. 
REM Grabs a 3x5 grid from the Bounding Box (-120.0 35.0), (-119, 37) 

SET lon_min=-130.0
SET lon_max=-110.0

SET lat_min=20
SET lat_max=40

SET grid_x=10
SET grid_y=10

echo "Grabbing SRTM Heightmaps"
python cli.py retrieve --res 100 100 --prefix "Height" --data srtm --outdir "Heightmaps" --format r16 --dimen %grid_x% %grid_y% --bbox %lat_min% %lon_min% %lat_max% %lon_max%


echo "Grabbing Sentinel Images"
python cli.py retrieve --res 4096 4096 --prefix "Sat" --data sentinel --outdir "Satellites" --format jpg --dimen %grid_x% %grid_y% --bbox %lat_min% %lon_min% %lat_max% %lon_max%

echo "Done Grabbing Tiles for Lat Lon : [" $lat_min $lon_min "] [" $lat_max $lon_max "]"
