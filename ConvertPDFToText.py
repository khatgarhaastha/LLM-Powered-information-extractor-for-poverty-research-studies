
import os
import pypdf

def pdfparser(data):
    pages = []
    pdf = pypdf.PdfReader(open(data, "rb"))
    for page in pdf.pages:
        pages.append(page.extract_text())
    fileName = (data.split("/")[-1].split(".")[0])
    # Save the extracted text to a file
    with open(f"Data/Processed/ExtractedText_{fileName}.txt", "w", encoding="utf-8") as file:
        for page in pages:
            file.write(page)
    return pages

if __name__ == '__main__':
    for file in os.listdir("Data"):
        if file.endswith(".pdf"):
            pdfparser("Data/"+file)  