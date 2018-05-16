import string

import arcpy
from arcpy import env


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        raster = arcpy.Parameter(
        displayName="Raster",
        name="raster",
        datatype="GPRasterLayer",
        parameterType="Required",
        direction="Input")

        sample = arcpy.Parameter(
        displayName="Sample Layer",
        name="sampleLayer",
        datatype="DEFeatureClass",
        parameterType="Required",
        direction="Input")

        params = [raster, sample]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        raster = parameters[0].valueAsText
        sample = parameters[1].valueAsText
        env.workspace = "C:\Users\Pietruszka\Desktop\Teledetekcja\5\wynik"

        arcpy.MakeRasterLayer_management(raster, "band1", "", "", "1")
        arcpy.SaveToLayerFile_management("band1", "band1.lyr", "")

        arcpy.MakeRasterLayer_management(raster, "band2", "", "", "2")
        arcpy.SaveToLayerFile_management("band2", "band2.lyr", "")

        arcpy.MakeRasterLayer_management(raster, "band3", "", "", "3")
        arcpy.SaveToLayerFile_management("band3", "band3.lyr", "")

        arcpy.MakeRasterLayer_management(raster, "band4", "", "", "4")
        arcpy.SaveToLayerFile_management("band4", "band4.lyr", "")

        # Set local variables
        zoneField = "FID"

        # Check out the ArcGIS Spatial Analyst extension license
        arcpy.CheckOutExtension("Spatial")

        # Execute ZonalStatisticsAsTable
        outZon1 = arcpy.sa.ZonalStatisticsAsTable(sample, zoneField, "band1",
                                        "zonalStatBand1.dbf", "NODATA", "ALL")
        outZon2 = arcpy.sa.ZonalStatisticsAsTable(sample, zoneField, "band2",
                                        "zonalStatBand2.dbf", "NODATA", "ALL")
        outZon3 = arcpy.sa.ZonalStatisticsAsTable(sample, zoneField, "band3",
                                        "zonalStatBand3.dbf", "NODATA", "ALL")
        outZon4 = arcpy.sa.ZonalStatisticsAsTable(sample, zoneField, "band4",
                                        "zonalStatBand4.dbf", "NODATA", "ALL")

        tables = [outZon1, outZon2, outZon3, outZon4]
        band = 1
        reLayers = []
        maximum, minimum = 0, 0
        for table in tables:
            rows = arcpy.SearchCursor(table, fields="MIN; MAX")
            minList = []
            maxList = []
            for row in rows:
                minList.append(row.getValue("MIN"))
                maxList.append(row.getValue("MAX"))

            maximum = max(maxList)
            minimum = min(minList)

            nameBand = "band" + str(band)
            remap = arcpy.sa.RemapRange([[0, minimum, "NODATA"], [minimum, maximum, 1], [maximum, 1000000, "NODATA"]])
            reLayers.append(arcpy.sa.Reclassify(nameBand, "Value", remap))
            band += 1

        outFzyOv = arcpy.sa.FuzzyOverlay(reLayers, "AND")
        outFzyOv.save("fuzOvLay.tif")

        return
