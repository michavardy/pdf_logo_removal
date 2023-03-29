import PyPDF2

# Open the PDF file in read-binary mode
with open("example.pdf", "rb") as pdf_file:
    # Create a PyPDF2 PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the first page of the PDF
    page = pdf_reader.pages[0] 

    # black list
    black_list =[]
    # Loop over each annotation
    for index, annotation in enumerate(page['/Annots']):

        # Get the annotation object
        annotation_object = annotation.get_object()

        # Check if the annotation is an image
        if  annotation_object['/Subtype'] == '/Image':
            # Remove the annotation from the page
            black_list.append(index)
    # remove first image from annotations
    del page['/Annots'][black_list[0]]
    # Decrease the annotation count
    page['/Count'] -= 1

    # Create a new PdfFileWriter object and add the modified page to it
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_writer.addPage(page)

    # Create a new PDF file in write-binary mode and write the modified page to it
    with open("modified.pdf", "wb") as output_file:
        pdf_writer.write(output_file)
