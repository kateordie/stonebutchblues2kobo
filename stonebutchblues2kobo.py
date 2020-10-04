from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from PyPDF2.pdf import PageObject
import copy
import hashlib
import os
import sys

def openPDF(path):
    pdf = PdfFileReader(open(path, 'rb'))
    return pdf

def validatePDF(path):
    #Validates the PDF with a hash, to make sure you're using this absurdly specific program correctly.
    md5_hash = hashlib.md5()
    with open(path,"rb") as f:
    # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    if md5_hash.hexdigest() == '81d8aa55f97c641adda039fb604af002':
        return True
    else:
        return False

def outputPDF(pathout):
    pdfout = PdfFileWriter()
    return pdfout

if __name__ == '__main__':
    #I used an intermediate file because PyPDF doesn't seem to like doubling the pages and then cropping them.
    pathinter = "SBBIntermediate.pdf"

    pathin = sys.argv[1]
    pathout = sys.argv[2]

    if len(sys.argv) != 3:
        print("Please enter two arguments: input file, and output file name.")
        sys.exit(0)

    if not os.path.exists(pathin):
        print("Specified file does not exist.")
        sys.exit(0)

    thisPdf = openPDF(pathin)

    if validatePDF(pathin):
        print("This appears to be Stone Butch Blues by esteemed queer author Leslie Feinberg.")
    else:
        answer = ""
        while answer != "Y" and answer != "y":
            answer = input("This does not appear to be Stone Butch Blues by esteemed queer author Leslie Feinberg. Continue (Y/N)?")
            if answer == "N" or answer == "n":
                sys.exit(0)
            elif answer == "Y" or answer == "y":
                print("PDFing at your own risk!")
            else:
                print("Please enter a valid input.")
    interPdf = outputPDF(pathinter)
    #Doubles the PDF pages, since this PDF is initially formatted weird.
    for i in range (0, thisPdf.getNumPages()-1):
        page1 = thisPdf.getPage(i)
        page2 = thisPdf.getPage(i)

        interPdf.addPage(page1)
        interPdf.addPage(page2)

    interPdfFile = open(pathinter, 'wb')
    interPdf.write(interPdfFile)
    interPdfFile.close()

    thisPdf = openPDF(pathinter)
    outPdf = outputPDF(pathout)

    """Dumps all the content before and after and crops. This is all actually really good content, and I recommend you 
    read it all! It just looked pretty terrible trying to format it, so I cut it all out. You'll note that the cropping
    is just as absurdly specific as the tool would indicate - this is for SBB and SBB only.
    """
    for i in range (34, thisPdf.getNumPages()-75):
        page = thisPdf.getPage(i)

        origLowerLeftX = page.mediaBox.getLowerLeft()[0]
        origLowerRightX = page.mediaBox.getLowerRight()[0]
        origUpperLeftX = page.mediaBox.getUpperLeft()[0]
        origUpperRightX = page.mediaBox.getUpperRight()[0]
        origLowerLeftY = page.mediaBox.getLowerLeft()[1]
        origLowerRightY = page.mediaBox.getLowerRight()[1]
        origUpperLeftY = page.mediaBox.getUpperLeft()[1]
        origUpperRightY = page.mediaBox.getUpperRight()[1]
        
        if i % 2 == 0:
            page.mediaBox.lowerRight = origLowerRightX/2, origLowerRightY + 45
            page.mediaBox.upperRight = origUpperRightX/2, origUpperRightY - 45
            page.mediaBox.lowerLeft = origLowerLeftX + 45, origLowerLeftY + 45
            page.mediaBox.upperLeft = origUpperLeftX + 45, origUpperLeftY - 45

        else:
            page.mediaBox.lowerLeft = origLowerRightX/2, origLowerRightY + 45
            page.mediaBox.upperLeft = origUpperRightX/2, origUpperRightY - 45
            page.mediaBox.lowerRight = origLowerRightX - 45, origLowerRightY + 45
            page.mediaBox.upperRight = origUpperRightX - 45, origUpperRightY - 45

        outPdf.addPage(page)

    outPdfFile = open(pathout, 'wb')
    outPdf.write(outPdfFile)
    outPdfFile.close() 

    thisPdf.stream.close()
    os.remove(pathinter)

    print("PDF Cropped!")