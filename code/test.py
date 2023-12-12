# use this for test python code

from PIL import Image

def is_valid_jpeg(image_path):
    try:
        with Image.open(image_path) as img:
            # Verifica se il formato dell'immagine è JPEG
            return img.format == 'JPEG'
    except Exception as e:
        # Gestisci eventuali eccezioni
        return False

# Esempio di utilizzo
image_path = "/Users/alberto/ROBOTICS/autovelox_detector_project/data/images/test/rbw_img_26.jpeg"

if is_valid_jpeg(image_path):
    print(f"L'immagine {image_path} è un JPEG valido.")
else:
    print(f"L'immagine {image_path} non è un JPEG valido o non può essere aperta correttamente.")