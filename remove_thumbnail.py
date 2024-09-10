from PIL import Image
import piexif
import os

def add_gps_data(image_path, latitude, longitude):
    # Open the image
    image = Image.open(image_path)

    # Get the existing Exif data
    exif_data = image.info.get("exif")
    if exif_data is None:
        exif_data = {}
    else:
        exif_data = piexif.load(exif_data)

    # Create the GPSInfo dictionary
    gps_info = {
        piexif.GPSIFD.GPSLatitudeRef: "N",
        piexif.GPSIFD.GPSLatitude: _convert_to_dms(latitude),
        piexif.GPSIFD.GPSLongitudeRef: "E",
        piexif.GPSIFD.GPSLongitude: _convert_to_dms(longitude)
    }

    # Insert the GPSInfo into the existing Exif data
    exif_data["GPS"] = gps_info

    # Remove the thumbnail from the Exif data to avoid the "thumbnail too large" error
    if "thumbnail" in exif_data:
        del exif_data["thumbnail"]

    # Convert the Exif data to bytes
    exif_bytes = piexif.dump(exif_data)

    # Save the image with the modified Exif data
    image.save(image_path, exif=exif_bytes, format='JPEG')

    print(f"GPS data added to {image_path}")

def _convert_to_dms(coordinates):
    degrees, minutes, seconds = coordinates
    return ((degrees, 1), (minutes, 1), (int(seconds * 1000), 1000))

# Specify the directory containing the images
directory_path = r"Z:\Temporary\eleni_data\dasiki_katastrofi_codes_images\6928_1"

# Specify the GPS coordinates
latitude = (35, 7, 1.4)  # Example: 35°7'1.4" N
longitude = (24, 44, 52.951)  # Example: 24°44'52.951"

# Iterate over the images in the directory and add GPS data
for filename in os.listdir(directory_path):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        image_path = os.path.join(directory_path, filename)
        add_gps_data(image_path, latitude, longitude)
