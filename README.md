# earthpy

Useful script for the collection and processing of Satellite and Digital elevation datasets. 
Initally created for the generation of Unreal Engine 4 Heightmaps and Textures to be used with its tiled landscape system.

# Requirements 

- Python Verion > 3.7 

- numpy scikit-image argparse
	python3 -m pip install numpy scipy scikit-image argparse

# Usage

For an example use case, see ./camp_pendleton.sh

# Unreal Landscape 

To Create a landscape for Unreal : 

1. Get Terrain Heightmap tiles

```bash
./earthpy.sh retrieve                      
    --prefix "Height"                       
    --data srtm                             
    --outdir "Heightmaps"   
    --format r16                            
    --res $resX $resY                       
    --dimen $grid_x $grid_y                 
    --bbox $lat_min $lon_min $lat_max $lon_max
```

Where $lat_min $lon_min $lat_max $lon_max are the Lat Lon BBox. 

$resX and $resY are the Target resolution of the Raster. For UE4 Tiled Landscape they must be one of the following:

8129 x 8129 
4033 x 4033 
2017 x 2017 
1009 x 1009 
505  x 505 
253  x 253 
127  x 127


2. Get the Satellite Images 
```bash
./earthpy.sh retrieve                     
    --prefix "Sat"                          
    --data sentinel                         
    --outdir "Satellites"         
    --format jpg                            
    --res $resX $resY                        
    --dimen $grid_x $grid_y                 
    --bbox $lat_min $lon_min $lat_max $lon_max 
```
$resX and $resY can be within the range 0-4096

3. Import Landscape 

a. Open Your Unreal Project 

On the toolbar
	- Select Window->World Settings 
	- Check World->Enable World Composition 
	- Select Window->Levels
	- Under the Levels Dropdown click Import Tiled Landscape
	- Click Select Heightmap Tiles and select all the desired *.r16 files in the Heightmaps directory cretaed by earthpy
	- Scale according to resolution. 
		+ The Dataset uses `3601 x 3601` tiles that represent 1 arc second ~ *30 meters*. 
		+ So, given your resolution `res` and `res == resX == resY` 
		Your XY scalar should be `30/res * 100` 
			`* 100`  because Unrealuses centimeters not meters.

4. Attach Materials
	*This part should be automated, but currently is not.*
		
	- 	- Create a Material Params Asset Like [this](res/Tile_Material_Params.png)

		- Set Tile Extent according to each tiles size in Unreal Space. To find this open the World Composition Editor [here](res/World_Composition.png)
		- Then load a tile by double clikcing it. Hovering over should give you its extent.
		
	- Create a Material Asset Like [this](res/Tile_Material.png)
	- Create a Material Instance For each Tile 
		- Each instance is defined by is Texture parameter. So, if you were to create Mat_Inst_x1_y1 thenyou shouldset its texture params like [so](res/Tile_Material_Instance.png)
	- Attach all material instances to its corresponding tile
		- Open World Composition Editor, and load all tiles. When they are loaded they should show up in the World Outliner.Select each tile and sets its Material to your newly created Material Instance