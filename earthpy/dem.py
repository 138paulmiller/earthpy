'''
dem.py
    Digital Elevation Model Utilities. Used for retrieval and processing of elevation data.
'''
# cache all files that intersect with the bbox. Split the data accordingly to match the tile size requests


'''
If using default server:
Directory structure 
 SRTM_GL1/
    SRTM_GL1_srtm/
        North/
            North_0_29/
                N30E006.hgt
                ...
            North_30_60/
                N30E000.hgt
                ... 
        South/
            S01E006.hgt
            ...
'''
SRTM1_SERVER="https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/SRTM_GL1/"

