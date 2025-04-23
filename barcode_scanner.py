import os
from barcode import EAN13
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image

def generate_barcode(data: str, output_path):
    """Generate a PNG EAN13 barcode into exactly the path you give."""
    # Ensure parent folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        EAN13(data, writer=ImageWriter()).write(f)


def read_barcode(image_path: str):
    """Decode and return barcode as string, or None if not found."""
    if not os.path.isfile(image_path):
        return None

    img = Image.open(image_path)
    decoded = decode(img)
    if decoded:
        return decoded[0].data.decode("utf-8")
    return None

def main():
    # 1) Determine a single “truth” path for both writing and reading:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file = os.path.join(script_dir, "barcode_image.png")

    # 2) Generate the barcode in that exact location
    generate_barcode("100000902922", image_file)

    # 3) Read it back
    ean = read_barcode(image_file)
    if ean:
        print(ean)
    else:
        print("No barcode found.")

if __name__ == "__main__":
    main()
