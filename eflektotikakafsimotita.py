import arcpy


# Set the workspace environment
arcpy.env.workspace = r'blah\blah\BLAH.gdb'

# Set the feature class name
fc_name = 'SP02_Veg_Map_final'

# Create update cursor
fields = ['VEG_TYPE', 'DENSITY', 'YPOROFOS', 'YPSOMETRO', 'EFLEKTOTITA', 'KAFSIMOTITA']
with arcpy.da.UpdateCursor(fc_name, fields) as cursor:
    for row in cursor:
        # Extract values from the row
        veg_type, density, yporofos, ypsometro = row[0], row[1], row[2], row[3]

        # Apply the specified conditions
        if veg_type == 1:
            if density == 1 and ypsometro == 1 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 9  # EFLEKTOTITA
                row[5] = 8   # KAFSIMOTITA
            elif density == 2 and ypsometro == 1 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 10
                row[5] = 10
            elif density == 3 and ypsometro == 1 and yporofos == ' ':
                row[4] = 9
                row[5] = 10
            elif density == 1 and ypsometro == 2 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 6
                row[5] = 8
            elif density == 2 and ypsometro == 2 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 8
                row[5] = 9
            elif density == 3 and ypsometro == 2 and yporofos == 'OXI':
                row[4] = 7
                row[5] = 9
            elif ypsometro == 3 and yporofos in ('NAI', 'ΝΑΙ', 'OXI'):
                row[4] = 3
                row[5] = 7

        elif veg_type == 2:
            if density == 1 and ypsometro == 1 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 4
                row[5] = 6
            elif density == 2 and ypsometro == 1 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 5
                row[5] = 7
            elif density == 3 and ypsometro == 1 and yporofos == ' ':
                row[4] = 4
                row[5] = 7
            elif density == 1 and ypsometro == 2 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 3
                row[5] = 4
            elif density == 2 and ypsometro == 2 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 4
                row[5] = 5
            elif density == 3 and ypsometro == 2 and yporofos == ' ':
                row[4] = 4
                row[5] = 5
            elif ypsometro == 3 and yporofos in ('NAI', 'ΝΑΙ', 'OXI'):
                row[4] = 1
                row[5] = 3

        elif veg_type == 3:
            if density == 1 and ypsometro == 1 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 5
                row[5] = 6
            elif density == 2 and ypsometro == 1 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 6
                row[5] = 7
            elif density == 3 and ypsometro == 1 and yporofos == 'OXI':
                row[4] = 6
                row[5] = 7
            elif density == 1 and ypsometro == 2 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 4
                row[5] = 3
            elif density == 2 and ypsometro == 2 and yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 5
                row[5] = 3
            elif density == 3 and ypsometro == 2 and yporofos == ' ':
                row[4] = 5
                row[5] = 3
            elif ypsometro == 3 and yporofos in ('NAI', 'ΝΑΙ', 'OXI'):
                row[4] = 2
                row[5] = 3

        # Continue adding conditions for other veg_types

        elif veg_type == 4:
            if density == 1 and yporofos == ' ' and ypsometro == 1:
                row[4] = 7
                row[5] = 6
            elif density == 2 and yporofos == ' ' and ypsometro == 1:
                row[4] = 8
                row[5] = 7
            elif density == 3 and yporofos == ' ' and ypsometro == 1:
                row[4] = 9
                row[5] = 8
            elif density == 1 and yporofos == ' ' and ypsometro == 2:
                row[4] = 6
                row[5] = 5
            elif density == 2 and yporofos == ' ' and ypsometro == 2:
                row[4] = 7
                row[5] = 6
            elif density == 3 and yporofos == ' ' and ypsometro == 2:
                row[4] = 8
                row[5] = 7
            elif yporofos == ' ' and ypsometro == 3:
                row[4] = 2
                row[5] = 3

        elif veg_type == 5:
            if density == 1 and yporofos == ' ' and ypsometro == 1:
                row[4] = 3
                row[5] = 3
            elif density == 2 and yporofos == ' ' and ypsometro == 1:
                row[4] = 4
                row[5] = 4
            elif density == 3 and yporofos == ' ' and ypsometro == 1:
                row[4] = 5
                row[5] = 5
            elif density == 1 and yporofos == ' ' and ypsometro == 2:
                row[4] = 2
                row[5] = 2
            elif density == 2 and yporofos == ' ' and ypsometro == 2:
                row[4] = 3
                row[5] = 3
            elif density == 3 and yporofos == ' ' and ypsometro == 2:
                row[4] = 4
                row[5] = 4
            elif yporofos == ' ' and ypsometro == 3:
                row[4] = 1
                row[5] = 2

        elif veg_type == 6:
            if yporofos == 'OXI':
                row[4] = 1
                row[5] = 2

        elif veg_type == 7:
            if yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 7
                row[5] = 6

        elif veg_type == 8:
            if yporofos in ('NAI', 'ΝΑΙ'):
                row[4] = 7
                row[5] = 5

        elif veg_type == 9:
            row[4] = 4
            row[5] = 2

        elif veg_type == 10:
            row[4] = 1
            row[5] = 2

        elif veg_type == 11:
            row[4] = 1
            row[5] = 1

        # Update the row
        cursor.updateRow(row)

# Delete the cursor
del cursor
