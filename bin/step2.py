# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# step2.py
# Created on: 2016-03-05 14:41:08.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
arcpy.CheckOutExtension("3D")


# Local variables:
DEM = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\DEM"
filled = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\filled"
flow_dir = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\flow_dir"
Output_drop_raster = ""
flow_accu = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\flow_accu"
multiply = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply"
reclassed = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\reclassed"
streamtofeature_shp = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\streamtofeature.shp"

# Process: Fill
arcpy.gp.Fill_sa(DEM, filled, "")

# Process: Flow Direction
tempEnvironment0 = arcpy.env.mask
arcpy.env.mask = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\AnalysisMask"
arcpy.gp.FlowDirection_sa(filled, flow_dir, "NORMAL", Output_drop_raster)
arcpy.env.mask = tempEnvironment0

# Process: Flow Accumulation
arcpy.gp.FlowAccumulation_sa(flow_dir, flow_accu, "", "FLOAT")

# Process: Raster Calculator
description = arcpy.Describe(DEM)
cellsize=description.children[0].meanCellHeight
arcpy.gp.RasterCalculator_sa("\"%flow_accu%\"*1600/43560", multiply)

# Process: Reclassify
arcpy.Reclassify_3d(multiply, "Value", "0 250 NODATA;250 22532.1953125 2", reclassed, "DATA")

# Process: Stream to Feature
arcpy.gp.StreamToFeature_sa(reclassed, flow_dir, streamtofeature_shp, "SIMPLIFY")

