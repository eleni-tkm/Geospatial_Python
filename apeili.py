import arcpy
 
# Set the workspace environment
arcpy.env.workspace = r'D:\Docs\ArcGIS\Default.gdb'
 
# Set the name of your feature class
fc_name = 'A018_PITHANOTITA_Identity_Id'
 
# Set the field names
ginomeno_field = 'GINOMENO_APEILI'
pithanotita_field = 'VATHMOS_APEILIS'
 
# Define the ranges and corresponding values
ranges = [(1, 4.5, 1), (4.6, 17.5, 2), (17.6, 45.5, 3), (45.6, 94.5, 4), (94.6, 170.5, 5),
          (170.6, 279.5, 6), (279.6, 427.5, 7), (427.6, 620.5, 8), (620.6, 864.5, 9),
          (864.6, 1000, 10)]
 
# Update the 'PITHANOTITA' field based on the defined ranges
with arcpy.da.UpdateCursor(fc_name, [ginomeno_field, pithanotita_field]) as cursor:
    for row in cursor:
        ginomeno_value = row[0]
        for range_start, range_end, pithanotita_value in ranges:
            if range_start <= ginomeno_value <= range_end:
                row[1] = pithanotita_value
                break
        cursor.updateRow(row)