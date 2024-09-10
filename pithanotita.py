import arcpy
 
# Set the workspace environment
arcpy.env.workspace = r'\\192.168.1.5\kartECO SHARED\Projects\Dimosio\K207 - TAIPED\02_Antipirika_sxedia_SP02\Working_files\Data_Help_Photos\Data\4. Paragomena Stoixeia\xartis_pithanotitas\eflektotita\SP02_Veg_Map_new_1.gdb'
 
# Set the name of your feature class
fc_name = 'PITHANOTITAS_new'
 
# Set the field names
ginomeno_field = 'GINOMENO_PITHANOTITA'
pithanotita_field = 'PITHANOTITA'
 
# Define the ranges and corresponding values
ranges = [(1, 2.5, 1), (2.6, 6.5, 2), (6.6, 12.5, 3), (12.6, 20.5, 4), (20.6, 30.5, 5),
          (30.6, 42.5, 6), (42.6, 56.5, 7), (56.6, 72.5, 8), (72.6, 90.5, 9),
          (90.6, 100, 10)]
 
# Update the 'PITHANOTITA' field based on the defined ranges
with arcpy.da.UpdateCursor(fc_name, [ginomeno_field, pithanotita_field]) as cursor:
    for row in cursor:
        ginomeno_value = row[0]
        for range_start, range_end, pithanotita_value in ranges:
            if range_start <= ginomeno_value <= range_end:
                row[1] = pithanotita_value
                break
        cursor.updateRow(row)