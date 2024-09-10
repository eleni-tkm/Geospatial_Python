import os
import geopandas as gpd
from pyproj import Transformer
from lxml import etree

# Define the directory containing the shapefiles
directory = r'C:\Users\user\Desktop\SAP_FOTOSIMEIA'

# Function to create the XML content
def create_xml_content(shapefile):
    base_name = os.path.splitext(shapefile)[0]

    # Read the shapefile using geopandas
    gdf = gpd.read_file(os.path.join(directory, shapefile))

    # If CRS is unknown, set it to EPSG:4326
    if gdf.crs is None:
        gdf.set_crs(epsg=2100, inplace=True)

    # Get the bounding box and transform to EPSG:4326
    min_x, min_y, max_x, max_y = gdf.total_bounds
    transformer = Transformer.from_crs(gdf.crs, 'epsg:4326', always_xy=True)
    min_lon, min_lat = transformer.transform(min_x, min_y)
    max_lon, max_lat = transformer.transform(max_x, max_y)

    # Create the plain text content
    content = (
        "Τίτλος: Χρήσεις γης φωτοσημείων υποέργου ΣΑΠ\n"
        "Περιγραφή: Τα ψηφιακά αυτά αρχεία περιέχουν όλα τα υποπολύγωνα με τις χρήσεις γης των φωτοσημείων του υποέργου. Είναι αρχείο μορφής shapefile (πολυγωνικό).\n"
        f"Όνομα Αρχείων Δεδομένων: {base_name}.shp, {base_name}.shx, {base_name}.dbf, {base_name}.cpg\n"
        "Τίτλος-κωδικός Μελέτης: Τίτλος μελέτης: Εργασίες φωτοερμηνείας και αρχικής εγκατάστασης και λήψης στοιχείων από τις δειγματοληπτικές επιφάνειες ΣΑΠ στην Αποκεντρωμένη Διοίκηση Κρήτης (Περιφέρεια Κρήτης)\n"
        "Κωδικός Mελέτης: Υποέργο 8\n"
        "Ελεύθερες Λέξεις Κλειδιά: ΣΑΠ, Απογραφή Δασών, Φωτοερμηνεία, Χρήσεις γης, Φωτοσημεία, Κλιματική αλλαγή\n"
        "Περιοχή: Αποκεντρωμένη Διοίκηση Κρήτης (Περιφέρεια Κρήτης)\n"
        "Γλώσσα Μεταδεδομένων: Ελληνικά\n"
        "Γλώσσα Πόρου: Ελληνικά\n"
        "Τύπος Πόρου: Αρχείο shapefile\n"
        "Ημερομηνία Μεταδεδομένων: 2024/06/05\n"
        "Θεματικές κατηγορίες: Περιβάλλον (Environment)\n"
        "Λέξεις Κλειδιά: GEMET - INSPIRE themes: Κάλυψη γης (Land cover) GEMET - INSPIRE themes, version 1.0, 2008-06-01\n"
        "Περίγραμμα Γεωγραφικών Συντεταγμένων:\n"
        f"  Νότιο Γεωγραφικό Πλάτος: {min_lat:.2f}\n"
        f"  Βόρειο Γεωγραφικό Πλάτος: {max_lat:.2f}\n"
        f"  Δυτικό Γεωγραφικό Μήκος: {min_lon:.2f}\n"
        f"  Ανατολικό Γεωγραφικό Μήκος: {max_lon:.2f}\n"
        "Σύστημα Αναφοράς Συντεταγμένων: GGRS87\n"
        "Χωρική Ανάλυση:\n"
        "  Ισοδύναμη κλίμακα: 1:5.000\n"
        "  Οριζοντιογραφική Ακρίβεια: 4 μέτρα\n"
        "  Μονάδα μέτρησης: Μέτρα\n"
        "Ημερομηνία έναρξης εργασιών: 2022/07/18 (Υπογραφή σύμβασης)\n"
        "Ημερομηνία περάτωσης εργασιών: 2024/09/18\n"
        "Αναγνωριστικό: SAPChriseisgisFotosimeion_Apokentromenis_Dioikisis_Kritis\n"
        "Περιορισμοί: Χωρίς περιορισμούς\n"
        "Προδιαγραφή: Το Παράρτημα 1 της διακήρυξης ανοιχτής διαδικασίας, μέσω ΕΣΗΔΗΣ για την επιλογή αναδόχου για την παροχή υπηρεσιών: «Εργασίες φωτοερμηνείας και αρχικής εγκατάστασης και λήψης στοιχείων από τις δειγματοληπτικές επιφάνειες ΣΑΠ στην Αποκεντρωμένη Διοίκηση Κρήτης (Περιφέρεια Κρήτης)»\n"
        "Αρμόδιο Μέρος:\n"
        "  Δημιουργός του πόρου: Ένωση των οικονομικών φορέων «ΚΑΡΤΕΡΗΣ ΑΠΟΣΤΟΛΟΣ – ΚΑΡΤΕΡΗΣ ΜΑΡΙΝΟΣ Ο.Ε. και ΟΜΙΚΡΟΝ ΣΥΜΒΟΥΛΟΙ ΠΕΡΙΒΑΛΛΟΝΤΟΣ ΑΝΩΝΥΜΗ ΕΤΑΙΡΕΙΑ»\n"
        "  Στοιχεία επικοινωνίας αναδόχου:\n"
        "    Διεύθυνση: Αγίας Αναστασίας και Λαέρτου, TK 57001, Πυλαία Θεσσαλονίκης\n"
        "    Τηλέφωνο: +30 2310365441\n"
        "    Φαξ: +30 2310365442\n"
        "  Όνομα εκπροσώπου του αναδόχου: Καρτέρης Απόστολος\n"
        "  Αρμόδιος για την διαχείριση, τη συντήρηση και τη διανομή του πόρου: ΥΠΕΝ\n"
    )

    # Create XML structure
    root = etree.Element("Μεταδεδομένα")
    #plain_text_element = etree.SubElement(root, "Περιεχόμενο")
    root.text = content
    
    # Convert XML structure to string
    xml_content = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    
    return xml_content

# Iterate over all files in the directory
for file in os.listdir(directory):
    if file.endswith('.shp'):
        xml_content = create_xml_content(file)
        if xml_content:
            # Write the XML content to a file
            xml_filename = os.path.splitext(file)[0] + '_new' + '.xml'
            with open(os.path.join(directory, xml_filename), 'wb') as xml_file:
                xml_file.write(xml_content)
            print(f"Created {xml_filename}")
