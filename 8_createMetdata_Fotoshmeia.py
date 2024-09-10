import os
import geopandas as gpd
from pyproj import Transformer
from lxml import etree

# Define the directory containing the shapefiles
directory = r'E:\SAP_FOTOSIMEIA'
output_directory=r'E:\SAP_FOTOSIMEIA'
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
    title="Τίτλος: Χρήσεις γης φωτοσημείων υποέργου ΣΑΠ"
    description="Περιγραφή: Τα ψηφιακά αυτά αρχεία περιέχουν όλα τα υποπολύγωνα με τις χρήσεις γης των φωτοσημείων του υποέργου. Είναι αρχείο μορφής shapefile (πολυγωνικό)."
    # Create XML structure
    root = etree.Element("Μεταδεδομένα")
    etree.SubElement(root, "Τίτλος").text = title
    etree.SubElement(root, "Περιγραφή").text = description
    dedomenaName=etree.SubElement(root, "Όνομα_Αρχείων_Δεδομένων")
    
    files = [f"{base_name}.shp", f"{base_name}.shx", f"{base_name}.dbf", f"{base_name}.cpg"]
    for f in files:
        etree.SubElement(dedomenaName, "Ονομα_Αρχείου").text = f
        
    titleCode=etree.SubElement(root, "Τίτλος_κωδικός_Μελέτης")
    titleCode.text="Τίτλος και κωδικός μελέτης"
    etree.SubElement(titleCode, "Τίτλος_Μελέτης").text = "Τίτλος μελέτης: Εργασίες φωτοερμηνείας και αρχικής εγκατάστασης και λήψης στοιχείων από τις δειγματοληπτικές επιφάνειες ΣΑΠ στην Αποκεντρωμένη Διοίκηση Κρήτης (Περιφέρεια Κρήτης)"
    etree.SubElement(titleCode, "Κωδικός_Mελέτης").text = "Υποέργο 8"
	
    ELEFlekseisklidia="Ελεύθερες Λέξεις Κλειδιά: ΣΑΠ, Απογραφή Δασών, Φωτοερμηνεία, Χρήσεις γης, Φωτοσημεία, Κλιματική αλλαγή."
    etree.SubElement(root, "Περιοχή_Μελέτης").text="Περιοχή: Αποκεντρωμένη Διοίκηση Κρήτης (Περιφέρεια Κρήτης)"
    etree.SubElement(root, "Γλώσσα_Μεταδεδομένων").text="Γλώσσα Μεταδεδομένων: Ελληνικά"
    etree.SubElement(root, "Γλώσσα_Πόρου").text="Γλώσσα Πόρου: Ελληνικά"
    etree.SubElement(root, "Τύπος_Πόρου").text="Τύπος Πόρου: Αρχείο shapefile"
    etree.SubElement(root, "Ημερομηνία_Μεταδεδομένων").text="2024/08/12"
    etree.SubElement(root, "Θεματικές_Κατηγορίες").text="Θεματικές κατηγορίες: Περιβάλλον (Environment)"
    etree.SubElement(root, "Ελεύθερες_Λέξεις_Κλειδιά").text=ELEFlekseisklidia
    etree.SubElement(root, "Λέξεις_Κλειδιά").text='Λέξεις Κλειδιά: GEMET - INSPIRE themes: Κάλυψη γης (Land cover) GEMET - INSPIRE themes, version 1.0, 2008-06-01'
    
    anagnwristiko="SAPChriseisgisFotosimeion_Apokentromenis_Dioikisis_Kritis"
    coordinate_element=etree.SubElement(root, "Περίγραμμα_Γεωγραφικών_Συντεταγμένων")
    coordinate_element.text="Περίγραμμα Γεωγραφικών Συντεταγμένων: "
    etree.SubElement(coordinate_element, "Νότιο_Γεωγραφικό_Πλάτος").text = f"Νότιο Γεωγραφικό Πλάτος: {min_lat:.2f}"
    etree.SubElement(coordinate_element, "Βόρειο_Γεωγραφικό_Πλάτος").text = f"Βόρειο Γεωγραφικό Πλάτος: {max_lat:.2f}"
    etree.SubElement(coordinate_element, "Δυτικό_Γεωγραφικό_Μήκος").text = f"Δυτικό Γεωγραφικό Μήκος: {min_lon:.2f}"
    etree.SubElement(coordinate_element, "Ανατολικό_Γεωγραφικό_Μήκος").text = f"Ανατολικό Γεωγραφικό Μήκος: {max_lon:.2f}"


    etree.SubElement(root, "Σύστημα_Αναφοράς_Συντεταγμένων").text="Σύστημα Αναφοράς Συντεταγμένων: GGRS87"
    
    # Create the element for spatial analysis
    xwrAnalysis_element = etree.SubElement(root, "Χωρική_Ανάλυση")
    xwrAnalysis_element.text = "Χωρική Ανάλυση:"
    # Create child elements for spatial analysis
    etree.SubElement(xwrAnalysis_element, "Ισοδύναμη_Κλίμακα").text = "Ισοδύναμη κλίμακα: 1:5.000"
    etree.SubElement(xwrAnalysis_element, "Οριζοντιογραφική_Ακρίβεια").text = "Οριζοντιογραφική Ακρίβεια: 4 μέτρα"
    etree.SubElement(xwrAnalysis_element, "Μονάδα_Μέτρησης").text = "Μονάδα μέτρησης: Μέτρα"

    etree.SubElement(root, "Ημερομηνία_Εναρξης").text="Ημερομηνία έναρξης εργασιών: 2022/07/18 (Υπογραφή σύμβασης)"
    etree.SubElement(root, "Ημερομηνία_Περάτωσης").text="Ημερομηνία περάτωσης εργασιών: 2024/08/27"
    etree.SubElement(root, "Αναγνωριστικό").text=anagnwristiko
    etree.SubElement(root, "Περιορισμοί").text="Περιορισμοί: Χωρίς περιορισμούς"
    etree.SubElement(root, "Προδιαγραφή").text="Προδιαγραφή: Το Παράρτημα 1 της διακήρυξης ανοιχτής διαδικασίας, μέσω ΕΣΗΔΗΣ για την επιλογή αναδόχου για την παροχή υπηρεσιών: «Εργασίες φωτοερμηνείας και αρχικής εγκατάστασης και λήψης στοιχείων από τις δειγματοληπτικές επιφάνειες ΣΑΠ στην Αποκεντρωμένη Διοίκηση Κρήτης (Περιφέρεια Κρήτης)»"

    ArmodioMeros = etree.SubElement(root, "Αρμόδιο_Μέρος")
    ArmodioMeros.text = "Αρμόδιο Μέρος:"
    etree.SubElement(ArmodioMeros, 'Δημιουργός_Πόρου').text="Δημιουργός του πόρου:  Ένωση των οικονομικών φορέων «ΚΑΡΤΕΡΗΣ ΑΠΟΣΤΟΛΟΣ – ΚΑΡΤΕΡΗΣ ΜΑΡΙΝΟΣ Ο.Ε. και ΟΜΙΚΡΟΝ ΣΥΜΒΟΥΛΟΙ ΠΕΡΙΒΑΛΛΟΝΤΟΣ ΑΝΩΝΥΜΗ ΕΤΑΙΡΕΙΑ»"
    stoixeiaEpikoinwnias=etree.SubElement(ArmodioMeros,'ΣτοιχείαΕπικοινωνίας')
    stoixeiaEpikoinwnias.text="Στοιχεία επικοινωνίας αναδόχου: "
    etree.SubElement(stoixeiaEpikoinwnias, 'Διεύθυνση').text="Αγίας Αναστασίας και Λαέρτου, TK 57001, Πυλαία Θεσσαλονίκης"
    etree.SubElement(stoixeiaEpikoinwnias, 'Τηλέφωνο').text="Τηλέφωνο: +30 2310365441"
    etree.SubElement(stoixeiaEpikoinwnias, 'Φαξ').text="+30 2310365442"
    etree.SubElement(ArmodioMeros, 'Όνομα').text="Όνομα εκπροσώπου του αναδόχου: Καρτέρης Απόστολος"
    etree.SubElement(ArmodioMeros, 'Αρμόδιος_Διαχείρισης').text="Αρμόδιος για την διαχείριση, τη συντήρηση και τη διανομή του πόρου: ΥΠΕΝ"
    
    
    # Convert XML structure to string
    xml_content = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    
    return xml_content

# Iterate over all files in the directory
for file in os.listdir(directory):
    if file.endswith('.shp'):
        xml_content = create_xml_content(file)
        if xml_content:
            # Write the XML content to a file
            xml_filename = os.path.splitext(file)[0] + '.xml'
            with open(os.path.join(output_directory, xml_filename), 'wb') as xml_file:
                xml_file.write(xml_content)
            print(f"Created {xml_filename}")
