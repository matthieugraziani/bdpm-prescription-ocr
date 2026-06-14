import easyocr
reader=easyocr.Reader(['fr'])
def extract(image):
    return "\n".join(reader.readtext(image,detail=0))
