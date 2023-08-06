"""Created on Thu Jul  2 14:06:03 2020.

@author: mofarrag

Make sure the working directory is set to the examples folder in the Hapi repo"
currunt_work_directory = Hapi/Example
"""
# import os
import numpy as np

from pyramids.raster import Raster as R

rpath = r"C:\MyComputer\01Algorithms\gis\pyramids"

Path = "examples/data/ZonalStatistics/"
SavePath = Path
BaseMapF = Path + "classes.tif"

ExcludedValue = 0
Compressed = True
OccupiedCellsOnly = False
#%% one map
ExtractedValues, NonZeroCells = R.overlayMap(
    Path + "maps/Map1.zip", BaseMapF, ExcludedValue, Compressed, OccupiedCellsOnly
)

MapPrefix = "Map"
# several maps
ExtractedValues, NonZeroCells = R.overlayMaps(
    Path + "maps", BaseMapF, MapPrefix, ExcludedValue, Compressed, OccupiedCellsOnly
)

# save extracted values in different files
Polygons = list(ExtractedValues.keys())
for i in range(len(Polygons)):
    np.savetxt(
        SavePath + "/" + str(Polygons[i]) + ".txt",
        ExtractedValues[Polygons[i]],
        fmt="%4.2f",
    )
