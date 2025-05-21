import csv
import os
from fpdf import FPDF
from datetime import datetime

EXPORT_DIR = "export"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_csv(data: list, filename: str = None):
    filename = filename or f"citation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = os.path.join(EXPORT_DIR, filename)

    with open(path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["doc_id", "citation", "sentence", "score"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return path

def export_to_pdf(data: list, filename: str = None):
    filename = filename or f"citation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(EXPORT_DIR, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for row in data:
        citation = row.get('citation', 'N/A')
        sentence = row.get('sentence', '')
        pdf.multi_cell(0, 10, f"[{citation}] {sentence}\n\n")

    pdf.output(path)
    return path


