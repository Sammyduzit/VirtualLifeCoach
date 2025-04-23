from barcode import EAN13
from barcode.writer import SVGWriter


with open("barcode_image.png", "wb") as f:
    EAN13(str(100000011111), writer=SVGWriter()).write(f)