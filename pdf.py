import pdfplumber



# Open the PDF file
with pdfplumber.open("example.pdf") as pdf:
    # Select a page
    page = pdf.pages[0]

    # Extract images from the page
    images = page.images

    # Loop over each image
    for i, image in enumerate(images):
        # Save the image to a file
        image.to_image().save(f"image_{i}.png")
