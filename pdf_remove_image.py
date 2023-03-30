import PyPDF2
from PyPDF2 import PageObject
from PyPDF2.generic import ByteStringObject, NameObject, DictionaryObject, RectangleObject
from PIL import Image

'''
    Methods:
        get_object()
    attributes in page object
        '/Annots': All links and widgets
        '/Contents', 
        '/CropBox', 
        '/Group', 
        '/MediaBox', 
        '/Parent', 
        '/Resources':
            '/ExtGState', 
            '/Font', 
            '/ProcSet', 
            '/XObject': Holds all pictures: '/Im0', '/Im1', ...
                /BitsPerComponent', 
                '/ColorSpace', 
                '/Filter', 
                '/Height', 
                '/Interpolate', 
                '/SMask', 
                '/Subtype', 
                '/Type', 
                '/Width'
        '/Rotate', 
        '/StructParents', 
        '/Tabs', 
        '/Type', 
        '/ArtBox', 
        '/BleedBox', 
        '/TrimBox'
'''

# read logo

# Open the PDF file in read-binary mode
with open("example.pdf", "rb") as pdf_file:
    # Create a PyPDF2 PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the first page of the PDF
    page = pdf_reader.pages[0] 

    # remove "/Im0"
    del page['/Resources']['/XObject']['/Im0']

    # open jpeg
    with open('image.jpg', 'rb') as f:
        img_data = f.read()
    
    # open iimage
    img = Image.open('image.jpg')

    # Get the width and height of the image
    width, height = img.size
    
    # create new image
    # Create a new form XObject for the image
    xobj = DictionaryObject()
    xobj.update({
        NameObject('/Type'): NameObject('/XObject'),
        NameObject('/Subtype'): NameObject('/Image'),
        NameObject('/Width'): width,
        NameObject('/Height'): height,
        NameObject('/BitsPerComponent'): 8,
        NameObject('/ColorSpace'): NameObject('/DeviceRGB'),
        NameObject('/Filter'): NameObject('/DCTDecode'),
        NameObject('/Length'): len(img_data)
    })
    xobj.stream = ByteStringObject(img_data)

    # Add the form XObject to the new PDF page
    page[NameObject('/Resources')][NameObject('/XObject')] = DictionaryObject()
    page[NameObject('/Resources')][NameObject('/XObject')][NameObject('/Image')] = xobj
    page[NameObject('/Contents')] = ByteStringObject(b'q\n1 0 0 1 0 0 cm\n/Image Do\nQ\n')

        
        # Create a new PdfFileWriter object and add the modified page to it
    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.add_page(page)

    # Create a new PDF file in write-binary mode and write the modified page to it
    with open("modified.pdf", "wb") as output_file:
        pdf_writer.write(output_file)
