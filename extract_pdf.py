from pypdf import PdfReader
import os

pdf_path = r"c:\Users\nidok\OneDrive\Documentos\REPOSITORIOS\google_collab_project\resources\Evaluación Parcial 3 Instrucciones Encargo.pdf"

try:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")
