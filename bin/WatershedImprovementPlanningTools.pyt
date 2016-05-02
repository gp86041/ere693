import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            # Check out any necessary licenses
            arcpy.CheckOutExtension("spatial")
            arcpy.CheckOutExtension("3D")


            # Local variables:
            DEM = "DEM"
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
            
            log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            # Check out any necessary licenses
            arcpy.CheckOutExtension("spatial")
            arcpy.CheckOutExtension("3D")


            # Local variables:
            Impervious = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\Impervious"
            DEM = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\DEM"
            flow_accu = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\flow_accu"
            reclassed = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\reclassed"
            Impervious__3_ = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\Impervious"
            v3toraster = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3toraster"
            v3blockstatics = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3blockstatics"
            v3aggregate = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3aggregate"
            v3filled = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3filled"
            v3flow_dir = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3flow_dir"
            Output_drop_raster = ""
            v3flowacc2 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3flowacc2"
            v3divide = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3divide"
            reclassed3 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\reclassed3"
            v3multiply = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3multiply"
            v3streamtofeature_shp = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3streamtofeature.shp"

            # Process: Fill
            arcpy.gp.Fill_sa(DEM, v3filled, "")

            # Process: Flow Direction
            tempEnvironment0 = arcpy.env.mask
            arcpy.env.mask = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\AnalysisMask"
            arcpy.gp.FlowDirection_sa(v3filled, v3flow_dir, "NORMAL", Output_drop_raster)
            arcpy.env.mask = tempEnvironment0

            # Process: Calculate Field
            arcpy.CalculateField_management(Impervious, "LENGTH", "1", "VB", "")

            # Process: Feature to Raster
            description = arcpy.Describe(DEM)
            cellsize=description.children[0].meanCellHeight
            arcpy.FeatureToRaster_conversion(Impervious__3_, "LENGTH", v3toraster, "4")

            # Process: Block Statistics
            arcpy.gp.BlockStatistics_sa(v3toraster, v3blockstatics, "Rectangle 10 10 CELL", "SUM", "DATA")

            # Process: Aggregate
            arcpy.gp.Aggregate_sa(v3blockstatics, v3aggregate, "10", "MEAN", "EXPAND", "DATA")

            # Process: Flow Accumulation
            arcpy.gp.FlowAccumulation_sa(v3flow_dir, v3flowacc2, v3aggregate, "FLOAT")

            # Process: Divide
            arcpy.gp.Divide_sa(v3flowacc2, flow_accu, v3divide)

            # Process: Reclassify
            arcpy.Reclassify_3d(v3divide, "Value", "0 10 1;10 20 2;20 30 3;30 40 4;40 50 5;50 60 6;60 70 7;70 80 8;80 90 9;90 100 10", reclassed3, "DATA")

            # Process: Times
            arcpy.gp.Times_sa(reclassed3, reclassed, v3multiply)

            # Process: Stream to Feature
            arcpy.gp.StreamToFeature_sa(v3multiply, v3flow_dir, v3streamtofeature_shp, "SIMPLIFY")

            # Local variables:
            DEM = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\DEM"
            v3divide = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\3divide"
            v4filled = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\4filled"
            v4flow_dir = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\4flow_dir"
            Output_drop_raster = ""
            v4flow_accu = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\4flow_accu"
            multiply42 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply42"
            multiply45 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply45"
            multiply410 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply410"
            multiply425 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply425"
            multiply450 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply450"
            multiply4100 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply4100"
            multiply422 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply422"
            multiply452 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply452"
            multiply4102 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply4102"
            multiply4252 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply4252"
            multiply4502 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply4502"
            multiply41002 = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\multiply41002"

            # Process: Fill
            arcpy.gp.Fill_sa(DEM, v4filled, "")

            # Process: Flow Direction
            tempEnvironment0 = arcpy.env.mask
            arcpy.env.mask = "C:\\Users\\jeff\\OneDrive\\school work\\esf\\winter 2015\\GIS Modeling\\Lab6\\Lab06Data.gdb\\AnalysisMask"
            arcpy.gp.FlowDirection_sa(v4filled, v4flow_dir, "NORMAL", Output_drop_raster)
            arcpy.env.mask = tempEnvironment0

            # Process: Flow Accumulation
            arcpy.gp.FlowAccumulation_sa(v4flow_dir, v4flow_accu, "", "FLOAT")

            # Process: Raster Calculator
            arcpy.gp.RasterCalculator_sa("144*(Power(\"%4flow_accu%\"*1600/27880000,0.691))", multiply42)

            # Process: Raster Calculator (7)
            arcpy.gp.RasterCalculator_sa("28.5*(Power((\"%4flow_accu%\"*1600/27880000),0.390) )*  (Power(\"%multiply42%\", 0.338) )*( Power(\"%3divide%\" , 0.436))", multiply422)

            # Process: Raster Calculator (2)
            arcpy.gp.RasterCalculator_sa("248*(Power(\"%4flow_accu%\"*1600/27880000,0.670))", multiply45)

            # Process: Raster Calculator (8)
            arcpy.gp.RasterCalculator_sa("28.5*(Power((\"%4flow_accu%\"*1600/27880000),0.390) )*  (Power(\"%multiply45%\", 0.338) )*( Power(\"%3divide%\" , 0.436))", multiply452)

            # Process: Raster Calculator (3)
            arcpy.gp.RasterCalculator_sa("334*(Power(\"%4flow_accu%\"*1600/27880000,0.665))", multiply410)

            # Process: Raster Calculator (9)
            arcpy.gp.RasterCalculator_sa("28.5*(Power((\"%4flow_accu%\"*1600/27880000),0.390) )*  (Power(\"%multiply410%\", 0.338) )*( Power(\"%3divide%\" , 0.436))", multiply4102)

            # Process: Raster Calculator (4)
            arcpy.gp.RasterCalculator_sa("467*(Power(\"%4flow_accu%\"*1600/27880000,0.655))", multiply425)

            # Process: Raster Calculator (10)
            arcpy.gp.RasterCalculator_sa("28.5*(Power((\"%4flow_accu%\"*1600/27880000),0.390) )*  (Power(\"%multiply425%\", 0.338) )*( Power(\"%3divide%\" , 0.436))", multiply4252)

            # Process: Raster Calculator (5)
            arcpy.gp.RasterCalculator_sa("581*(Power(\"%4flow_accu%\"*1600/27880000,0.650))", multiply450)

            # Process: Raster Calculator (11)
            arcpy.gp.RasterCalculator_sa("28.5*(Power((\"%4flow_accu%\"*1600/27880000),0.390) )*  (Power(\"%multiply450%\", 0.338) )*( Power(\"%3divide%\" , 0.436))", multiply4502)

            # Process: Raster Calculator (6)
            arcpy.gp.RasterCalculator_sa("719*(Power(\"%4flow_accu%\"*1600/27880000,0.643))", multiply4100)

            # Process: Raster Calculator (12)
            arcpy.gp.RasterCalculator_sa("28.5*(Power((\"%4flow_accu%\"*1600/27880000),0.390) )*  (Power(\"%multiply4100%\", 0.338) )*( Power(\"%3divide%\" , 0.436))", multiply41002)

            
            log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
